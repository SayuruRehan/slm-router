# TRACER-36 — Baseline Experiment Report and Protocol Freeze Candidate

## 1. Objective
Establish a reproducible PoC baseline for Qwen and Gemma on the same 20 DebugBench samples, resolve previously ambiguous labels, validate a small execution-test design, and freeze the correctness-evidence rules before scaling the study.

## 2. Frozen TRACER-31 configuration
- Dataset SHA-256: `8a48789a7d5968d832a8756f6cca607b97a4a7e002bd746c90661527ed95f8c8`
- Qwen: `qwen2.5-coder:1.5b` / run `20260823T055846Z-2a2e56f1`
- Gemma: `gemma3:4b` / run `20260823T060119Z-cabb9934`
- Prompt version: `debugbench-code-repair-v1`
- Temperature: `0`
- Seed: `42`
- Max generated tokens: `512`
- Ollama: `0.32.1`
- Host: `macOS-15.7.4-arm64-arm-64bit-Mach-O`
- Python: `3.14.2`
- Docker image: `python:3.11-slim`
- Sandbox: network none, read-only root/workspace, cap-drop ALL, no-new-privileges, 256 MB, CPU 0.5, PID limit 64, isolated Python.

## 3. Automated baseline outcomes before manual review
| Model | Reference match | Syntax error | Needs review |
|---|---:|---:|---:|
| Qwen | 2 | 7 | 11 |
| Gemma | 2 | 0 | 18 |

## 4. TRACER-17 final labels
A single reviewer was used for this PoC, per project-owner decision.

| Model | Manual cases | Manual correct | Manual incorrect | Final correct / 20 | Final accuracy |
|---|---:|---:|---:|---:|---:|
| Qwen | 11 | 4 | 7 | 6 | 30.0% |
| Gemma | 18 | 5 | 13 | 7 | 35.0% |

Combined final correctness: **13/40 (32.5%)**.

## 5. Runtime/token evidence
| Metric | Qwen | Gemma |
|---|---:|---:|
| Total latency (s) | 151.57 | 502.33 |
| Mean latency (s) | 7.58 | 25.12 |
| Prompt tokens | 8885 | 9622 |
| Completion/eval tokens | 3921 | 4022 |

These are descriptive only; TRACER is not optimizing cost or latency.

## 6. TRACER-32 pilot
Five samples and deterministic tests are frozen in `sample_manifests/tracer32_execution_pilot.json`.

Manually reviewed expected result pattern:
- reference: 5/5 pass
- original buggy: 0/5 pass
- Qwen: 2/5 pass
- Gemma: 5/5 pass

The actual Docker result files are intentionally not fabricated. Run:
```bash
python scripts/run_tracer32_execution_pilot.py
```

The runner enforces the sanity gate that every reference must pass and every original buggy program must fail.

## 7. Frozen correctness-evidence hierarchy
1. valid executable tests;
2. syntax/compile failure;
3. normalized reference/AST exact match;
4. single manual review for unresolved PoC cases;
5. similarity/confidence as diagnostics only.

Reference solutions and test outcomes remain offline labels/evaluation evidence and must not be inference-time ACRE features.

## 8. Known limitations
- The cached 20-sample DebugBench subset does not include authoritative executable tests.
- TRACER-17 was simplified to one reviewer, so no independent human agreement measure exists.
- The five-sample TRACER-32 fixture set is a PoC validation set, not a final evaluation benchmark.
- Gemma's brute-force maximum-absolute-expression solution was treated as functionally correct for the stored prompt, but may violate large hidden runtime constraints.
- The Docker sandbox reduces risk but is not a perfect security boundary.

## 9. Protocol-freeze decision
The PoC protocol is ready to freeze **subject to one final mechanical check: run the TRACER-32 Docker pilot and confirm its recorded outputs match the manually reviewed expectations or investigate any mismatch before scaling**.
