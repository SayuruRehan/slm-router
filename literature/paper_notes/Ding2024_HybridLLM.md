# Paper Notes — Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing

**Authors:** Ding et al.  
**Year / Venue:** 2024 / ICLR  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.iclr.cc/paper_files/paper/2024/hash/b47d93c99fa22ac0b377578af0a1f63a-Abstract-Conference.html  
**Stable source:** https://arxiv.org/abs/2404.14618  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Choose between cheaper and stronger LLMs while controlling quality/cost.

## Setting / Data
Query-level model routing before candidate generation.

## Method
Predicts query difficulty/quality to select a weak or strong model.

## Evaluation
Task performance and cost trade-offs.

## Key Finding
Learned query routing can reduce expensive-model usage while maintaining quality.

## Limitations / Conflicting Evidence
Decision is made before seeing the SLM response; cannot use response-specific failure evidence.

## Relevance to TRACER
Strong pre-generation routing baseline.

## Gap Evidence
TRACER conditions risk on the actual initial response and estimates three action outcomes.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
