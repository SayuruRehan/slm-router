import json
import os
import subprocess
import sys

import streamlit as st

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
RESULTS_PATH = os.path.join(
    REPO_ROOT, "results", "baselines", "qwen25_coder_records.json"
)
RUN_PATH = os.path.join(HERE, "run.py")

st.set_page_config(page_title="DebugBench SLM smoke test", layout="wide")

st.title("DebugBench SLM smoke test")
st.caption("qwen2.5-coder:1.5b on the fixed 20-row TRACER DebugBench manifest. "
           "Select a row to compare the code.")

if st.button("Re-run the 20 problems", type="primary"):
    with st.spinner("Calling Ollama on 20 problems, one at a time..."):
        proc = subprocess.run([sys.executable, RUN_PATH], capture_output=True, text=True)
    if proc.returncode == 0:
        st.success("Run finished. Results below are freshly generated.")
        with st.expander("Run log (stdout)"):
            st.code(proc.stdout[-20000:], language="text", wrap_lines=True, height=300)
    else:
        st.error(f"Run failed (exit {proc.returncode}). Is Ollama running?")
        st.code(proc.stderr[-5000:], language="text", wrap_lines=True)

if not os.path.exists(RESULTS_PATH):
    st.warning("No results.json yet — press the button above to generate it.")
    st.stop()

with open(RESULTS_PATH) as f:
    results = json.load(f)

st.caption(f"Showing results from: {RESULTS_PATH}")

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
**Not a correctness
signal.** Buggy and fixed code are near-identical on this dataset, so this sits ~0.97 for everything
and discriminates nothing — it is logged to demonstrate that, not to grade with it.

**Manual verdict** — empty by default, for hand-review. AST matching gives false negatives when the
model fixes the bug correctly but differently from the reference, so at n=10 these get read by eye.
""")

counts = {}
for r in results:
    counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
review_rate = sum(1 for r in results if r["needs_manual_review"]) / len(results)

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
        "#": r["index"],
        "Problem": r["slug"],
        "Bug category": r["category"],
        "Bug subtype": r["subtype"],
        "Outcome": r["outcome"],
        "Fixed? (AST)": r["check_a_correct"],
        "Unchanged? (AST)": r["check_b_unchanged"],
        "Cosine (diagnostic)": r["check_c_cosine_diagnostic_only"],
        "Latency (s)": r["latency_sec"],
        "Manual verdict": r["manual_verdict"],
    }
    for r in results
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
            width="small", help="Specific bug injected, e.g. illegal indentation."),
        "Outcome": st.column_config.TextColumn(
            width="small",
            help="correct / incorrect / syntax_error / no_change. See the explainer above."),
        "Fixed? (AST)": st.column_config.CheckboxColumn(
            width="small", help="Check A: matches the reference solution as a syntax tree."),
        "Unchanged? (AST)": st.column_config.CheckboxColumn(
            width="small", help="Check B: model returned the buggy code unchanged."),
        "Cosine (diagnostic)": st.column_config.NumberColumn(
            width="small", format="%.3f",
            help="Check C: DIAGNOSTIC ONLY, not a correctness signal."),
        "Latency (s)": st.column_config.NumberColumn(
            width="small", format="%.1f", help="Wall-clock time for the Ollama call."),
        "Manual verdict": st.column_config.TextColumn(
            width="small", help="Empty until hand-reviewed; edit in results.json."),
    },
)

selected_rows = event["selection"]["rows"]
if not selected_rows:
    st.info("Select a row above to see the code comparison.")
else:
    r = results[selected_rows[0]]
    st.subheader(f"[{r['index']}] {r['slug']}")
    st.caption(f"{r['category']} → {r['subtype']}  ·  outcome: **{r['outcome']}**")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Buggy code** (input)")
        st.code(r["buggy_code"], language="python", line_numbers=True, height=420)
    with col2:
        st.markdown("**Model output** (extracted)")
        st.code(r["extracted_code"], language="python", line_numbers=True, height=420)
    with col3:
        st.markdown("**Reference solution**")
        st.code(r["reference_solution"], language="python", line_numbers=True, height=420)

    with st.expander("Raw model response (before code extraction)"):
        st.code(r["raw_response"], language="markdown", wrap_lines=True, height=300)
