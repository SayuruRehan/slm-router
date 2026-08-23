# Paper Notes — CAP: Conformalized Abstention Policies for Context-Adaptive Risk Management for LLMs and VLMs

**Authors:** Sina Tayebati; Divake Kumar; Nastaran Darabi; Dinithi Jayasuriya; Theja Tulabandhula; Ranganath Krishnan; Amit Ranjan Trivedi  
**Year / Venue:** 2025 / ACML  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.mlr.press/v304/tayebati26a.html  
**Stable source:** https://proceedings.mlr.press/v304/tayebati26a.html  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Adapt abstention/risk levels per instance rather than applying one global conformal level.

## Setting / Data
LLMs/VLMs, hallucination detection and selective generation.

## Method
Reinforcement-learning policy selects per-instance conformal risk level; includes point prediction, set prediction and abstention.

## Evaluation
Coverage, hallucination AUROC, AUARC, calibration error.

## Key Finding
Maintains target coverage while improving selective-generation/risk-management metrics over static conformal baselines.

## Limitations / Conflicting Evidence
Focuses on abstention/risk-level choice, not choosing among repair and independent regeneration outcomes.

## Relevance to TRACER
Updated evidence that adaptive risk management can be multi-action, so TRACER gap must be precise.

## Gap Evidence
TRACER's specific contribution is calibrated residual failure for three response-handling actions.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
