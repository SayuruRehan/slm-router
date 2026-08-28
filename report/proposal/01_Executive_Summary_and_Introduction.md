# TRACER Research Proposal — Executive Summary and Introduction

**Related Jira:** TRACER-121  
**Status:** Draft for proposal integration

# Executive Summary

Small language models (SLMs) are attractive for practical AI systems because they can require fewer computational resources and can be easier to deploy than larger, stronger models. Their usefulness, however, is constrained by the risk of returning incorrect responses. Existing research has studied model routing, cascading, confidence estimation, selective prediction, calibration, verification, and response correction. The current TRACER literature evidence set does not identify a method that exactly matches the proposed post-response formulation in which the residual probability of failure is estimated separately for three response-handling actions: **ACCEPT** the existing SLM response, **REPAIR** that response using a stronger model, or **REGENERATE** an independent solution using the stronger model.

TRACER proposes an **Action-Conditional Risk Estimator (ACRE)** that uses information available before the selected action is executed to estimate `R_ACCEPT`, `R_REPAIR`, and `R_REGENERATE`. The project will construct offline action-outcome data in which all three outcomes are observed for the same initial SLM response and labelled primarily using objective validators. The primary study will focus on code and numerical-reasoning tasks, using Qwen3-4B-Instruct-2507 as the primary SLM, Gemma 3 4B IT for cross-SLM evaluation, and GPT-4.1 as the stronger model for REPAIR and REGENERATE. A calibrated risk-controlled policy will ACCEPT a response when its predicted residual risk is within a predefined tolerance; otherwise it will select the lower-risk remediation action.

The primary evaluation outcome will be the **final incorrect-response rate**, compared against fixed-action and binary accept-or-escalate baselines. Secondary evaluation will examine false acceptance, calibration, selective risk, action-selection quality, repair success and repair damage, and cross-SLM transfer. Cost, token use, and latency will be recorded as descriptive engineering measures rather than treated as the primary optimisation objective. The expected contribution is empirical evidence on whether calibrated, action-specific post-response risk estimation can improve the reliability of SLM-based systems.

# 1. Introduction

## 1.1 Background and Motivation

Small language models can provide a practical alternative to stronger, resource-intensive language models where deployment cost, computational availability, or responsiveness matters. The central limitation is reliability: an SLM may produce an answer that appears plausible while still being objectively incorrect. A system that always accepts the SLM inherits these errors, while a system that always invokes a stronger model gives up much of the practical value of using the SLM in the first place.

The problem is also more nuanced than deciding whether to accept or escalate. Once an initial response exists, a stronger model can be used in at least two different ways. It can **REPAIR** the existing response by examining and correcting it, or it can **REGENERATE** a new answer independently. These actions need not have the same probability of success. Repair may preserve useful parts of an almost-correct response, but it may remain anchored to an erroneous answer or damage a response that did not require intervention. Independent regeneration avoids that anchoring but discards potentially useful work already performed by the SLM.

TRACER therefore treats response handling as a risk-estimation problem rather than a generic confidence- or cost-routing problem.

## 1.2 Problem Statement

Existing routing, cascading, selective-prediction, calibration, and correction methods provide mechanisms for deciding when to trust a model, defer, escalate, or revise an answer. However, within the current TRACER evidence set, no reviewed method exactly matches the proposed formulation of estimating **separately calibrated residual probabilities of incorrectness** for:

1. **ACCEPT** — return the initial SLM response unchanged;
2. **REPAIR** — use a stronger model to correct the existing SLM response; and
3. **REGENERATE** — use the stronger model to solve the original task independently.

The research problem is therefore:

> After observing an initial SLM response, can a learned and calibrated action-risk estimator identify the response-handling action that is least likely to leave the final answer incorrect?

TRACER is intentionally risk-focused. Cost and latency are secondary descriptive measures rather than the primary optimisation target.

## 1.3 Research Question

> **Can a calibrated machine-learning-based action-risk model reduce the risk of returning incorrect SLM responses by learning to select among acceptance, stronger-model repair, and independent regeneration, compared with binary accept-or-escalate and fixed-action baselines?**

## 1.4 Research Objectives

