# TRACER Literature Evidence Matrix — TRACER-24

**Audit date:** 2026-08-23  
**Sources covered:** 25  
**Core/Critical sources:** 23  
**Verified peer-reviewed:** 24  
**Emerging non-peer-reviewed:** 1

## Canonical use

`TRACER_Literature_Evidence_Matrix.csv` is the canonical, diffable evidence table for Jira TRACER-24. The historical XLSX trackers remain planning artifacts. `TRACER_Research_Paper_Tracker.xlsx` is an updated workbook copy with TRACER naming, corrected FrugalGPT year, peer-review verification columns, and the newly identified literature.

## Audit corrections

- The final peer-reviewed **FrugalGPT** publication is **TMLR 2024**; the 2023 date refers to the preprint.
- The historical tracker still uses the old **TriRoute** project name.
- Spreadsheet reading-progress fields should not be treated as proof of analysis; repository note files exist even when the tracker says `Not Started`.
- Five tracker papers previously lacked note files: FrugalGPT, Hybrid LLM, LLM Cascades, Factual Confidence, and TAT-QA.
- Calibration, selective prediction, conformal risk control, selective generation, and 2025–2026 routing work were underrepresented.

## Evidence themes now covered

1. **Routing/cascading:** FrugalGPT, Hybrid LLM, AutoMix, RouteLLM, Unified Routing/Cascading, SATER, BEST-Route, LENS.
2. **Repair/correction:** CRITIC, Cannot Self-Correct, SLMs Need Strong Verifiers.
3. **Confidence/calibration:** Factual Confidence, Confidence Tokens, Guo et al. calibration, Jiang et al. LM calibration.
4. **Selective risk/abstention:** SelectiveNet, Conformal Risk Control, Selective Generation, CAP, Conformal Tail Risk Control.
5. **Objective validation/datasets:** DebugBench, FinQA, TAT-QA.
6. **Emerging closest work:** Resample or Reroute? (preprint; not peer-reviewed).

## Updated gap statement

The literature does **not** support a broad claim that existing systems only make a binary model choice. BEST-Route adds adaptive best-of-n compute, CAP learns context-dependent abstention/risk levels, selective generation controls whether generated content should be retained, and Resample-or-Reroute explicitly compares two test-time budget actions.

The narrower defensible TRACER gap is:

> **Existing work studies model routing, cascading, abstention, selective generation, self-correction, verifier-assisted correction, and adaptive test-time compute. In the reviewed evidence, however, no peer-reviewed method matches TRACER's exact post-response formulation: estimate a calibrated residual failure probability separately for ACCEPT, REPAIR that conditions on and edits the existing SLM response, and independent REGENERATE, then apply an explicit risk threshold using only information available before executing the selected action.**

This is a **working gap statement**, not yet the final novelty claim. TRACER-25 must test it against the closest works on consistent dimensions.

## Conflicting evidence that must be retained

- CRITIC shows external tool feedback can enable useful correction, while Huang et al. show intrinsic self-correction can fail or damage correct responses. TRACER should therefore measure **repair success and repair damage**, not assume correction helps.
- Confidence-token and factual-confidence work supports uncertainty features, but LM calibration and robustness studies show raw confidence is not automatically trustworthy. ACRE probabilities need explicit calibration.
- Selective prediction/conformal work shows risk thresholds are established ideas; TRACER should claim novelty in its **action-conditional tri-action residual-risk formulation**, not in thresholding/abstention itself.
- Modern routing work has moved beyond simple weak-vs-strong binary routing, so comparisons must include action-space differences rather than use a strawman.

## Peer-review policy

Use `Yes` only when a final archival venue/publisher record is verified. `Resample or Reroute?` is marked **No — preprint** as of this audit. It can be cited as emerging closest work but should not be the sole evidence supporting a core research-gap statement.

## Remaining Jira acceptance gate

A second team member still needs to review the matrix for completeness, bibliographic status, and gap interpretation before TRACER-24 can be closed.
