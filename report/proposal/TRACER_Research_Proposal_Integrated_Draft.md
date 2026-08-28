# TRACER: Tri-Action Risk Assessment and Calibration for Execution Routing of Small Language Model Responses

> **Integrated proposal body for TRACER-127.** Official front matter, Individual Contributions, and the signed Declaration of Originality are intentionally handled manually outside this repository draft.

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

## 1.7 Expected Outcomes

Expected project outputs are:

- a versioned action-outcome dataset;
- objective validators and provenance mechanisms;
- a trained, calibrated ACRE model;
- an end-to-end ACCEPT/REPAIR/REGENERATE routing policy;
- comparison against fixed and binary baselines;
- analysis of calibration, false acceptance, risk regret, repair success, and repair damage;
- cross-SLM evidence where feasible; and
- a reproducible implementation and documented experimental methodology.

The project does **not** assume that TRACER will outperform every baseline. A valid outcome may show that action-specific routing helps only under particular task, model, or calibration conditions. The contribution is the formulation, implementation, and controlled empirical evaluation of the tri-action residual-risk approach.

# 2. Background and Literature Review

## 2.1 Small/Strong Model Routing and Cascading

The growing range of language models has made **dynamic model selection** an important research problem. Early and recent routing work generally asks whether a query should be handled by a cheaper/weaker model or passed to a stronger one, often under a cost–quality objective. Hybrid LLM learns a query router that trades model quality against cost (Ding et al. 2024), while FrugalGPT formalises the use of model cascades to reduce inference expenditure without necessarily sacrificing task quality (Chen, Zaharia, and Zou 2024). RouteLLM uses preference data to learn routing decisions between stronger and weaker models and demonstrates that routers can generalise beyond the exact model pair used during training (Ong et al. 2025).

More recent work broadens routing beyond a simple weak-versus-strong decision. Unified Routing and Cascading provides a common theoretical view of routing, cascading, and their combination, emphasising the importance of reliable quality estimators (Dekoninck, Baader, and Vechev 2025). BEST-Route jointly considers model selection and test-time compute by allowing multiple samples from cheaper models when useful (Ding et al. 2025). Confidence Tokens explicitly trains a model to expose confidence signals that support downstream routing and rejection decisions (Chuang et al. 2025). Mixture-of-Thought cascades similarly use response consistency and reasoning representations to decide when a stronger model is necessary (Yue et al. 2024).

These studies establish that modern routing is **not merely binary or static**. They also show that confidence, response quality estimation, and adaptive compute are already active research areas. TRACER therefore does not claim novelty from model routing itself. Its distinction is the **post-response action space and prediction target**: after an SLM has already produced a candidate, TRACER estimates the probability that the final answer will remain wrong under three explicit handling actions rather than primarily estimating query difficulty, model preference, or a generic accept/escalate decision.

## 2.2 Post-Response Routing and Response-Aware Signals

AutoMix is particularly relevant because it decides whether an already generated response should be accepted or whether a stronger model should be involved (Aggarwal et al. 2024). This means that “routing after observing a response” is not sufficient as a novelty claim for TRACER. Likewise, recent response-level cascade work continues to explore how a draft response can be retained, enhanced, or escalated rather than treating inference as a single model-selection decision (Wu et al. 2026, preprint).

The implication for TRACER is that the research gap must be narrower. TRACER treats the same `(task, initial SLM response)` pair as the source instance for all candidate actions and attempts to learn **action-conditional residual failure risk**. The research target is therefore not simply “is this answer trustworthy?” but rather:

- what is the probability of failure if the answer is **ACCEPTED unchanged**;
- what is the probability of failure if a stronger model **REPAIRS the existing answer**; and
- what is the probability of failure if the stronger model **REGENERATES independently**.

This formulation allows cases in which REPAIR and REGENERATE have different expected outcomes, which would be hidden if both were collapsed into one escalation label.

## 2.3 Confidence, Calibration, Selective Prediction, and Risk Control

Reliable routing depends on the quality of the probabilities used for decision-making. Neural networks are often miscalibrated, and post-hoc temperature scaling has been shown to be an effective baseline calibration method (Guo et al. 2017). Language-model confidence is likewise not automatically calibrated: Jiang et al. (2021) show that language-model probabilities can correlate poorly with correctness on question answering and that explicit calibration improves their usefulness. Factual-confidence estimators for modern LLMs can also be unstable under meaning-preserving input variations, reinforcing the need to evaluate confidence quality rather than assume it is reliable (Mahaut et al. 2024).

Selective prediction provides another foundation. SelectiveNet formalises the idea that a model may abstain on uncertain cases and optimises the risk–coverage trade-off directly (Geifman and El-Yaniv 2019). Conformal Risk Control extends risk control by providing finite-sample guarantees for user-specified risk functions under suitable assumptions (Angelopoulos et al. 2024). Selective generation and context-adaptive abstention further demonstrate that generation systems can vary the amount of output retained or abstain depending on estimated uncertainty and risk (Lee et al. 2024; Tayebati et al. 2025). A recent Conformal Cascade preprint applies conformal prediction-set size as an accept/defer rule for multi-tier LLM inference (Dou, Fang, and Li 2026, preprint), further showing that calibrated risk-controlled escalation is itself an established direction.

TRACER **adopts rather than invents** these ideas. Calibration and the `epsilon` threshold are methodological foundations for converting predicted action risks into a selective routing rule. The proposed novelty is that the probabilities being calibrated are **three separate residual-failure risks tied to explicit post-response actions**. TRACER does not claim formal conformal guarantees unless a conformal procedure is implemented and independently validated.

## 2.4 Repair, Self-Correction, and Regeneration

