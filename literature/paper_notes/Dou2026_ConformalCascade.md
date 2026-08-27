# Conformal Cascade: Distribution-Free Accuracy Guarantees for Multi-Tier LLM Inference

## Bibliographic status
- **Authors:** Yifan Dou, Shikan Fang, Shibo Li
- **Year:** 2026
- **Status:** arXiv preprint; not treated as peer-reviewed in the TRACER evidence base as of 2026-08-27
- **Stable URL:** https://arxiv.org/abs/2607.25018

## Problem
Conventional LLM cascades commonly use confidence thresholds to accept a cheaper model's answer or defer to a stronger tier, but those confidence scores can be miscalibrated and the threshold can be brittle across model pairs and domains.

## Method
Conformal Cascade uses the size of a calibrated conformal prediction set as the decision rule:
- accept when the set collapses to a single candidate answer;
- otherwise defer to the next model tier.

The paper states finite-sample, distribution-free accuracy guarantees under its formulation.

## Reported evaluation
The preprint reports evaluation across multiple-choice benchmarks and several open-weight model families, comparing cascade acceptance/cost and accuracy behaviour with heuristic calibrated cascades.

## Relevance to TRACER
This work is critical for novelty discipline:
- calibrated acceptance/defer thresholds are not new;
- finite-sample risk/accuracy control for cascades is not something TRACER should claim unless TRACER actually implements and proves such guarantees;
- TRACER's epsilon threshold should be presented as an operational selective-risk policy, not as the novel contribution by itself.

## Difference from TRACER
Conformal Cascade is an **accept-or-defer multi-tier cascade**. It does not, in the reviewed formulation, compare:
1. accepting the existing SLM response;
2. repairing that same response with stronger-model assistance; and
3. independently regenerating a new solution;

using separately calibrated residual-failure estimates for all three actions.

## Novelty caution
Use this paper to explicitly state that TRACER adapts established ideas from calibration/selective risk. The research contribution must remain the **post-response action-conditional tri-action residual-risk formulation**, not calibrated thresholding.
