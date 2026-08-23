# TRACER-17 — Single-Reviewer Manual Review Summary

## Review approach
For this PoC iteration, the project owner requested **one reviewer instead of two independent reviewers**. The 29 records previously labelled `needs_manual_review` were reviewed by code inspection against the stored task statement and benchmark reference solution.

**Reviewer disclosure:** the review was performed by ChatGPT as an AI-assisted code reviewer. It should not be described in the research paper as an independent human inter-rater study.

## Results
| Model | Manual cases | Manual correct | Manual incorrect | Final correct / 20 | Final accuracy |
|---|---:|---:|---:|---:|---:|
| Qwen | 11 | 4 | 7 | 6 | 30.0% |
| Gemma | 18 | 5 | 13 | 7 | 35.0% |

Overall baseline correctness after resolving all 40 samples: **13/40 (32.5%)**.

## Important interpretation
- `reference_match` remained an automated positive label.
- baseline `syntax_error` remained an automated negative label.
- only the 29 unresolved cases received the single manual review.
- AST/reference mismatch was **not** treated as incorrect by itself.
- cosine similarity was not used as a correctness label.
- Gemma's `maximum-of-absolute-value-expression` was marked functionally correct for the stored task statement, with medium confidence because the O(n^2) solution may not satisfy large hidden runtime constraints.

Detailed decisions are in `results/manual_review/tracer17_manual_review.csv`.