Research on correction shows why REPAIR should not automatically be treated as beneficial. CRITIC demonstrates that external tool feedback can enable an LLM to critique and revise its own outputs across several task types (Gou et al. 2024). However, Huang et al. (2024) show that large language models can fail to improve reasoning through unaided self-correction and may even degrade correct answers. For smaller models, strong-verifier work similarly finds that correction quality depends heavily on verifier strength and the quality of external feedback (Zhang et al. 2024).

These findings motivate two TRACER design choices. First, **REPAIR is modelled as an action with its own residual risk**, rather than being assumed to dominate ACCEPT. Second, the evaluation explicitly measures **repair success** and **repair damage**. A separate REGENERATE action is retained because an independent solution can avoid anchoring on the original response, while also discarding useful information that a targeted repair might preserve. Recent test-time work has begun to compare resampling and rerouting as distinct resource-allocation actions, but it does not use TRACER's exact three-head post-response residual-risk formulation (Chen 2026, preprint).

## 2.5 Objective Validation and Benchmark Choice

TRACER requires outcome labels that measure whether the final result is correct after each action. For code, functional execution is a stronger source of evidence than text similarity. DebugBench provides a large debugging benchmark spanning Python, Java, and C++ with diverse bug types and quality-control procedures (Tian et al. 2024). EvalPlus shows that code-generation evaluation can change substantially when benchmark test suites are strengthened, demonstrating the importance of executable validation rather than relying on surface similarity alone (Liu et al. 2023).

For numerical reasoning, FinQA provides questions over financial reports together with structured numerical reasoning annotations and is used as TRACER's primary numerical domain (Chen et al. 2021). This gives the study two distinct correctness settings: executable functional correctness for code and deterministic/normalised numerical correctness for financial reasoning.

The project therefore uses the following evidence precedence when determining correctness:

1. valid executable or deterministic task-specific tests;
2. syntax/compile failure where applicable;
3. exact or normalised reference/AST match as positive supporting evidence;
4. documented manual adjudication only for genuinely unresolved cases;
5. similarity/confidence diagnostics only as secondary evidence.

Infrastructure failure is recorded separately and is not labelled as candidate failure.

## 2.6 Closest-Work Comparison

| Research direction | Representative work | Main decision/target | What is already established | Remaining distinction for TRACER |
|---|---|---|---|---|
| Weak/strong routing | Hybrid LLM; RouteLLM | Choose model from query/features | Learned model selection and cost–quality routing | TRACER operates after an initial SLM response and predicts action-specific residual failure |
| Cascading | FrugalGPT; Mixture-of-Thought; Unified Routing/Cascading | Escalate through models until quality criterion is met | Sequential escalation and quality estimators | TRACER distinguishes REPAIR from independent REGENERATE |
| Response-aware routing | AutoMix | Accept response or involve stronger model | Post-response accept/escalate decision | TRACER has three explicit actions and three risk targets |
| Adaptive compute | BEST-Route | Select model and test-time sample count | Multi-action/test-time compute allocation | TRACER targets final incorrectness under ACCEPT/REPAIR/REGENERATE |
| Confidence routing | Confidence Tokens; factual-confidence estimators | Estimate reliability/confidence | Learned confidence signals for routing/rejection | TRACER calibrates each action's residual-risk probability |
| Selective prediction / abstention | SelectiveNet; Conformal Risk Control; CAP | Control risk/coverage or abstain | Risk thresholds, coverage trade-offs, conformal methods | TRACER applies selective risk control to tri-action post-response routing |
| Correction | CRITIC; self-correction studies; strong verifiers | Revise an existing answer | Repair can help but is conditional on feedback/verifier quality | TRACER predicts when repair is preferable and measures repair damage |
| Resampling/regeneration | Resample or Reroute? | Allocate budget between resampling and rerouting | Distinct test-time remediation choices | TRACER compares context-preserving repair against independent regeneration for the same source response |

## 2.7 Research Gap

The literature supports a deliberately narrow and evidence-bounded gap statement:

> **Within the current TRACER evidence set, including peer-reviewed work on routing, cascading, calibration, selective risk, correction, verification, and adaptive test-time compute, together with closely related 2026 preprints, no reviewed method exactly matches TRACER's proposed formulation: after observing an SLM response, estimate separately calibrated residual probabilities of incorrectness for ACCEPT, context-preserving REPAIR, and independent REGENERATE, then apply an explicit risk threshold using only pre-action information.**

Accordingly, TRACER does not claim to invent routing, calibration, abstention, correction, or regeneration. Its proposed contribution is the **combination and formalisation of a three-action post-response decision space with separately calibrated action-conditional residual-failure estimates and leakage-safe offline supervision**.

# 3. Innovation and Significance

## 3.1 Innovation

TRACER's proposed innovation is an **action-conditional risk formulation for post-response SLM routing**. The project does not treat the initial SLM output as a terminal answer, nor does it reduce the next decision to a single “accept or escalate” label. Instead, for one `(task, initial SLM response)` pair, TRACER explicitly represents three possible response-handling actions:

- **ACCEPT** — return the existing SLM response unchanged;
- **REPAIR** — give the existing response to a stronger model and instruct it to correct that response; and
- **REGENERATE** — ask the stronger model to solve the original task independently without using the SLM answer as repair context.

For each action `a`, TRACER defines the target:

`R_a(x, y) = P(F_a = 1 | Z(x, y))`

where `F_a = 1` means that the final response after action `a` is incorrect and `Z(x, y)` contains only information available **before the selected action is executed**. ACRE therefore predicts `R_ACCEPT`, `R_REPAIR`, and `R_REGENERATE`.

The proposed contribution has five linked elements:

