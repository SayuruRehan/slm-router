# Paper Notes — On Calibration of Modern Neural Networks

**Authors:** Chuan Guo; Geoff Pleiss; Yu Sun; Kilian Q. Weinberger  
**Year / Venue:** 2017 / ICML  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.mlr.press/v70/guo17a.html  
**Stable source:** https://arxiv.org/abs/1706.04599  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Make predicted probabilities correspond to empirical correctness likelihood.

## Setting / Data
Modern neural networks on classification tasks.

## Method
Compares post-hoc calibration methods; introduces temperature scaling as an effective practical baseline.

## Evaluation
Calibration error/reliability alongside predictive accuracy.

## Key Finding
Modern neural networks can be poorly calibrated; temperature scaling is a strong simple post-hoc method.

## Limitations / Conflicting Evidence
Classification setting, not autoregressive LLM action routing.

## Relevance to TRACER
Direct methodological foundation for ACRE per-head temperature scaling.

## Gap Evidence
TRACER applies calibration to action-conditional residual-failure probabilities.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
