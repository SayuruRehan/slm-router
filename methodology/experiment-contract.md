# TRACER Experiment Contract

Version: 1.0

## Purpose

This contract makes model and action results comparable. An experiment is valid only when its dataset identity, sample manifest, prompt, model, generation settings, validator, and output schema are recorded.

## Unit of analysis

The unit is an initial SLM response to a task. Later action experiments will attach three potential outcomes to that same initial response:

- ACCEPT outcome: correctness of the unchanged SLM response.
- REPAIR outcome: correctness after a stronger model receives the original response plus external validator evidence.
- REGENERATE outcome: correctness after a stronger model receives only the original task and solves it from scratch.

The action-specific risk target is the probability that the chosen action's final response still fails the objective validator.

## Required run metadata

- Unique run ID and timestamps.
- Experiment name and semantic version.
- Dataset SHA-256 and manifest path.
- Stable dataset index and slug per sample.
- Prompt version.
- Model name, model digest when available, and Ollama version.
- Temperature, seed, token limit, and other generation options.
- Raw response and extracted code.
- Validator outcome, label source, and manual-review requirement.
- Latency and token counts.

## Label hierarchy

1. Sandboxed execution tests are the primary correctness source when available.
2. Empty, unparsable, or unchanged code provides definitive failure evidence.
3. Reference AST equality provides positive reference evidence.
4. A parsing, changed response with a different AST is unresolved—not automatically wrong.
5. Human review may resolve a record, but reviewer identity and protocol must be logged before using that label for training.

## Safe execution requirements

Generated code must not run directly on the host. The included Docker backend uses:

- No network access.
- Read-only root filesystem and read-only source mount.
- Dropped Linux capabilities and no-new-privileges.
- CPU, memory, process, and wall-time limits.
- Ephemeral container removal.

This reduces risk but is not perfect isolation. Keep Docker patched and use a dedicated research environment.

## Baseline comparison rule

Qwen and Gemma baselines must differ only in model identity. They share the same manifest, prompt version, generation controls, and validation implementation.

## Sprint 1 success criteria

- Both configs pass dry-run validation.
- Offline unit tests and lint checks pass.
- Either model can be selected by changing only the configuration path.
- JSON, CSV, and summary files preserve the required metadata.
- Unresolved examples are not counted as incorrect.