1. **Three explicit post-response actions.** REPAIR and REGENERATE are treated as different decisions rather than one generic escalation.
2. **Action-conditional residual-failure targets.** ACRE predicts the probability of remaining incorrect after each action, not just the confidence of the initial answer.
3. **Separate probability calibration.** Each action head is calibrated so the predicted residual risks can be interpreted and compared on a common probabilistic scale.
4. **Risk-controlled routing.** ACCEPT is permitted only when `R_ACCEPT <= epsilon`; otherwise the lower predicted risk of REPAIR and REGENERATE is selected. Cases where all remediation risks remain above tolerance can be recorded as unresolved/abstention for analysis.
5. **Leakage-safe full-information supervision.** All three action outcomes may be generated and labelled offline for training, but gold answers, reference solutions, downstream action outcomes, and post-action evidence are prohibited from ACRE's inference-time feature vector.

This combination is designed to answer a different question from conventional routing: not “which model is best for this query?” but **“given the answer we already have, which available action is least likely to leave the final answer wrong?”**

## 3.2 What TRACER Does Not Claim as Novel

The literature review shows that the following concepts are established and are used by TRACER as foundations rather than claimed inventions:

- weak/strong model routing and cascading (Ding et al. 2024; Chen, Zaharia, and Zou 2024; Ong et al. 2025);
- post-response accept/escalate routing (Aggarwal et al. 2024);
- confidence estimation and learned quality signals (Chuang et al. 2025; Mahaut et al. 2024);
- calibration, including temperature scaling (Guo et al. 2017; Jiang et al. 2021);
- selective prediction, rejection, and risk/coverage control (Geifman and El-Yaniv 2019; Angelopoulos et al. 2024);
- response correction and verifier-assisted refinement (Gou et al. 2024; Zhang et al. 2024);
- regeneration/resampling and adaptive test-time compute (Ding et al. 2025; Chen 2026, preprint).

Keeping these boundaries explicit reduces the risk of overstating novelty and makes the final contribution testable.

## 3.3 Scientific Significance

The main scientific value of TRACER is that it turns post-response handling into a **comparative probabilistic decision problem**. This enables several questions that are difficult to study with a single confidence score:

- whether the risk of ACCEPT can be estimated independently of the risk of REPAIR;
- whether REPAIR and REGENERATE succeed on different subsets of cases;
- whether calibration improves action choice rather than merely producing better-looking probability estimates;
- how much headroom exists between learned routing and an offline oracle that sees all action outcomes;
- whether the learned risks transfer from one SLM to another; and
- which signals contribute most to action-specific risk through feature and calibration ablations.

The framework also creates a direct way to measure **repair damage**. Prior correction research shows that revision can fail or degrade correct outputs (Huang et al. 2024), so a reliable system should not assume that intervention is automatically beneficial. TRACER's action-outcome data makes this phenomenon measurable.

## 3.4 Practical Significance

SLMs are attractive where local deployment, hardware limits, inference cost, or response time make stronger models undesirable as the default. Their practical limitation is that a plausible-looking answer may still be wrong. A routing system that can identify low-risk answers while escalating risky cases has the potential to preserve some of the deployment advantages of an SLM without accepting its errors indiscriminately.

TRACER is particularly relevant to systems in which:

- the SLM can generate a useful first attempt cheaply;
- a stronger model is available but should not be invoked for every request;
- final correctness is more important than minimising model calls; and
- objective or high-quality validation evidence is available during offline training/evaluation.

The project remains **risk-focused**. Strong-model call rate, token usage, latency, and API cost are measured as descriptive engineering outcomes, not as the primary optimisation objective. This prevents cost savings from being mistaken for success if final correctness worsens.

## 3.5 Expected Research Contributions

If the study succeeds, the expected contributions are:

1. a formal and reproducible definition of ACCEPT/REPAIR/REGENERATE residual-failure risk;
2. a leakage-safe dataset in which all three action outcomes are observed for the same source response;
3. an ACRE model that produces separately calibrated action risks;
4. a risk-controlled routing policy driven by those probabilities;
5. empirical evidence against fixed-action, binary accept-or-escalate, uncalibrated, and oracle baselines;
6. analysis of repair success, repair damage, calibration, risk regret, and cross-SLM transfer; and
7. a reproducible implementation that allows the formulation to be tested beyond the initial code and numerical domains.

A negative result would still be meaningful. If tri-action routing does not outperform simpler baselines, the study can identify whether the limitation comes from weak action separability, poor features, insufficient calibration, action-outcome noise, or limited transfer. The contribution is therefore the **controlled empirical test of the formulation**, not an assumption that the proposed method must win.

# 4. Methodology, Evaluation, Data Management, and Ethics

## 4.1 Research Design

TRACER uses a controlled empirical machine-learning study. The unit of analysis is one `(task, initial SLM response)` pair. For each source response, the project will observe the outcome of all three actions offline:

- `ACCEPT`: the initial response is returned unchanged;
- `REPAIR`: the stronger model receives the task and initial response and is instructed to correct that response;
- `REGENERATE`: the stronger model receives the original task but not the SLM response and produces an independent answer.

Each resulting final answer is evaluated under the relevant objective correctness protocol, producing action-specific binary failure labels:

`F_a = 1` if the final response after action `a` is incorrect; otherwise `F_a = 0`.

The primary modelling target is therefore:

`R_a(x, y) = P(F_a = 1 | Z(x, y))`

for `a ∈ {ACCEPT, REPAIR, REGENERATE}`, where `Z(x, y)` contains only pre-action information.

The risks are **predictive action-conditional probabilities**, not causal treatment effects.

## 4.2 Planned Models

The primary configuration is:

| Role | Planned model | Purpose |
|---|---|---|
| Primary SLM | Qwen3-4B-Instruct-2507 | Generate the initial response used for the main training/evaluation dataset |
| Cross-SLM | Gemma 3 4B IT | Secondary transfer/generalisation evaluation |
| Stronger model | GPT-4.1 | Execute REPAIR and REGENERATE in the primary study |

