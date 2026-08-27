# RLM-Cascade: Response-Level Speculative Decoding for Cost-Efficient LLM API Serving

## Bibliographic status
- **Authors:** Haifeng Wu, Srinivasan Manoharan, Fangbo Tu, Junhua Zhao, Jian Wan
- **Year:** 2026
- **Status:** arXiv preprint; not treated as peer-reviewed in the TRACER evidence base as of 2026-08-27
- **Stable URL:** https://arxiv.org/abs/2606.22840

## Problem
RLM-Cascade targets the serving cost of expensive LLM APIs by first obtaining a draft response from a cheaper model and then deciding whether/how a stronger model should participate.

## Method
From the paper abstract, the system operates at **response level** rather than only routing the original query. A fast draft model generates a candidate response and a lightweight complexity router selects a path in which the draft can be used directly, a capable model can be involved, or the response can be enhanced.

## Reported evaluation
The preprint reports a real-world agentic coding workload and a small Code/Math/Instruct benchmark, with cost, latency, draft-use rate, and pass-rate style measures.

## Relevance to TRACER
This is closer to TRACER than query-only routing because a candidate response already exists before the downstream decision. It is therefore important evidence that TRACER **must not** claim that post-response routing or response enhancement is absent from prior work.

## Difference from TRACER
The defensible distinction is narrower:
- TRACER defines **ACCEPT, REPAIR, and independent REGENERATE** as explicit alternative actions.
- ACRE estimates a **separate residual failure probability for each action**.
- Those probabilities are calibrated and used by an explicit risk policy.
- REPAIR is defined as editing/conditioning on the existing SLM response, while REGENERATE solves independently using the stronger model.
- Inference-time ACRE features are restricted to information available **before** the selected action is executed.

RLM-Cascade, based on the currently reviewed preprint description, is primarily an efficiency-oriented response-level cascade and does not provide this exact three-risk formulation.

## Novelty caution
Use this paper in TRACER-25 as an **emerging closest-work challenge**. Do not use it as peer-reviewed evidence, and do not overstate differences beyond what the available paper evidence supports.
