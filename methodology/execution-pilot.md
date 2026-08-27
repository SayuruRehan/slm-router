# TRACER-32 — Five-Sample Execution-Test Pilot

## Purpose
Validate that the chosen correctness evidence can distinguish buggy, correct, and alternative repaired solutions before scaling objective test construction.

## Samples
The fixed five samples are stored in `sample_manifests/tracer32_execution_pilot.json`.

## Candidate categories
For every sample:
1. original buggy code;
2. benchmark reference;
3. Qwen output;
4. Gemma output.

## Sanity gate
The runner aborts if:
- any benchmark reference fails; or
- any original buggy program passes.

## Security
Generated code is run only through `DockerPythonSandbox`. There is deliberately no direct host-execution fallback.

## Jira evidence
- manually reviewed expected results: `results/pilot/tracer32_expected_results.csv`
- real execution evidence after running the script: `results/pilot/tracer32_execution_results.json`
- summary: `results/pilot/tracer32_execution_summary.json`
