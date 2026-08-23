# Paper Notes — LENS: Latent Precision Inference in Multi-LLM Routing

**Authors:** Juntao Liu; Lixing Yu; Kun Yue; Zhiwen Tang  
**Year / Venue:** 2026 / UAI  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.mlr.press/v337/liu26b.html  
**Stable source:** https://proceedings.mlr.press/v337/liu26b.html  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Make routing robust when interaction-derived feedback has unknown/variable precision under logging noise and drift.

## Setting / Data
Multi-LLM routing under task/model distribution shifts.

## Method
Probabilistic latent-precision model with posterior utility maximisation and variational inference.

## Evaluation
Performance-cost trade-offs under distribution shift.

## Key Finding
Explicitly modeling feedback precision improves routing, especially under task/model shifts.

## Limitations / Conflicting Evidence
Routes among models using feedback signatures; no explicit post-response repair action.

## Relevance to TRACER
Very recent evidence on uncertainty in supervision and routing calibration under shift.

## Gap Evidence
TRACER should separate label/validator reliability concerns from its action-conditional risk model.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
