# Paper Notes — Conformal Tail Risk Control for Large Language Model Alignment

**Authors:** Catherine Chen; Jingyan Shen; Zhun Deng; Lihua Lei  
**Year / Venue:** 2025 / ICML  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.mlr.press/v267/chen25bd.html  
**Stable source:** https://arxiv.org/abs/2502.20285  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Control severe/tail LLM failures under imperfect automated scoring.

## Setting / Data
Black-box LLM outputs and human-machine scoring misalignment.

## Method
Conformal calibration for distortion/tail risk measures using L-statistics.

## Evaluation
Tail/distortion risk and high-confidence guarantees.

## Key Finding
Provides calibrated guarantees for tail-risk measures despite scorer mismatch.

## Limitations / Conflicting Evidence
Alignment/tail-risk calibration, not tri-action routing or response repair.

## Relevance to TRACER
Strengthens TRACER's risk-calibration theoretical context.

## Gap Evidence
TRACER predicts per-action ordinary residual failure; it should not imply conformal tail guarantees unless added explicitly.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