Local SLM inference will use Hugging Face/vLLM where practical so log-probability-derived uncertainty signals can be recorded. Any substitution caused by availability, licensing, hardware, or API changes will be versioned and documented rather than silently replaced.

## 4.3 Datasets and Sampling

Two primary task domains are planned.

### Code

- **DebugBench** provides realistic debugging tasks and diverse bug categories (Tian et al. 2024).
- **HumanEval+/MBPP+ through EvalPlus-style execution** provide stronger functional tests for code-generation correctness (Liu et al. 2023).

### Numerical reasoning

- **FinQA** is the primary numerical-reasoning benchmark and contains financial question-answering problems with structured reasoning information (Chen et al. 2021).
- **TAT-QA** remains optional if time and data-processing scope permit; it is not required for the minimum study (Zhu et al. 2021).

The target primary action-outcome dataset is approximately **1,000–1,400 source examples**, with roughly **500–700 examples per domain**. A separate **250–350-example Gemma transfer set** is planned where feasible.

Data is split **before downstream action generation** to prevent response variants from the same source task appearing across train, validation, and test partitions. The planned split is approximately **60% training, 20% validation/calibration, and 20% held-out test**, grouped by source task.

## 4.4 Action-Outcome Generation

For each source task:

1. Generate the initial SLM response using the frozen primary SLM configuration.
2. Store the task identifier, model/version, generation settings, response text, token/log-probability metadata where available, and provenance.
3. Evaluate the ACCEPT outcome.
4. Invoke the stronger model once using the frozen **REPAIR prompt**.
5. Invoke the same stronger-model version once using the frozen **REGENERATE prompt**.
6. Apply the domain-specific objective validator to all three final answers.
7. Store all three labels for offline supervision and evaluation.

The stronger-model prompt, API/model version, generation controls, and retry/error-handling policy will be frozen before the full action-outcome run. Repeated repair loops are outside the primary action definition.

## 4.5 Correctness Validation

### Code validation

Executable tests are the preferred evidence for functional correctness. Generated code is executed inside an isolated Docker sandbox. The current PoC configuration uses a `python:3.11-slim` image with:

- network disabled;
- read-only root/workspace where possible;
- Linux capabilities dropped;
- `no-new-privileges`;
- bounded memory, CPU, process count, and execution time;
- isolated Python execution; and
- infrastructure failures recorded separately from candidate failures.

The PoC established the following evidence hierarchy, which will be retained unless the final validator protocol explicitly improves it:

1. valid executable tests;
2. syntax/compile failure;
3. normalised reference/AST exact match as positive supporting evidence;
4. documented manual review for unresolved cases;
5. similarity/confidence diagnostics only.

A mismatch from the reference/AST is **not** sufficient evidence that code is wrong; functionally different code may still pass authoritative tests.

### Numerical validation

For FinQA, deterministic numerical-answer checking will normalise representations such as commas, currency/percentage formatting, sign, and tolerated numeric formatting before comparison. Where reasoning traces are available, they are treated as offline validation/supervision evidence and not as inference-time ACRE features.

## 4.6 Pre-Action Feature Vector

ACRE may use only signals available after the initial SLM response exists but **before the selected action is executed**. Candidate feature groups include:

- task/query embedding;
- initial SLM response embedding;
- task and response length/structure features;
- SLM uncertainty features such as token log-probabilities, entropy, minimum/mean confidence, or self-consistency signals when available;
- pre-action syntax/static-analysis signals that do not rely on hidden tests or gold answers;
- task/domain indicators;
- deterministic metadata frozen before training.

Forbidden inference-time inputs include:

- gold answers;
- benchmark reference solutions;
- final correctness labels;
- REPAIR or REGENERATE outputs/outcomes;
- executable hidden-test outcomes unavailable before routing;
- any feature computed after the selected action executes.

This leakage constraint is enforced both in the feature schema and in experiment review.

## 4.7 ACRE Architecture

The planned primary ACRE model is a shared multi-head neural estimator:

`Input features`
→ `Dense(256) + ReLU`
→ `Dropout(0.2)`
→ `Dense(128) + ReLU`
→ three sigmoid heads:

- `R_ACCEPT`
- `R_REPAIR`
- `R_REGENERATE`

Each head predicts the probability that the final answer will be incorrect after that action. The training objective is the sum/mean of binary cross-entropy losses for the three observed action outcomes. Because all three outcomes are observed offline for each training instance, every source example can supervise all three heads.

Simpler candidate families (for example logistic/linear baselines and tree-based models where suitable) may be compared during model selection so the final architecture is not chosen solely because it is more complex.

## 4.8 Probability Calibration

Uncalibrated neural probabilities can be systematically over- or under-confident (Guo et al. 2017), and language-model confidence is also known to require calibration (Jiang et al. 2021). TRACER therefore calibrates each action head separately on validation/calibration data.

The primary method is **temperature scaling** applied independently to the ACCEPT, REPAIR, and REGENERATE logits. Calibration quality will be assessed using:

- Brier score;
- Expected Calibration Error (ECE);
- reliability diagrams; and
- calibration slope/intercept where useful.

The uncalibrated ACRE output remains a required ablation/baseline.

## 4.9 Risk-Controlled Routing Policy

At inference time:

1. Estimate calibrated `R_ACCEPT`, `R_REPAIR`, and `R_REGENERATE`.
2. If `R_ACCEPT <= epsilon`, select **ACCEPT**.
3. Otherwise select the lower predicted risk between **REPAIR** and **REGENERATE**.
4. If both remediation risks remain above the same acceptable risk tolerance, record the case as unresolved/optional abstention for analysis.

