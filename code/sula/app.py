import json
from pathlib import Path

import streamlit as st

from tracer.experiments.viewer_runner import (
    BaselineCliUnavailableError,
    run_canonical_baseline,
)

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
CONFIG_PATH = REPO_ROOT / "configs" / "qwen25_coder_baseline.yaml"
RESULTS_PATH = REPO_ROOT / "results" / "baselines" / "qwen25_coder_records.json"

st.set_page_config(page_title="DebugBench SLM smoke test", layout="wide")

st.title("DebugBench SLM smoke test")
st.caption(
    "qwen2.5-coder:1.5b on the fixed 20-row TRACER DebugBench manifest. "
    "Select a row to compare the code."
)

if st.button("Re-run the 20 problems", type="primary"):
    # TRACER-30: Qwen uses the canonical shared runner and verifies its expected output.
    try:
        with st.spinner("Running the canonical Qwen baseline on 20 problems..."):
            outcome = run_canonical_baseline(CONFIG_PATH, RESULTS_PATH, REPO_ROOT)
    except BaselineCliUnavailableError as exc:
        st.error(str(exc))
    else:
        if outcome.success:
            st.success("Run finished and qwen25_coder_records.json was refreshed.")
            with st.expander("Run log (stdout)"):
                st.code(outcome.stdout[-20_000:], language="text", wrap_lines=True, height=300)
        elif outcome.returncode == 0:
            st.error(
                "The runner exited successfully, but qwen25_coder_records.json was not "
                "created or refreshed. The run is not being reported as successful."
            )
            st.code(outcome.stdout[-5000:], language="text", wrap_lines=True)
        else:
            st.error(f"Run failed (exit {outcome.returncode}). Is Ollama running?")
            st.code(outcome.stderr[-5000:], language="text", wrap_lines=True)

if not RESULTS_PATH.exists():
    st.warning(
        "No standardized Qwen results found. Run `tracer-baseline --config "
        "configs/qwen25_coder_baseline.yaml` from the repository root, or use the button above."
    )
    st.stop()

with RESULTS_PATH.open(encoding="utf-8") as result_file:
    results = json.load(result_file)

st.caption(f"Showing results from: {RESULTS_PATH}")

validator_metadata = results[0].get("validator_config") if results else None
with st.expander("Validator configuration used for this result"):
    if validator_metadata:
        st.json(validator_metadata)
    else:
        st.info(
            "Legacy result file: validator metadata is not present. Re-run with the canonical "
            "baseline runner to create TRACER-29 provenance fields."
        )

with st.expander("What do these columns mean?"):
    st.markdown("""
**Outcome** — the validation result per problem:

| Label | Meaning |
| --- | --- |
| `reference_match` | Output AST matches the reference; useful evidence but not execution-tested. |
| `needs_manual_review` | Output changed the bug, but there are no tests to prove correctness. |
| `syntax_error` | Model output is not valid Python at all — it never got to be right or wrong. |
| `no_change` | Model handed back the buggy code unchanged. |

**Fixed? (AST)** — Check A. The correctness signal: model output vs. reference solution, compared as
normalised syntax trees, so whitespace/comments/formatting are ignored.

**Unchanged? (AST)** — Check B. Model output vs. the *buggy input*.
True means the model changed nothing.

**Cosine (diagnostic)** — Check C. Character-trigram similarity to the reference.
**Not a correctness signal.** Buggy and fixed code are near-identical on this dataset, so this sits
near 0.97 for many samples and is logged as diagnostic evidence rather than a grading rule.

**Manual verdict** — empty by default, for hand review. AST matching can reject a
functionally correct alternative implementation, so unresolved records are reviewed rather than
silently counted wrong.
""")

counts = {}
for result in results:
    counts[result["outcome"]] = counts.get(result["outcome"], 0) + 1
review_rate = sum(1 for result in results if result["needs_manual_review"]) / len(results)

cols = st.columns(5)
cols[0].metric("Needs review", f"{review_rate:.0%}")
for col, outcome in zip(
    cols[1:],
    ["reference_match", "needs_manual_review", "syntax_error", "no_change"],
    strict=True,
):
    col.metric(outcome, counts.get(outcome, 0))

table = [
    {
        "#": result["index"],
        "Problem": result["slug"],
        "Bug category": result["category"],
        "Bug subtype": result["subtype"],
        "Outcome": result["outcome"],
        "Fixed? (AST)": result["check_a_correct"],
        "Unchanged? (AST)": result["check_b_unchanged"],
        "Cosine (diagnostic)": result["check_c_cosine_diagnostic_only"],
        "Latency (s)": result["latency_sec"],
        "Manual verdict": result["manual_verdict"],
    }
    for result in results
]

event = st.dataframe(
    table,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "#": st.column_config.NumberColumn(width="small", help="Row index in this run."),
        "Problem": st.column_config.TextColumn(width="medium", help="DebugBench problem slug."),
        "Bug category": st.column_config.TextColumn(
            width="small",
            help="Bug class from the dataset, e.g. syntax / logic / reference error.",
        ),
        "Bug subtype": st.column_config.TextColumn(
            width="small", help="Specific bug injected, e.g. illegal indentation."
        ),
        "Outcome": st.column_config.TextColumn(
            width="small",
            help="reference_match / needs_manual_review / syntax_error / no_change.",
        ),
        "Fixed? (AST)": st.column_config.CheckboxColumn(
            width="small", help="Check A: matches the reference solution as a syntax tree."
        ),
        "Unchanged? (AST)": st.column_config.CheckboxColumn(
            width="small", help="Check B: model returned the buggy code unchanged."
        ),
        "Cosine (diagnostic)": st.column_config.NumberColumn(
            width="small",
            format="%.3f",
            help="Check C: diagnostic only, not a correctness signal.",
        ),
        "Latency (s)": st.column_config.NumberColumn(
            width="small", format="%.1f", help="Wall-clock time for the Ollama call."
        ),
        "Manual verdict": st.column_config.TextColumn(
            width="small", help="Empty until hand-reviewed; edit in the stored result."
        ),
    },
)

selected_rows = event["selection"]["rows"]
if not selected_rows:
    st.info("Select a row above to see the code comparison.")
else:
    selected = results[selected_rows[0]]
    st.subheader(f"[{selected['index']}] {selected['slug']}")
    st.caption(
        f"{selected['category']} → {selected['subtype']}  ·  "
        f"outcome: **{selected['outcome']}**"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Buggy code** (input)")
        st.code(selected["buggy_code"], language="python", line_numbers=True, height=420)
    with col2:
        st.markdown("**Model output** (extracted)")
        st.code(selected["extracted_code"], language="python", line_numbers=True, height=420)
    with col3:
        st.markdown("**Reference solution**")
        st.code(
            selected["reference_solution"], language="python", line_numbers=True, height=420
        )

    with st.expander("Raw model response (before code extraction)"):
        st.code(selected["raw_response"], language="markdown", wrap_lines=True, height=300)
