# TRACER-8 Literature Repository Audit

## What was checked
- `literature/TriRoute_Research_Paper_Tracker.xlsx`
- `literature/paper-tracker-accept-edit-regenerate.xlsx` (repository presence/version noted)
- all files currently listed under `literature/paper_notes/`
- updated public literature through 2026-08-23 for routing, calibration, selective risk, abstention, repair/correction and objective validation

## Findings
- Two spreadsheet tracker artifacts exist; a canonical CSV is preferable for version-controlled research evidence.
- Ten paper-note Markdown files existed before this audit.
- Five papers already present in the main tracker lacked a note file.
- Existing notes are useful but several still contain `Not yet read`, `TBD`, or full-text-reading placeholders.
- `TriRoute_Research_Paper_Tracker.xlsx` still uses the previous project name.
- The tracker copy records FrugalGPT as 2023/TMLR; final TMLR publication is 2024.
- The tracker is strong on routing/cascading and correction, but did not adequately cover calibration/selective-risk foundations or the newest 2025–2026 related work.

## Changes prepared in this patch
- canonical CSV evidence matrix;
- Markdown synthesis;
- updated TRACER-named XLSX tracker;
- five missing note files for papers already tracked;
- ten additional notes covering calibration/selective-risk foundations and newer closest work.

## Important novelty correction
Do not write that all prior routers are binary. The literature now includes adaptive best-of-n routing, abstention policies, selective generation, and resampling/rerouting. The TRACER gap must remain specific to calibrated post-response residual failure risk across ACCEPT, REPAIR, and independent REGENERATE.