The unresolved state is **not a fourth learned action**.

`epsilon` will be selected using validation/calibration data and will not be tuned on the held-out test set. Sensitivity analysis will report how final error, false acceptance, strong-model usage, and coverage change across reasonable threshold values.

## 4.10 Baselines and Ablations

Minimum baselines:

1. Always ACCEPT.
2. Always REPAIR.
3. Always REGENERATE.
4. Binary accept-or-escalate.
5. A confidence-threshold/cascade-style baseline where feasible.
6. Uncalibrated ACRE.
7. Calibrated ACRE + `epsilon` policy.
8. Offline oracle action selection for analysis only.

Planned ablations include:

- tri-action vs collapsed binary action space;
- calibrated vs uncalibrated probabilities;
- removal of uncertainty features;
- removal of validator/static-analysis features;
- task-only vs task-plus-response representations;
- primary-SLM vs cross-SLM transfer.

## 4.11 Evaluation Metrics

### Primary outcome

**Final incorrect-response rate** on the held-out test set.

This is the percentage of source tasks whose final routed output is objectively incorrect after the selected action.

### Reliability

- false acceptance rate;
- selective risk at `epsilon`;
- coverage/abstention rate where the unresolved analysis is enabled.

### Calibration

- Brier score;
- ECE;
- reliability curves.

### Routing quality

- agreement with the offline oracle action;
- risk regret relative to oracle action selection;
- per-action confusion/selection distribution;
- oracle headroom.

### Action behaviour

- REPAIR success rate;
- REPAIR damage rate;
- REGENERATE success rate;
- cases where REPAIR and REGENERATE disagree.

### Secondary engineering measures

- strong-model call rate;
- token use;
- latency;
- estimated/API cost where available.

These are descriptive and do not replace final incorrect-response rate as the primary outcome.

## 4.12 Statistical Analysis

Because routing policies are evaluated on the same held-out source tasks, comparisons are paired. The final report will include:

