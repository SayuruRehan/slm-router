# Paper Notes — How Can We Know When Language Models Know? On the Calibration of Language Models for Question Answering

**Authors:** Zhengbao Jiang; Jun Araki; Haibo Ding; Graham Neubig  
**Year / Venue:** 2021 / TACL  
**Peer-reviewed:** Yes  
**Verification:** https://aclanthology.org/2021.tacl-1.57/  
**Stable source:** https://doi.org/10.1162/tacl_a_00407  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Determine whether generative LM confidence corresponds to answer correctness.

## Setting / Data
T5, BART and GPT-2 on QA datasets.

## Method
Evaluates and improves LM calibration through fine-tuning and post-hoc modifications.

## Evaluation
Calibration and QA correctness.

## Key Finding
Raw LM probabilities are substantially miscalibrated; calibration methods improve confidence/correctness correspondence.

## Limitations / Conflicting Evidence
Single-answer correctness confidence, not downstream action-conditional risk.

## Relevance to TRACER
Direct language-model evidence that confidence requires calibration.

## Gap Evidence
TRACER calibrates failure probability conditioned on each action, not just the initial answer.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
