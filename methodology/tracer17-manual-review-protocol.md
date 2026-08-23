# TRACER-17 — Single-Reviewer Manual Review Protocol

## Scope
This PoC uses one reviewer, per project-owner decision, to resolve baseline records where automated checks could not establish correctness.

## Reviewer evidence
The reviewer may inspect:
- stored task statement;
- buggy input code;
- benchmark reference solution;
- model candidate;
- parse/reference-match status.

Model identity is not used as a correctness criterion.

## Verdicts
- `correct`: functionally satisfies the stored task.
- `incorrect`: contains a concrete functional/runtime/logic defect.
- `uncertain`: insufficient evidence.

For this completed PoC review, every unresolved record received either `correct` or `incorrect`.

## Ground-truth rules
1. Exact/reference AST match is a strong positive label.
2. Syntax/compile failure is a negative label for executable Python tasks.
3. AST mismatch alone is not a negative label.
4. Similarity/confidence diagnostics never determine ground truth.
5. Reference solutions and labels are offline evaluation evidence only and must not become inference-time ACRE features.

## Academic disclosure
This single review was performed by ChatGPT as an AI-assisted code reviewer. It is suitable as a PoC engineering label-resolution step but is not equivalent to an independent human inter-rater evaluation.
