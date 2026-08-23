# Paper Notes — Conformal Risk Control

**Authors:** Anastasios N. Angelopoulos; Stephen Bates; Adam Fisch; Lihua Lei; Tal Schuster  
**Year / Venue:** 2024 / ICLR  
**Peer-reviewed:** Yes  
**Verification:** https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html  
**Stable source:** https://openreview.net/forum?id=33XGfHLtZg  
**TRACER-24 status:** Audit summary prepared; detailed full-text read can add exact table-level numbers if needed for the proposal/thesis.

## Problem
Control expected monotone losses with finite-sample guarantees.

## Setting / Data
General predictive systems; examples include NLP.

## Method
Extends conformal prediction to select a parameter controlling expected risk.

## Evaluation
Expected risk relative to user-specified level; finite-sample guarantee.

## Key Finding
Provides a general framework for controlling expected risk using calibration data.

## Limitations / Conflicting Evidence
Requires monotone risk-control structure; not a learned tri-action router by itself.

## Relevance to TRACER
Theoretical reference for explicit risk thresholds and calibrated/selective policies.

## Gap Evidence
TRACER learns three residual risks and uses an epsilon policy; formal conformal guarantees are not automatically implied.

## Use in the Research
Use this source only for claims supported by its final archival paper/publisher record. Where this note says the source is a preprint, label that status explicitly and do not use it as the sole support for a core novelty claim.
