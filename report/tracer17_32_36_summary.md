# TRACER-17 / TRACER-32 / TRACER-36 Summary

## TRACER-17 — Manual review
The 29 unresolved baseline outputs have been resolved using the requested **single-reviewer** PoC process.

- Qwen: **6/20 correct (30.0%)**
- Gemma: **7/20 correct (35.0%)**
- Combined: **13/40 correct (32.5%)**

The detailed reasoning is in `results/manual_review/tracer17_manual_review.csv`.

## TRACER-32 — Five-sample pilot
Five deterministic fixtures and 20 candidate executions are defined.

Manually reviewed expected outcomes:
- reference: **5/5 pass**
- original buggy: **0/5 pass**
- Qwen: **2/5 pass**
- Gemma: **5/5 pass**

Because this ChatGPT environment does not expose Docker, these are clearly stored as **expected** results rather than fabricated execution logs. Run `python scripts/run_tracer32_execution_pilot.py` in the repository to capture the real Docker evidence.

## TRACER-36 — Protocol freeze
The protocol is now defined around this evidence hierarchy:

**Executable tests → syntax/compile failure → reference/AST exact match → single manual review → diagnostic similarity/confidence**

The baseline report below incorporates all completed TRACER-31 evidence and the completed TRACER-17 labels, and treats TRACER-32 Docker execution as the final verification gate.

## Research-quality caveat
The project owner explicitly simplified TRACER-17 from two independent human reviews to one review for the PoC. The review in this artifact was performed by ChatGPT as an AI-assisted code reviewer. Do not report Cohen's kappa or inter-rater reliability for this run.