1. **Construct reproducible action-outcome data** in which ACCEPT, REPAIR, and REGENERATE outcomes are observed for the same initial SLM response.
2. **Train ACRE** to estimate residual failure risk for each action using only pre-action information.
3. **Calibrate the action-specific risk estimates** so predicted probabilities better correspond to observed failure frequencies.
4. **Implement a risk-controlled routing policy** that accepts sufficiently low-risk responses and otherwise selects between REPAIR and REGENERATE.
5. **Compare against meaningful baselines**, including fixed-action policies, binary accept-or-escalate routing, and uncalibrated routing.
6. **Evaluate reliability and generalisation** using correctness, calibration, routing-quality, repair-behaviour, and cross-SLM measures.

## 1.5 Research Hypotheses

**H1:** The calibrated TRACER policy will achieve a lower final incorrect-response rate than binary accept-or-escalate and fixed-action baselines on held-out evaluation data.

- **H2:** Per-action calibration will improve Brier score, Expected Calibration Error (ECE), and reliability relative to uncalibrated ACRE outputs.
- **H3:** Modelling REPAIR and REGENERATE separately will reduce final incorrect responses compared with collapsing both into a single generic escalation action.
- **H4:** REPAIR will show heterogeneous effects: some responses will improve, while others will remain incorrect or be damaged.
- **H5 (secondary):** ACRE will retain useful risk discrimination and calibration when evaluated on a second SLM, although performance may degrade under transfer.

## 1.6 Project Scope

### In scope

- Post-response routing after an initial SLM answer exists.
- ACCEPT, REPAIR, and REGENERATE.
- ACRE action-conditional residual-failure prediction.
- Separate probability calibration for all three action risks.
- A risk threshold `epsilon` for selective acceptance.
- Objective correctness validation wherever available.
- Code tasks using DebugBench and executable EvalPlus-style tasks where appropriate.
- Numerical reasoning using FinQA as the primary numerical domain.
- Qwen3-4B-Instruct-2507 as primary SLM, Gemma 3 4B IT for cross-SLM evaluation, and GPT-4.1 as the planned stronger model.
- Offline generation of all three action outcomes.
- Evaluation against fixed-action, binary-routing, and uncalibrated baselines.

### Out of scope

- Cost/latency as the primary optimisation objective.
- General-purpose unrestricted conversational deployment.
- Formal causal claims about action effects.
- Multi-step autonomous agents or repeated repair loops as the primary action space.
- Gold answers, benchmark references, or downstream action outcomes as inference-time ACRE features.
- Treating unresolved/abstention as a fourth learned action.
- Claiming formal conformal guarantees unless separately implemented and validated.
- Production-scale commercial deployment.

## 1.7 Expected Key Findings / Research Outcomes

Because this is a research proposal, the final empirical findings are not known in advance. The study is designed to determine the following:

1. **Whether action-specific residual risks are learnable:** whether features from the task and initial SLM response contain enough information to distinguish the failure risk of ACCEPT, REPAIR, and REGENERATE.
2. **Whether calibration improves routing reliability:** whether calibrated action-risk probabilities reduce false acceptance and final incorrect-response rate relative to uncalibrated routing.
3. **When REPAIR should be preferred over REGENERATE:** whether targeted correction and independent regeneration succeed on different subsets of cases rather than behaving as interchangeable escalation actions.
4. **How often repair is harmful:** the prevalence of repair damage, where intervention turns an initially correct or recoverable answer into an incorrect final answer.
5. **How close learned routing approaches the offline oracle:** the residual gap between ACRE-selected actions and the best action observed offline for each task.
6. **Whether the learned risk estimates transfer across SLMs:** whether discrimination and calibration learned primarily from Qwen responses remain useful on Gemma responses.

A valid research outcome may show improvement only for particular domains, action types, or risk thresholds. The study therefore treats negative or mixed findings as informative rather than assuming TRACER must outperform every baseline.

## 1.8 Research Deliverables

The planned project deliverables are:

- a versioned and reproducible multi-domain source-task manifest and action-outcome dataset;
- objective code and numerical validators with provenance and safety controls;
- frozen ACCEPT, REPAIR, and REGENERATE action contracts and prompts;
- a leakage-safe pre-action feature pipeline;
- a trained ACRE model with separately calibrated `R_ACCEPT`, `R_REPAIR`, and `R_REGENERATE`;
- an end-to-end risk-controlled routing policy using the `epsilon` threshold;
- fixed-action, binary-routing, uncalibrated, calibrated, and oracle baseline implementations;
- a held-out evaluation covering correctness, false acceptance, calibration, risk regret, repair success/damage, and cross-SLM transfer; and
- a reproducible GitHub research implementation together with the thesis, figures, result tables, and final presentation.
