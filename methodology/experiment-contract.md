# TRACER Experiment Contract

Version: 1.2

## Purpose
This contract makes model and action results comparable. The canonical research definitions are maintained in `methodology/Research_Definition.md`.

## Unit of analysis
The unit is one initial SLM response to a task.

- **ACCEPT:** return the unchanged SLM response.
- **REPAIR:** stronger model corrects the existing SLM response using the frozen repair prompt and only allowed pre-action context.
- **REGENERATE:** stronger model independently solves the original task without receiving the SLM response or repair context.

For action `a`, residual-failure risk is the predictive probability that the final response after `a` is incorrect, conditioned only on allowed pre-action features.

## Required run metadata
- run ID and timestamps;
- experiment/version;
- dataset SHA-256 and manifest;
- stable sample identity;
- prompt version;
- model/provider/runtime version;
- generation controls;
- raw and extracted outputs;
- validator outcome and provenance;
- label source / review requirement;
- latency and token counts;
- runtime context for local runs.

## Correctness evidence hierarchy
1. Valid sandboxed executable/programmatic tests.
2. Syntax/compile failure as definitive negative evidence for executable tasks.
3. Normalized reference/AST exact match as strong positive evidence.
4. Reference/AST mismatch is unresolved, not automatically wrong.
5. Documented review protocol for cases without adequate objective evidence.
6. Similarity/confidence are diagnostics only.

Infrastructure failures must never become candidate failures.

## Inference-leakage rule
Gold/reference answers, benchmark labels, and observed ACCEPT/REPAIR/REGENERATE outcomes are offline supervision/evaluation evidence only. They must not be inference-time ACRE features.

Any validator feature used by ACRE must be computable before the selected action executes and must be explicitly frozen in the protocol.

## Action-outcome comparability
For every source `(task, initial SLM response)`:
- all three actions refer to the same source response;
- REPAIR and REGENERATE use frozen versioned prompts;
- the primary study uses the same stronger-model version for both remediation actions;
- splits are created before downstream action outcomes whenever practical;
- action labels preserve prompt, model, validator and dataset provenance.

## Safe execution
Generated code must run only through the hardened Docker validator when execution is required. Network, filesystem, capability, process, memory, CPU and timeout restrictions must remain enabled.

## PoC note
The existing 20-sample DebugBench work is a PoC/baseline artifact. Objective validators should replace manual review wherever practical in the final dataset.
