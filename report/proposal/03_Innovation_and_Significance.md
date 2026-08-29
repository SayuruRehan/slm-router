# 3. Innovation and Significance

**Related Jira:** TRACER-123  
**Status:** Proposal-ready draft; team review remains part of final integration.

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

## 3.5 Stakeholder Impact

The significance of TRACER can be expressed in terms of the stakeholders who would use, evaluate, or be affected by SLM-based systems.

| Stakeholder | Expected impact |
|---|---|
| **AI/ML researchers** | Provides a reproducible formulation and evaluation framework for studying post-response action risk, calibration, repair damage, and tri-action routing. |
| **AI application developers and platform engineers** | Provides evidence on when an SLM response can be accepted and when a stronger model should repair or independently regenerate an answer, helping engineers design more reliability-aware inference pipelines. |
| **Organisations and product owners deploying SLMs** | Provides a risk-first basis for deciding when stronger-model intervention is justified. Cost, token use, and latency remain secondary measures, so efficiency gains are not treated as successful if final correctness worsens. |
| **End users of SLM-enabled applications** | The intended downstream benefit is a lower probability of receiving an incorrect final answer, together with more conservative handling of cases whose estimated risk remains high. |
| **Evaluators and future research teams** | Provides versioned datasets, validators, prompts, risk definitions, and experiment artefacts that can be reused or extended to other models and domains. |

TRACER does not claim that the same impact will automatically generalise to unrestricted conversational applications. The proposal evaluates this significance first in code and numerical-reasoning domains where correctness can be measured objectively.

## 3.6 Expected Research Contributions

If the study succeeds, the expected contributions are:

1. a formal and reproducible definition of ACCEPT/REPAIR/REGENERATE residual-failure risk;
2. a leakage-safe dataset in which all three action outcomes are observed for the same source response;
3. an ACRE model that produces separately calibrated action risks;
4. a risk-controlled routing policy driven by those probabilities;
5. empirical evidence against fixed-action, binary accept-or-escalate, uncalibrated, and oracle baselines;
6. analysis of repair success, repair damage, calibration, risk regret, and cross-SLM transfer; and
7. a reproducible implementation that allows the formulation to be tested beyond the initial code and numerical domains.

A negative result would still be meaningful. If tri-action routing does not outperform simpler baselines, the study can identify whether the limitation comes from weak action separability, poor features, insufficient calibration, action-outcome noise, or limited transfer. The contribution is therefore the **controlled empirical test of the formulation**, not an assumption that the proposed method must win.
