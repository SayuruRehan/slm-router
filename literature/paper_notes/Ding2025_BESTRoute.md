# Paper Notes — BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute

**Authors:** Dujian Ding; Ankur Mallick; Shaokun Zhang; Chi Wang; Daniel Madrigal; Mirian Del Carmen Hipolito Garcia; Menglin Xia; Laks V. S. Lakshmanan; Qingyun Wu; Victor Rühle  
**Year / Venue:** 2025 / ICML  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.mlr.press/v267/ding25d.html  
**Stable source:** https://arxiv.org/abs/2506.22716  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Choose not only a model but also how many samples to draw under quality/cost requirements.

## Setting / Data
Multi-LLM routing with test-time best-of-n sampling.

## Method
Routes by query difficulty and quality thresholds to a model plus response count.

## Evaluation
Quality and inference cost.

## Key Finding
Reports up to 60% cost reduction with less than 1% performance drop.

## Limitations / Conflicting Evidence
Action space is model/sample-count allocation before outcome-specific repair; not calibrated residual failure for ACCEPT/REPAIR/REGENERATE.

## Relevance to TRACER
Important updated closest work showing modern routers are not merely binary.

## Gap Evidence
Forces TRACER to state a narrower post-response action-risk contribution.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
