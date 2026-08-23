"""Streamlit viewer for the canonical DebugBench + gemma3:4b baseline."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from tracer.experiments.viewer_runner import (
    BaselineCliUnavailableError,
    run_canonical_baseline,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
CONFIG_PATH = REPO_ROOT / "configs" / "gemma3_baseline.yaml"
RESULTS_PATH = REPO_ROOT / "results" / "baselines" / "gemma3_records.json"

st.set_page_config(page_title="DebugBench + gemma3:4b PoC viewer", layout="wide")

st.title("DebugBench + gemma3:4b PoC viewer")
st.caption("gemma3:4b on the fixed 20-row TRACER DebugBench manifest.")

if st.button("Re-run the 20 problems", type="primary"):
    # TRACER-30: Gemma uses the canonical shared runner and verifies its expected output.
    try:
        with st.spinner("Running the canonical Gemma baseline on 20 problems..."):
            outcome = run_canonical_baseline(CONFIG_PATH, RESULTS_PATH, REPO_ROOT)
    except BaselineCliUnavailableError as exc:
        st.error(str(exc))
    else:
        if outcome.success:
            st.success("Run finished and gemma3_records.json was refreshed.")
            with st.expander("Run log (stdout)"):
                st.code(outcome.stdout[-20_000:], language="text", wrap_lines=True, height=300)
        elif outcome.returncode == 0:
            st.error(
                "The runner exited successfully, but gemma3_records.json was not created or "
                "refreshed. The run is not being reported as successful."
            )
            st.code(outcome.stdout[-5000:], language="text", wrap_lines=True)
        else:
            st.error(f"Run failed (exit {outcome.returncode}). Is Ollama running?")
            st.code(outcome.stderr[-5000:], language="text", wrap_lines=True)

if not RESULTS_PATH.exists():
    st.error(
        "No standardized Gemma results found. Run `tracer-baseline --config "
        "configs/gemma3_baseline.yaml` from the repository root, or use the button above."
    )
    st.stop()

results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
df = pd.DataFrame(results)

validator_metadata = results[0].get("validator_config") if results else None
with st.expander("Validator configuration used for this result"):
    if validator_metadata:
        st.json(validator_metadata)
    else:
        st.info(
            "Legacy result file: validator metadata is not present. Re-run with the canonical "
            "baseline runner to create TRACER-29 provenance fields."
        )

with st.expander("How grading works"):
    st.markdown(
        "An outcome is **reference_match** when the extracted code's AST matches the "
        "reference, **no_change** when it matches the buggy input, **syntax_error** "
        "when it does not parse, and **needs_manual_review** when it is a different "
        "parsing solution that cannot be verified because DebugBench has no tests here."
    )

st.subheader("Summary")
outcome_counts = df["outcome"].value_counts()
cols = st.columns(1 + len(outcome_counts))
cols[0].metric("Total problems", len(df))
for col, (outcome, count) in zip(cols[1:], outcome_counts.items(), strict=False):
    col.metric(outcome, count)

st.subheader("Problems")
table_cols = ["index", "slug", "category", "subtype", "outcome", "latency_sec"]
event = st.dataframe(
    df[table_cols],
    hide_index=True,
    use_container_width=True,
    on_select="rerun",
    selection_mode="single-row",
)

selected_rows = event.selection.rows if event.selection else []
if not selected_rows:
    st.info("Select a row in the table above to see the problem detail.")
    st.stop()

row = df.iloc[selected_rows[0]]

st.subheader(f"#{row['index']} — {row['slug']}")

left, right = st.columns(2)
with left:
    st.markdown("**Buggy code**")
    st.code(row["buggy_code"], language="python", line_numbers=True)
with right:
    st.markdown("**Reference solution**")
    st.code(row["reference_solution"], language="python", line_numbers=True)

st.markdown("**Extracted code (model's fix)**")
st.code(row["extracted_code"], language="python", line_numbers=True)

with st.expander("Raw model response", expanded=False):
    st.text(row["raw_response"])
