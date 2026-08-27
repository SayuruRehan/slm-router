# TRACER Research Gap and Contribution Freeze Candidate

**Related Jira:** TRACER-25  
**Status:** Candidate for team approval  
**Date:** 2026-08-27

## Final gap statement

> **Within the current 27-paper TRACER evidence set, including recent peer-reviewed routing, selective-risk, calibration and correction work plus the 2026 RLM-Cascade, Conformal Cascade and Resample-or-Reroute preprints, we found no method that exactly matches TRACER's proposed formulation: after observing an SLM response, estimate separately calibrated residual probabilities of incorrectness for ACCEPT, context-preserving REPAIR, and independent REGENERATE, then apply an explicit risk threshold using only pre-action information.**

## What TRACER does not claim as novel

TRACER does not claim to invent:
- LLM/SLM routing;
- cascading;
- post-response escalation;
- confidence estimation;
- probability calibration;
- selective prediction or abstention;
- conformal risk control;
- response correction;
- verifier-assisted correction;
- regeneration/resampling;
- adaptive test-time compute.

## Proposed contribution

The proposed contribution is the **combination and formalisation** of:

1. a three-action post-response decision space;
2. residual-failure prediction conditioned on each action;
3. separate probability calibration for those action risks;
4. an explicit risk-controlled policy;
5. offline full-information action-outcome supervision;
6. strict prevention of inference leakage from gold/reference/action outcomes.

## Action definitions

### ACCEPT
Return the current SLM response unchanged.

### REPAIR
Use a stronger model or repair procedure **conditioned on the existing SLM response**, with the purpose of correcting that response.

### REGENERATE
Use the stronger model to solve the task independently, without treating the existing SLM answer as the object to edit.

## Risk targets

For an input instance `x` and current SLM response `y`:

- `R_ACCEPT(x, y) = P(final answer incorrect | ACCEPT, pre-action features)`
- `R_REPAIR(x, y) = P(final answer incorrect | REPAIR, pre-action features)`
- `R_REGENERATE(x, y) = P(final answer incorrect | REGENERATE, pre-action features)`

The project should avoid wording these as causal effects unless the experimental design supports such causal interpretation; they are action-conditional predictive risks learned from offline observed action outcomes.

## Routing policy candidate

1. Estimate calibrated `R_ACCEPT`, `R_REPAIR`, `R_REGENERATE`.
2. If `R_ACCEPT <= epsilon`, ACCEPT.
3. Otherwise choose the lower predicted risk of REPAIR and REGENERATE.
4. If both remediation risks exceed the acceptable threshold, record unresolved/abstention for analysis.

## Primary novelty-sensitive evaluation

The final evaluation should show whether this formulation improves:
- final incorrect-response rate;
- false acceptance;
- selective risk at epsilon;
- calibration (Brier score, ECE, reliability);
- oracle action agreement / risk regret;
- repair success and repair damage;
- transfer across SLMs.

Cost and latency remain descriptive unless the research question is explicitly broadened.

## Approval rule

Freeze this as the proposal/thesis gap only after a second team member confirms:
- the closest-work table is complete enough for the proposal;
- no selected paper was mischaracterised;
- peer-review/preprint status is correct;
- the evidence-bounded wording is acceptable.