- bootstrap 95% confidence intervals for final incorrect-response rate and key derived metrics;
- paired significance testing for primary-policy error differences where sample size and assumptions permit (for example McNemar's test for paired binary correctness);
- per-domain results for code and numerical reasoning;
- calibration confidence intervals or bootstrap variability where appropriate;
- threshold-sensitivity curves;
- cross-SLM results reported separately rather than pooled into the primary result.

No claim of statistical significance will be made without the corresponding test and sample evidence.

## 4.13 Data Management and Reproducibility

The repository will version:

- dataset/source manifests and checksums;
- train/validation/test assignments;
- prompts and prompt versions;
- model identifiers and API versions;
- generation settings and random seeds where supported;
- raw and normalised outputs;
- validator versions and sandbox configuration;
- action labels and evidence;
- feature schema;
- trained model configuration;
- calibration parameters;
- evaluation outputs and summary tables.

Generated artefacts are stored using stable IDs that link each action outcome back to the source task. Secrets such as API keys are never committed. Large or licensed datasets are referenced through manifests/provenance rather than redistributed when licences prohibit it.

Git/GitHub provides source and experiment-version control, while Jira tracks the research backlog, decisions, review gates, and one-week sprint plan.

## 4.14 Ethics, Privacy, and Safety

The proposed study uses public research benchmarks and model-generated responses and is not designed to collect personal or sensitive participant data. Nevertheless, the project addresses several ethical and operational risks.

**Generated code safety.** Model-generated code may be malicious, accidental, or resource-intensive. It is executed only inside a constrained sandbox with disabled networking and strict resource limits. The sandbox reduces risk but is not treated as a perfect security boundary.

**Data privacy.** Only benchmark content required by the study is sent to external APIs. API keys are stored outside the repository. The team will avoid uploading private university, company, customer, or personally identifiable data.

**Model/API transparency.** External model versions can change. Every experiment records the reported model/version and date so API drift is visible.

**Annotation transparency.** Any AI-assisted manual adjudication used during exploratory PoC work is disclosed as AI-assisted and is not represented as independent human inter-rater evaluation. The final study prioritises objective validators; where human review is necessary, reviewer identity/type and the adjudication protocol will be recorded accurately.

**Research integrity.** Gold/reference answers and downstream action outcomes are used only for offline supervision and evaluation. They are prohibited from inference-time features. Negative or null results will be retained and reported rather than removed to improve headline performance.

## 4.15 Planned Tools and Technologies

The planned implementation stack is:

- **Python 3** for experiment orchestration, preprocessing, validation, modelling, and evaluation;
- **PyTorch** for the ACRE neural estimator;
- **Hugging Face Transformers** and **vLLM** for local SLM inference where supported;
- **scikit-learn / NumPy / pandas** for calibration baselines, preprocessing, statistical utilities, and analysis;
- **Docker** for sandboxed execution of generated code;
- **OpenAI API** for GPT-4.1 REPAIR and REGENERATE calls;
- **Git and GitHub** for version control, pull requests, experiment artefacts, and reproducibility records; and
- **Jira** for backlog management, sprint tracking, acceptance criteria, dependencies, and review gates.

Exact package versions will be frozen in the experiment environment before the primary full-scale runs.

## 4.16 Threats to Validity

Key threats include:

- **Dataset representativeness:** DebugBench/FinQA may not generalise to unrestricted language tasks.
- **Action dependence:** REPAIR and REGENERATE performance depends on the selected stronger model and prompt.
- **Validator error:** tests may be incomplete, and numerical normalisation may miss equivalent answers.
- **Model drift:** hosted models can change during the study.
- **Feature availability:** log-probability signals may differ across inference backends.
- **Class imbalance:** some actions may succeed or fail much more often than others.
- **Transfer shift:** a model trained primarily on Qwen responses may not retain calibration on Gemma responses.
- **Limited sample size:** statistical power may constrain fine-grained subgroup conclusions.

These threats are mitigated through versioning, grouped splits, objective validation, baseline/ablation studies, transfer evaluation, and transparent reporting.

# 5. Project Management Plan

## 5.1 Delivery Approach

TRACER is managed using an **Agile Scrum-style process with one-week sprints**. Jira is the official backlog and work-tracking system, while GitHub is used for source control, pull requests, experiment artefacts, and research documentation.

The project uses the following working practices:

- epics represent major research capabilities/work packages;
- user stories/features/tasks break epics into verifiable deliverables;
- subtasks are used for small implementation or review activities;
- work is linked to the relevant Jira key in branches/commits/PRs where practical;
- research decisions and experiment configurations are versioned rather than kept only in chat or meeting notes;
- work requiring independent review is not marked complete until the review gate is satisfied;
- one-week sprint reviews are used to compare planned and completed work and adjust the next sprint.

## 5.2 Current Major Work Packages and Milestones

The timeline is aligned to the current Jira epic due dates.

| Work package | Jira | Target milestone | Measurable exit condition |
|---|---|---:|---|
| Literature study and research definition | TRACER-8 | **3 Sep 2026** | Evidence matrix, closest-work gap, research question/definitions, verified reference set |
| Research proposal | TRACER-119 | **3 Sep 2026** | Proposal sections integrated and ready for submission review |
| Data and validators | TRACER-19 | **6 Sep 2026** | Versioned dataset manifests, provenance, objective validators, review protocol |
| Action-outcome generation | TRACER-20 | **20 Sep 2026** | Frozen ACCEPT/REPAIR/REGENERATE executors and labelled action-outcome dataset |
| ACRE model and calibration | TRACER-21 | **4 Oct 2026** | Leakage-safe feature pipeline, trained action-risk model, calibrated heads |
| Routing and end-to-end integration | TRACER-75 | **11 Oct 2026** | `epsilon` policy and all action executors integrated with repeatable evaluation runner |
| Evaluation and robustness | TRACER-22 | **18 Oct 2026** | Held-out primary evaluation, baseline comparison, ablations, robustness/statistical analysis |
| Governance and living documentation | TRACER-10 | **25 Oct 2026** | Decision log, experiment registry, risk register, runbook and governance records current |
| Thesis and final presentation | TRACER-23 | **25 Oct 2026** | Final research narrative, figures/tables, thesis/presentation artefacts ready for final academic review |

## 5.3 One-Week Sprint Plan

| Sprint | Dates | Primary focus | Target output |
|---|---|---|---|
| 1 | 3–9 Aug | Project/repository setup, initial literature and PoC framing | Backlog, repository structure, early experiments |
| 2 | 10–16 Aug | Baseline model experimentation | Shared Qwen/Gemma experiment pipeline and initial evidence |
| 3 | 17–23 Aug | Validator hardening and correctness pilot | Docker validator improvements, execution pilot, correctness hierarchy |
| 4 | 24–30 Aug | Literature gap + proposal drafting | Evidence matrix, closest-work comparison, proposal Sections 1–3 |
| 5 | 31 Aug–6 Sep | Proposal integration + data/validator freeze | Proposal submission candidate; dataset/validator v1 |
| 6 | 7–13 Sep | Action executors and prompt contracts | ACCEPT/REPAIR/REGENERATE implementation + pilot |
| 7 | 14–20 Sep | Full action-outcome generation | Versioned three-action dataset v1 |
| 8 | 21–27 Sep | Feature pipeline and ACRE training | Leakage-safe feature dataset + candidate models |
| 9 | 28 Sep–4 Oct | Calibration and model selection | Final ACRE model + calibrated action-risk heads |
| 10 | 5–11 Oct | Routing policy and integration | End-to-end TRACER runner + baseline policies |
| 11 | 12–18 Oct | Held-out evaluation and robustness | Primary results, calibration, ablations, transfer analysis |
| 12 | 19–25 Oct | Thesis/final presentation and governance close-out | Final technical narrative, reproducibility package, presentation |

## 5.4 Gantt Chart

![Figure 1. TRACER project Gantt chart showing the twelve one-week sprints from 3 August to 25 October 2026.](figures/tracer_project_gantt.png)

**Figure 1.** TRACER project Gantt chart aligned to the current one-week sprint plan and Jira milestone sequence.

The same dates are also provided in tabular form so the schedule remains readable if the figure is reformatted in the official proposal template.

## 5.5 Team Responsibilities

The table below is a **working delivery allocation**, not a contribution-percentage statement. The team may rebalance workload in Jira as implementation progresses.

| Team member | Planned primary responsibilities | Shared/review responsibilities |
|---|---|---|
| **Sayuru Rehan Bopitiya** | Technical/project coordination; experiment infrastructure; ACRE modelling/calibration; routing integration; evaluation/statistical analysis; repository/Jira coordination | Literature/methodology review; proposal/thesis integration; PR review |
| **Lithma Perera** | Literature/research-definition coordination; methodology/data-design review; validator/data-quality review; documentation quality | Experiment review; proposal/thesis writing; PR review |
| **Sulakna Weerasinghe** | Dataset provenance/QA support; benchmark/test verification; experiment/result checking; research documentation support | Literature review; evaluation QA; proposal/thesis review |

### Team-level responsibilities

All three members share responsibility for:

- approving the final research definition and gap statement;
- reviewing dataset/validator choices;
- reviewing high-impact experiment changes;
- checking proposal/thesis claims against evidence;
- reviewing pull requests for research-critical changes;
- ensuring results are reproducible and honestly reported.

## 5.6 Quality and Change Control

### Definition of Ready

A research/backlog item is ready when:

- the research or implementation objective is clear;
- inputs/dependencies are available;
- expected artefact/output is identified;
- acceptance criteria are testable;
- known risks or data dependencies are recorded.

### Definition of Done

A research/backlog item is done when:

- required code/data/documentation is versioned;
- acceptance criteria are demonstrably met;
- tests/checks pass where applicable;
- experiment configuration and evidence are recorded;
- required peer/team review is complete;
- Jira links to the relevant evidence or repository artefact.

### Change control

Changes to the frozen research question, action definitions, model roles, dataset split, action prompts, validator rules, feature schema, calibration policy, or held-out evaluation procedure must be recorded before the corresponding full experiment is rerun. This prevents post-hoc modification of the experiment solely because of observed results.

## 5.7 Risk Management Summary

| Risk | Likelihood | Impact | Owner | Mitigation |
|---|---|---|---|---|
| Dataset/validator labels are noisy or incomplete | Medium | High | Lithma + Sulakna | Prefer objective tests; independently verify fixtures; separate unresolved cases |
| Generated code is unsafe to execute | Medium | High | Sayuru | Docker isolation, network disabled, resource caps, read-only execution |
| Strong-model API/version changes | Medium | High | Sayuru | Record exact model/date/config; freeze full-run window; version outputs |
| ACRE overfits or is poorly calibrated | Medium | High | Sayuru | Grouped splits, simple baselines, calibration set, ablations, bootstrap analysis |
| Gold/reference leakage enters ACRE features | Low–Medium | Critical | Entire team | Explicit forbidden-feature schema and review gate |
| REPAIR/REGENERATE prompts create unfair comparison | Medium | High | Entire team | Freeze prompts and same strong-model version/settings |
| Sample size is insufficient for subgroup claims | Medium | Medium–High | Entire team | Predefine primary metric; aggregate only defensible subgroups; report CIs |
| Schedule slips because action generation/API calls are slow | Medium | High | Sayuru | Pilot throughput early; checkpoint outputs; prioritise mandatory datasets |
| Team review/dependency bottlenecks | Medium | Medium | Entire team | Weekly sprint planning, explicit reviewers, small PRs, Jira review gates |
| Literature novelty claim becomes outdated | Low–Medium | Medium | Lithma | Evidence-bounded wording; final literature check before submission/thesis |

A more detailed risk register is provided in `Appendix_B_Detailed_Risk_Register.md`.

## 5.8 Communication and Reporting

- **Weekly sprint planning/review:** confirm completed work, blockers, and next sprint goal.
- **Jira:** source of truth for backlog status, dependencies, due dates, and acceptance criteria.
- **GitHub:** source of truth for versioned implementation, experiment artefacts, literature notes, and proposal drafts.
- **Pull requests:** preferred review mechanism for research-critical repository changes.
- **Decision log/experiment registry:** used for changes that affect experimental interpretation.

This structure gives the project a traceable path from research question to implementation, evaluation, and final reporting.

# 6. References — Chicago Author-Date

Aggarwal, Pranjal, Aman Madaan, Ankit Anand, Srividya Pranavi Potharaju, Swaroop Mishra, Pei Zhou, Aditya Gupta, et al. 2024. “AutoMix: Automatically Mixing Language Models.” *Advances in Neural Information Processing Systems* 37. https://proceedings.neurips.cc/paper_files/paper/2024/hash/ecda225cb187b40ea8edc1f46b03ffda-Abstract-Conference.html.

Angelopoulos, Anastasios N., Stephen Bates, Adam Fisch, Lihua Lei, and Tal Schuster. 2024. “Conformal Risk Control.” In *International Conference on Learning Representations*. https://openreview.net/forum?id=33XGfHLtZg.

Chen, Lingjiao, Matei Zaharia, and James Zou. 2024. “FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance.” *Transactions on Machine Learning Research*. https://openreview.net/forum?id=cSimKw5p6R.

Chen, Teng-Ruei. 2026. “Resample or Reroute? Budget-Aware Test-Time Model Selection for Large Language Models.” arXiv preprint arXiv:2607.08665. https://arxiv.org/abs/2607.08665.

Chen, Zhiyu, Wenhu Chen, Charese Smiley, Sameena Shah, Iana Borova, Dylan Langdon, Reema Moussa, et al. 2021. “FinQA: A Dataset of Numerical Reasoning over Financial Data.” In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*, 3697–3711. Association for Computational Linguistics. https://doi.org/10.18653/v1/2021.emnlp-main.300.

Chuang, Yu-Neng, Prathusha Kameswara Sarma, Parikshit Gopalan, John Boccio, Sara Bolouki, Xia Hu, and Helen Zhou. 2025. “Learning to Route LLMs with Confidence Tokens.” In *Proceedings of the 42nd International Conference on Machine Learning*, 10859–10878. PMLR 267. https://proceedings.mlr.press/v267/chuang25b.html.

Dekoninck, Jasper, Maximilian Baader, and Martin Vechev. 2025. “A Unified Approach to Routing and Cascading for LLMs.” In *Proceedings of the 42nd International Conference on Machine Learning*, 12987–13010. PMLR 267. https://proceedings.mlr.press/v267/dekoninck25a.html.

Ding, Dujian, Ankur Mallick, Chi Wang, Robert Sim, Subhabrata Mukherjee, Victor Rühle, Laks V. S. Lakshmanan, and Ahmed H. Awadallah. 2024. “Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing.” In *International Conference on Learning Representations*. https://proceedings.iclr.cc/paper_files/paper/2024/hash/b47d93c99fa22ac0b377578af0a1f63a-Abstract-Conference.html.

Ding, Dujian, Ankur Mallick, Shaokun Zhang, Chi Wang, Daniel Madrigal, Mirian Del Carmen Hipolito Garcia, Menglin Xia, Laks V. S. Lakshmanan, Qingyun Wu, and Victor Rühle. 2025. “BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute.” In *Proceedings of the 42nd International Conference on Machine Learning*, 13870–13884. PMLR 267. https://proceedings.mlr.press/v267/ding25d.html.

Dou, Yifan, Shikan Fang, and Shibo Li. 2026. “Conformal Cascade: Distribution-Free Accuracy Guarantees for Multi-Tier LLM Inference.” arXiv preprint arXiv:2607.25018. https://arxiv.org/abs/2607.25018.

Geifman, Yonatan, and Ran El-Yaniv. 2019. “SelectiveNet: A Deep Neural Network with an Integrated Reject Option.” In *Proceedings of the 36th International Conference on Machine Learning*, 2151–2159. PMLR 97. https://proceedings.mlr.press/v97/geifman19a.html.

Gou, Zhibin, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Nan Duan, and Weizhu Chen. 2024. “CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing.” In *International Conference on Learning Representations*. https://proceedings.iclr.cc/paper_files/paper/2024/hash/fef126561bbf9d4467dbb8d27334b8fe-Abstract-Conference.html.

Guo, Chuan, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. 2017. “On Calibration of Modern Neural Networks.” In *Proceedings of the 34th International Conference on Machine Learning*, 1321–1330. PMLR 70. https://proceedings.mlr.press/v70/guo17a.html.

Huang, Jie, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou. 2024. “Large Language Models Cannot Self-Correct Reasoning Yet.” In *International Conference on Learning Representations*. https://openreview.net/forum?id=IkmD3fKBPQ.

Jiang, Zhengbao, Jun Araki, Haibo Ding, and Graham Neubig. 2021. “How Can We Know When Language Models Know? On the Calibration of Language Models for Question Answering.” *Transactions of the Association for Computational Linguistics* 9: 962–977. https://doi.org/10.1162/tacl_a_00407.

Lee, Minjae, Kyungmin Kim, Taesoo Kim, and Sangdon Park. 2024. “Selective Generation for Controllable Language Models.” *Advances in Neural Information Processing Systems* 37: 50494–50527. https://doi.org/10.52202/079017-1600.

Liu, Jiawei, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. 2023. “Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation.” *Advances in Neural Information Processing Systems* 36. https://proceedings.neurips.cc/paper_files/paper/2023/hash/43e9d647ccd3e4b7b5baab53f0368686-Abstract.html.

Mahaut, Matéo, Laura Aina, Paula Czarnowska, Momchil Hardalov, Thomas Müller, and Lluis Marquez. 2024. “Factual Confidence of LLMs: On Reliability and Robustness of Current Estimators.” In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 4554–4570. Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.acl-long.250.

Ong, Isaac, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M. Waleed Kadous, and Ion Stoica. 2025. “RouteLLM: Learning to Route LLMs with Preference Data.” In *International Conference on Learning Representations*. https://openreview.net/forum?id=8sSqNntaMr.

Tayebati, Sina, Divake Kumar, Nastaran Darabi, Dinithi Jayasuriya, Theja Tulabandhula, Ranganath Krishnan, and Amit Ranjan Trivedi. 2025. “CAP: Conformalized Abstention Policies for Context-Adaptive Risk Management for LLMs and VLMs.” In *Proceedings of the 17th Asian Conference on Machine Learning*, 926–941. PMLR 304. https://proceedings.mlr.press/v304/tayebati26a.html.

Tian, Runchu, Yining Ye, Yujia Qin, Xin Cong, Yankai Lin, Yinxu Pan, Yesai Wu, et al. 2024. “DebugBench: Evaluating Debugging Capability of Large Language Models.” In *Findings of the Association for Computational Linguistics: ACL 2024*, 4173–4198. Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.findings-acl.247.

Wu, Haifeng, Srinivasan Manoharan, Fangbo Tu, Junhua Zhao, and Jian Wan. 2026. “RLM-Cascade: Response-Level Speculative Decoding for Cost-Efficient LLM API Serving.” arXiv preprint arXiv:2606.22840. https://arxiv.org/abs/2606.22840.

Yue, Murong, Jie Zhao, Min Zhang, Liang Du, and Ziyu Yao. 2024. “Large Language Model Cascades with Mixture of Thought Representations for Cost-Efficient Reasoning.” In *International Conference on Learning Representations*. https://proceedings.iclr.cc/paper_files/paper/2024/hash/5de11e930c1bbfda5d4fc9d2b0924032-Abstract-Conference.html.

Zhang, Yunxiang, Muhammad Khalifa, Lajanugen Logeswaran, Jaekyeom Kim, Moontae Lee, Honglak Lee, and Lu Wang. 2024. “Small Language Models Need Strong Verifiers to Self-Correct Reasoning.” In *Findings of the Association for Computational Linguistics: ACL 2024*, 15637–15653. Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.findings-acl.924.

Zhu, Fengbin, Wenqiang Lei, Youcheng Huang, Chao Wang, Shuo Zhang, Jiancheng Lv, Fuli Feng, and Tat-Seng Chua. 2021. “TAT-QA: A Question Answering Benchmark on a Hybrid of Tabular and Textual Content in Finance.” In *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)*, 3277–3287. Association for Computational Linguistics. https://doi.org/10.18653/v1/2021.acl-long.254.

---

## Final reference-use rule

Use Chicago Author-Date consistently:

- one/two authors: `(Geifman and El-Yaniv 2019)`;
- three or more authors: `(Guo et al. 2017)`;
- multiple sources: `(Ding et al. 2024; Ong et al. 2025)`;
- explicitly mark arXiv-only 2026 works as preprints when publication status is relevant.

Only sources cited in the final proposal should remain in the submitted bibliography.