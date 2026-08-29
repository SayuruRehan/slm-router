# TRACER Research Definition Freeze Candidate — TRACER-26

**Version:** 1.0  
**Date:** 2026-08-27  
**Status:** Technical definition complete; requires three-member approval before Jira closure.

## Final title

**TRACER: Tri-Action Risk Assessment and Calibration for Execution Routing of Small Language Model Responses**

## Problem statement

Small language models (SLMs) can be substantially cheaper and easier to deploy than stronger models, but their responses can be unreliable. Existing routing, cascading, selective prediction, confidence estimation, calibration, and correction work provides useful mechanisms for deciding whether to trust or escalate a response. The current TRACER evidence set, however, does not identify a method that models the residual probability of failure separately for three post-response actions: returning the current SLM answer, repairing that answer, or independently regenerating a new answer.

The research problem is therefore whether, **after observing an initial SLM response**, a learned and calibrated risk estimator can predict which response-handling action is least likely to leave the final answer incorrect.

TRACER is deliberately **risk-focused**. Cost and latency are recorded as secondary descriptive measures rather than the primary optimisation objective.

## Unit of analysis

The unit of analysis is one `(task, initial SLM response)` pair. ACCEPT, REPAIR, and REGENERATE outcomes are attached to that same source response for offline supervision and evaluation.

## Operational action definitions

### ACCEPT
Return the existing SLM response unchanged.

### REPAIR
Invoke the stronger model with the original task, the existing SLM response, and only pre-action diagnostic information explicitly allowed by the frozen protocol. The stronger model is instructed to **correct the existing response**.

### REGENERATE
Invoke the stronger model to solve the original task independently. The stronger model receives the original task but **does not receive the SLM response or response-derived repair context**.

## Correctness and residual failure

For each action `a ∈ {ACCEPT, REPAIR, REGENERATE}`:

`F_a = 1` if the final response after action `a` is incorrect under the objective correctness protocol, otherwise `F_a = 0`.

Let `Z(x, y)` be the allowed pre-action feature vector. TRACER models:

`R_a(x, y) = P(F_a = 1 | Z(x, y))`

Therefore ACRE estimates `R_ACCEPT`, `R_REPAIR`, and `R_REGENERATE`.

These are **predictive action-conditional risks**, not causal treatment effects.

## ACRE

**ACRE = Action-Conditional Risk Estimator.**

### Allowed inference-time information
- task/query representation;
- initial SLM response representation;
- SLM uncertainty signals such as log-probability-derived features when available;
- pre-action validator/diagnostic signals;
- task/domain features;
- other deterministic metadata frozen before the experiment.

### Forbidden inference-time information
- gold answers;
- benchmark reference solutions;
- final correctness labels;
- downstream REPAIR or REGENERATE outcomes;
- executable-test outcomes that are not available before routing;
- features computed after the selected action has executed.

## Primary research question

> **Can a calibrated machine-learning-based action-risk model reduce the risk of returning incorrect SLM responses by learning to select among acceptance, stronger-model repair, and independent regeneration, compared with binary accept-or-escalate and fixed-action baselines?**

## Research objectives

1. Construct reproducible action-outcome data with observed ACCEPT, REPAIR, and REGENERATE outcomes.
2. Train ACRE to estimate action-conditional residual failure risk.
3. Calibrate each action-specific probability estimate.
4. Implement an explicit risk-controlled routing policy.
5. Compare against fixed-action, binary accept-or-escalate, uncalibrated, and oracle baselines.
6. Evaluate correctness risk, calibration, routing quality, repair behaviour, and cross-SLM transfer where feasible.

## Hypotheses

### H1 — Primary outcome
The calibrated TRACER policy will achieve a lower **final incorrect-response rate** than binary accept-or-escalate and fixed-action baselines on held-out data.

### H2 — Calibration
Per-action calibration will improve Brier score, Expected Calibration Error (ECE), and reliability relative to uncalibrated ACRE outputs.

### H3 — Tri-action value
Separately modelling REPAIR and REGENERATE will reduce final incorrect responses compared with collapsing both into one generic escalation action.

### H4 — Repair heterogeneity
REPAIR is not uniformly beneficial: some cases will improve while some initially correct or recoverable responses will be damaged or remain incorrect.

### H5 — Cross-SLM transfer (secondary)
ACRE will retain useful discrimination and calibration on a second SLM, although performance may degrade under transfer.

## Variables

### Independent / manipulated
- routing policy;
- calibrated vs uncalibrated risk estimates;
- tri-action vs binary action space;
- initial SLM identity;
- task domain / benchmark;
- selective-risk threshold `epsilon`.

### Dependent
**Primary:** final incorrect-response rate.

**Reliability:** false acceptance, selective risk, coverage/abstention.

**Calibration:** Brier score, ECE, reliability curves.

**Routing quality:** action accuracy, risk regret, oracle headroom.

**Action behaviour:** repair success, repair damage, regenerate success.

**Secondary descriptive:** latency, token usage, strong-model call rate, estimated/API cost where available.

## Experimental controls

- split data before downstream action generation;
- version dataset/manifests;
- freeze action prompts;
- use the same stronger-model version for REPAIR and REGENERATE in the primary study;
- freeze generation settings where supported;
- version objective validators and sandbox configuration;
- separate infrastructure failure from candidate failure;
- prohibit gold/reference/action-outcome leakage into ACRE inference features;
- record model/API version drift.

## Planned models and domains

- **Primary SLM:** Qwen3-4B-Instruct-2507
- **Cross-SLM:** Gemma 3 4B IT
- **Stronger model:** GPT-4.1
- **Code:** DebugBench plus executable EvalPlus-style HumanEval+/MBPP+ validation where appropriate
- **Numerical reasoning:** FinQA primary
- **Optional:** TAT-QA subject to scope

Any model substitution must be versioned and documented.

## Risk-controlled policy

1. Estimate calibrated `R_ACCEPT`, `R_REPAIR`, `R_REGENERATE`.
2. If `R_ACCEPT <= epsilon`, choose ACCEPT.
3. Otherwise choose the lower predicted risk between REPAIR and REGENERATE.
4. If both remediation risks exceed `epsilon`, record unresolved / optional abstention for analysis.

The unresolved state is not a fourth learned action.

## Minimum baselines

1. Always ACCEPT.
2. Always REPAIR.
3. Always REGENERATE.
4. Binary accept-or-escalate.
5. Uncalibrated ACRE.
6. Calibrated ACRE + risk policy.
7. Offline oracle action selection for analysis only.

## Evaluation hierarchy

**Primary:** final incorrect-response rate.

**Secondary reliability:** false acceptance, selective risk/coverage, Brier, ECE, reliability, action accuracy, risk regret, repair success/damage, cross-SLM transfer.

**Descriptive engineering:** latency, token counts, cost/strong-model usage.

## Frozen terminology

Use these exact terms in current artifacts:
- TRACER
- ACRE — Action-Conditional Risk Estimator
- ACCEPT
- REPAIR
- REGENERATE
- action-conditional residual failure risk
- initial SLM response
- stronger model
- pre-action feature
- objective validator
- final incorrect-response rate
- repair damage

Use **TriRoute** only when identifying a historical/legacy artifact.

## Approval gate

- [ ] Final title approved by all three team members.
- [ ] Problem statement approved.
- [ ] Research question approved.
- [ ] Action definitions approved.
- [ ] Residual-risk definition approved.
- [ ] Hypotheses and metric mapping approved.
- [ ] Proposal and presentation terminology reconciled.
- [ ] All three team members approve this freeze candidate.
