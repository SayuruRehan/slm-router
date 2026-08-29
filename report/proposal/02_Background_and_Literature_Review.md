# 2. Background and Literature Review

**Related Jira:** TRACER-122  
**Status:** Proposal-ready draft; team review remains part of final integration.

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
