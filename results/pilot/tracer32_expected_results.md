# TRACER-32 — Five-Sample Pilot Review Summary

## Fixed pilot
Five DebugBench samples were selected and deterministic tests were prepared. Each fixture compares the original buggy code, benchmark reference, Qwen output, and Gemma output.

## Manually reviewed expected outcomes
| Candidate type | Expected passes / 5 |
|---|---:|
| Buggy | 0 |
| Reference | 5 |
| Qwen | 2 |
| Gemma | 5 |

The fixture design therefore has the desired sanity pattern: every reference is expected to pass and every original buggy program is expected to fail.

## Execution status
The actual Docker executions are **not fabricated in this artifact**. This ChatGPT runtime does not provide Docker. The committed runner performs the 20 real executions using the hardened TRACER Docker validator:

```bash
python scripts/run_tracer32_execution_pilot.py
```

When run locally or in CI, the script writes `tracer32_execution_results.json`, `tracer32_execution_comparison.csv`, and `tracer32_execution_summary.json`, and aborts if a reference fails or a buggy program passes.

The file `results/pilot/tracer32_expected_results.csv` is a reviewed expectation sheet, not a substitute for recorded Docker evidence.
