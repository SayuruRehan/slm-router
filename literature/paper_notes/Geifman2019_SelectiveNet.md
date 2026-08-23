# Paper Notes — SelectiveNet: A Deep Neural Network with an Integrated Reject Option

**Authors:** Yonatan Geifman; Ran El-Yaniv  
**Year / Venue:** 2019 / ICML  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.mlr.press/v97/geifman19a.html  
**Stable source:** https://arxiv.org/abs/1901.09192  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Optimise predictions jointly with a reject/abstain option.

## Setting / Data
Deep classification/regression selective prediction.

## Method
Integrated reject option trained end-to-end under target coverage.

## Evaluation
Risk-coverage trade-off.

## Key Finding
Jointly learned selection can improve risk at a given coverage over confidence-threshold baselines.

## Limitations / Conflicting Evidence
Binary predict/reject framing; not generative action selection.

## Relevance to TRACER
Foundational selective-risk/coverage concept for TRACER's epsilon policy.

## Gap Evidence
TRACER has three actions and chooses between two remediation actions after ACCEPT is unsafe.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
