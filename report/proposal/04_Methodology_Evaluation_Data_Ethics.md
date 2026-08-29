# 4. Methodology, Evaluation, Data Management, and Ethics

**Related Jira:** TRACER-124  
**Status:** Proposal-ready experimental plan; implementation details remain version-controlled during the study.

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
