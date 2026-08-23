# Paper Notes — FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

**Authors:** Lingjiao Chen; Matei Zaharia; James Zou  
**Year / Venue:** 2024 / TMLR  
**Peer-reviewed:** Yes  
**Verification:** https://mlanthology.org/tmlr/2024/chen2024tmlr-frugalgpt/  
**Stable source:** https://openreview.net/forum?id=cSimKw5p6R  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Reduce LLM inference cost without sacrificing task quality.

## Setting / Data
Multiple LLM APIs; classification, QA, and reasoning tasks.

## Method
Learns LLM cascades, ordering models and stopping thresholds using quality/cost estimates.

## Evaluation
Task accuracy/performance and inference cost.

## Key Finding
Cascades can retain or improve quality while substantially reducing cost; final TMLR publication is 2024.

## Limitations / Conflicting Evidence
Primarily cost-quality optimisation; does not estimate separate residual failure risk for repair vs independent regeneration after observing an SLM answer.

## Relevance to TRACER
Foundational cascade baseline; supports learned stopping/escalation decisions.

## Gap Evidence
TRACER differs by post-response tri-action risk estimation rather than cascade order/cost optimisation.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
