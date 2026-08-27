# TRACER Literature Evidence Matrix — TRACER-24

**Audit date:** 2026-08-27  
**Sources covered:** 27  
**Core/Critical sources:** 23  
**Verified peer-reviewed:** 24  
**Emerging non-peer-reviewed:** 3

## Canonical use

`TRACER_Literature_Evidence_Matrix.csv` is the canonical, diffable evidence table for TRACER-24. The XLSX trackers remain planning/source artifacts. The canonical matrix now includes the two recent papers discussed during Week 3 that were missing from the previous audit: **RLM-Cascade** and **Conformal Cascade**.

## Audit corrections and reconciliation

- The final peer-reviewed **FrugalGPT** publication is **TMLR 2024**; the 2023 date refers to the preprint lineage.
- The historical tracker still uses the old **TriRoute** name; the TRACER-named workbook is the updated planning copy.
- Spreadsheet reading-progress fields are not treated as proof that a paper was or was not analysed; repository notes and the canonical evidence matrix are the evidence source.
- Missing note coverage for the original tracker papers has been filled.
- Calibration, selective prediction, conformal risk control, selective generation, and recent 2025–2026 routing/risk-management work are represented.
- The evidence set now explicitly includes **RLM-Cascade (2026 preprint)** and **Conformal Cascade (2026 preprint)** in addition to **Resample or Reroute? (2026 preprint)**.
- Peer-review status is intentionally separated from relevance: recent preprints may be very close conceptually but are not treated as archival peer-reviewed evidence.

## Evidence themes covered

1. **Routing/cascading:** FrugalGPT, Hybrid LLM, AutoMix, RouteLLM, Unified Routing/Cascading, SATER, BEST-Route, LENS.
2. **Post-response / emerging cascade work:** RLM-Cascade, Resample or Reroute?, Conformal Cascade.
3. **Repair/correction:** CRITIC, Cannot Self-Correct, SLMs Need Strong Verifiers.
4. **Confidence/calibration:** Factual Confidence, Confidence Tokens, Guo et al. calibration, Jiang et al. LM calibration.
5. **Selective risk/abstention:** SelectiveNet, Conformal Risk Control, Selective Generation, CAP, Conformal Tail Risk Control.
6. **Objective validation/datasets:** DebugBench, FinQA, TAT-QA.

## What the literature rules out as novelty claims

TRACER should **not** claim novelty for any of the following by themselves:

- routing between weak and strong models;
- post-generation acceptance/escalation;
- model cascading;
- confidence-based routing;
- probability calibration;
- risk thresholds or abstention;
- conformal risk control;
- response correction;
- verifier-assisted correction;
- repeated sampling/resampling;
- response-level draft reuse or enhancement.

All of these have relevant prior art in the reviewed evidence.

## Evidence-bounded gap carried into TRACER-25

The updated evidence supports the following narrower question:

> **Among the 27 works in the current TRACER evidence set, including three relevant 2026 preprints, we found no method that exactly matches the following formulation: after observing an SLM response, predict a separately calibrated residual probability of incorrectness for ACCEPT, context-preserving REPAIR of that response, and independent REGENERATE; then apply an explicit risk threshold using only information available before the selected action executes.**

This is intentionally phrased as an **evidence-set finding**, not a universal claim that no such work exists anywhere.

## Conflicting evidence retained

- **CRITIC** shows external tool feedback can enable useful correction, while **Huang et al.** show intrinsic self-correction can fail or damage correct reasoning. TRACER must measure both **repair success** and **repair damage**.
- Confidence-token and factual-confidence work supports uncertainty features, but calibration literature shows raw model confidence is not automatically trustworthy. ACRE therefore requires explicit calibration.
- Selective prediction, conformal risk control, Selective Generation, CAP, and Conformal Cascade show that risk-controlled acceptance/abstention is established. TRACER's contribution is not the threshold itself.
- BEST-Route and Resample or Reroute? show that modern routing action spaces are richer than a simple binary weak/strong choice.
- RLM-Cascade shows that response-level draft reuse/enhancement is already an emerging idea, so the gap must focus on **separate action-conditioned residual risk**, not merely on acting after a draft exists.

## TRACER-24 acceptance status

- [x] Every approved core source has a complete matrix entry.
- [x] Proposed literature gaps are tied to explicit evidence in the matrix and TRACER-25 comparison.
- [x] Peer-review status is recorded and separated from preprint-only evidence.
- [x] Conflicting findings and limitations are documented.
- [x] Tracker inconsistencies and missing note coverage are reconciled in the canonical evidence artifacts.
- [ ] A second team member reviews the matrix for completeness.

The last checkbox is a real team-review gate and should not be marked complete automatically.
