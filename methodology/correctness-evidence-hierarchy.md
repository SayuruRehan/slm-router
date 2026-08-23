# TRACER-36 — Correctness-Evidence Hierarchy

1. **Valid executable tests** — primary correctness evidence when available.
2. **Syntax/compile failure** — definitive negative for executable Python tasks.
3. **Normalized reference/AST exact match** — strong positive evidence.
4. **Single manual review for this PoC** — resolves cases without executable tests, per project-owner simplification.
5. **Similarity/confidence signals** — diagnostics only; never ground truth.

## Infrastructure rule
Docker/image/mount/runner failures are infrastructure failures and must not be converted into candidate failures.

## Research leakage rule
Reference solutions, gold labels, and test outcomes are offline supervision/evaluation data only. They must not be inference-time ACRE features.

## Freeze note
For the main study, objective executable tests should replace manual review wherever practical. A multi-reviewer protocol can be reinstated if inter-rater reliability becomes a reported research result.
