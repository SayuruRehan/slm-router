"""
Streamlit viewer for the DebugBench + gemma3:4b PoC results (results.json).

Standalone: does not import, copy, or reference code/sula/app.py.
Read-only viewer — run run_poc.py first to generate results.json.

Author: Lithma
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[4]
RESULTS_PATH = REPO_ROOT / "results" / "baselines" / "gemma3_records.json"

st.set_page_config(page_title="DebugBench + gemma3:4b PoC viewer", layout="wide")

st.title("DebugBench + gemma3:4b PoC viewer")
st.caption(
    "gemma3:4b fixing 20 Python DebugBench problems, graded by AST comparison."
)

if not RESULTS_PATH.exists():
    st.error(
        f"No results found at `{RESULTS_PATH.name}`. "
        "Run `run_poc.py` first to generate results, then reload this page."
    )
    st.stop()

results = json.loads(RESULTS_PATH.read_text())
df = pd.DataFrame(results)

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
