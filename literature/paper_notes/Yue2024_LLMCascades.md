# Paper Notes — Large Language Model Cascades with Mixture of Thought Representations for Cost-Efficient Reasoning

**Authors:** Yue et al.  
**Year / Venue:** 2024 / ICLR  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.iclr.cc/paper_files/paper/2024/hash/5de11e930c1bbfda5d4fc9d2b0924032-Abstract-Conference.html  
**Stable source:** https://arxiv.org/abs/2310.03094  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Use consistency signals to decide whether reasoning should escalate to stronger models.

## Setting / Data
Reasoning tasks in cascaded LLM inference.

## Method
Mixture-of-thought representations and consistency signals for cascade decisions.

## Evaluation
Reasoning accuracy, model usage, inference cost.

## Key Finding
Post-generation signals can improve cost-efficient cascade decisions.

## Limitations / Conflicting Evidence
Escalation is not decomposed into repair and independent regeneration with separate calibrated residual risks.

## Relevance to TRACER
Evidence that output-derived signals are valuable after generation.

## Gap Evidence
TRACER generalises post-generation escalation into distinct action-conditional risks.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
