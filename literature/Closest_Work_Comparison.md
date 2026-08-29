# TRACER-25 — Closest-Work Comparison and Research-Gap Validation

**Date:** 2026-08-27

## Purpose

This artifact tests the proposed TRACER gap against the closest works using consistent comparison dimensions:

- decision timing and input signals;
- action space;
- risk/objective target;
- calibration/risk-control method;
- validation source;
- dataset/task setting;
- reported limitation relevant to TRACER;
- the exact distinction TRACER still proposes.

The machine-readable version is `Closest_Work_Comparison.csv`.

## Closest-work synthesis

### 1. Routing and cascading already cover much more than binary weak-vs-strong selection
FrugalGPT, RouteLLM, Unified Routing/Cascading, SATER, BEST-Route, and LENS show that modern routing includes learned quality estimation, cascades, adaptive compute, and probabilistic treatment of uncertain feedback. Therefore TRACER must not use a strawman such as "existing routing is only binary."

### 2. Post-response accept/escalate is already established
AutoMix and post-generation cascade work use information from an already generated response to decide whether to keep it or involve a stronger model. RLM-Cascade goes even closer by operating on a draft response and including an enhancement path. Therefore "we make the decision after seeing the SLM response" is **not sufficient novelty**.

### 3. Calibration, abstention, and explicit risk thresholds are established
Guo et al., Jiang et al., SelectiveNet, Conformal Risk Control, Selective Generation, CAP, Conformal Tail Risk Control, and Conformal Cascade establish probability calibration, risk/coverage trade-offs, adaptive abstention, and conformal risk control. TRACER's epsilon threshold and calibration are methodologically justified by prior work but should not be presented as new in isolation.

### 4. Repair/correction is established, and its value is conditional
CRITIC shows that external tool feedback can enable correction. Huang et al. show that unaided self-correction can fail or damage correct reasoning. Strong-verifier work shows that verifier capability can determine whether SLM correction succeeds. This directly supports TRACER's decision to model **repair risk** and to measure **repair damage**, rather than assuming correction is always beneficial.

### 5. Multi-action test-time allocation is emerging
BEST-Route selects both model and sample count. Resample or Reroute? explicitly allocates budget between two test-time actions. CAP selects context-dependent risk/abstention behaviour. These works rule out a broad "first multi-action router" claim.

## What is adapted from prior work

TRACER intentionally adapts or builds on established ideas:

- learned routing / cascading;
- output-derived uncertainty and verifier features;
- probability calibration;
- selective-risk thresholds;
- stronger-model assistance;
- response correction;
- objective validation using executable/programmatic checks.

These should be cited as methodological foundations, not claimed as original inventions.

## What TRACER proposes as the specific contribution

The evidence supports a narrower contribution:

1. **Post-response action definition:** after an SLM produces a candidate response, treat the next decision as one of three explicit response-handling actions:
   - **ACCEPT** — return the existing SLM response unchanged;
   - **REPAIR** — give the existing SLM response to a stronger model/repair procedure and ask it to correct that response;
   - **REGENERATE** — ask the stronger model to solve independently without being anchored to the SLM answer.

2. **Action-conditional residual-risk target:** estimate the probability that the final answer remains incorrect **after each action**, rather than estimating one generic confidence score or only which model is stronger.

3. **Separate calibrated heads:** learn `R_ACCEPT`, `R_REPAIR`, and `R_REGENERATE`, then calibrate each action's predicted failure probability.

4. **Risk-controlled policy:** ACCEPT only when `R_ACCEPT <= epsilon`; otherwise choose the lower predicted risk between REPAIR and REGENERATE. If both exceed the risk tolerance, record the case as unresolved/abstention for analysis rather than inventing a fourth learned action.

5. **Pre-action inference constraint:** ACRE may use the query/task, existing SLM response, uncertainty, validator, and task features, but not gold answers, reference solutions, or the outcomes of actions that have not yet been executed.

6. **Full-information offline supervision:** during dataset construction, all three action outcomes can be generated/evaluated offline to create labels for the three heads. Those labels are training/evaluation evidence, not inference-time features.

## Final evidence-bounded gap statement

> **Within the current 27-paper TRACER evidence set, including recent peer-reviewed routing, selective-risk, calibration and correction work plus the 2026 RLM-Cascade, Conformal Cascade and Resample-or-Reroute preprints, we found no method that exactly matches TRACER's proposed formulation: after observing an SLM response, estimate separately calibrated residual probabilities of incorrectness for ACCEPT, context-preserving REPAIR, and independent REGENERATE, then apply an explicit risk threshold using only pre-action information.**

This wording is deliberately bounded to the reviewed evidence set. It should not be rewritten as an absolute claim that "no previous work exists."

## Research novelty statement for the proposal

A concise proposal-safe version is:

> **TRACER's proposed contribution is an action-conditional risk formulation for post-response SLM routing. Rather than predicting only whether an SLM answer is trustworthy or whether a stronger model should be invoked, TRACER estimates the residual probability of failure under three explicit response-handling actions—ACCEPT, REPAIR, and independent REGENERATE—and calibrates those risks for use in a selective risk-control policy.**

## Research question alignment

The gap supports the current primary research question:

> **Can a calibrated machine-learning-based action-risk model reduce the risk of returning incorrect SLM responses by learning to select among acceptance, stronger-model repair, and independent regeneration, compared with binary accept-or-escalate and fixed-action baselines?**

## Baselines implied by the literature

At minimum, the final experiment should include:

- always ACCEPT;
- always REPAIR;
- always REGENERATE;
- binary accept-or-escalate baseline;
- uncalibrated ACRE/router;
- calibrated ACRE + epsilon policy;
- oracle action selection for analysis only.

Where practical, include confidence-threshold or cascade-style baselines reflecting AutoMix/selective-risk prior work.

## TRACER-25 acceptance status

- [x] Closest relevant works identified from the evidence matrix.
- [x] Consistent comparison dimensions used.
- [x] Gap claims tied to specific prior-work differences.
- [x] Novel versus adapted elements explicitly separated.
- [ ] Team reviews and approves the final gap statement.

The final checkbox is a real team-review gate and should not be auto-completed.
