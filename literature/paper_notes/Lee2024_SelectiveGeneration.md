# Paper Notes — Selective Generation for Controllable Language Models

**Authors:** Minjae Lee; Kyungmin Kim; Taesoo Kim; Sangdon Park  
**Year / Venue:** 2024 / NeurIPS  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a6815122f533193a022cbc41786c1cc-Abstract-Conference.html  
**Stable source:** https://doi.org/10.52202/079017-1600  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Apply certified selective prediction ideas to free-form language generation.

## Setting / Data
Open/closed-source generative language models with textual-entailment correctness.

## Method
Supervised and semi-supervised selective generation controlling false discovery rate under entailment.

## Evaluation
FDR under entailment and selection efficiency.

## Key Finding
Selective generation can meet desired risk levels with theoretical guarantees using an entailment-based correctness relation.

## Limitations / Conflicting Evidence
Controls selection of generated content rather than choosing repair vs independent regeneration.

## Relevance to TRACER
Direct generative selective-risk precedent; important for avoiding overclaiming novelty.

## Gap Evidence
TRACER's novelty is action-conditional remediation risk, not selective generation itself.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
