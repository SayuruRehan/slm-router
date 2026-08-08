# DebugBench + gemma3:4b PoC

<!-- Author: Lithma -->

Standalone proof-of-concept measuring how often **gemma3:4b**, run locally
via **Ollama**, fixes bugs correctly on the first 20 Python problems of the
[DebugBench](https://huggingface.co/datasets/Rtian/DebugBench) dataset
(`Rtian/DebugBench`, `test` split, filtered to `language == "python3"`).

## Setup

- Model: `gemma3:4b`, served locally by Ollama (`POST /api/generate`)
- Decoding: `temperature=0`, `seed=42`, `num_predict=512`, `stream=False`
- Sample: first 20 rows of `Rtian/DebugBench["test"]` after filtering to
  `language == "python3"`

## Results

| # | Slug | Language | Category | Outcome | Latency (s) |
|---|------|----------|----------|---------|--------------|
| 0 | moving-stones-until-consecutive-ii | python3 | syntax error | incorrect | 15.4 |
| 1 | largest-number-after-mutating-substring | python3 | syntax error | correct | 4.7 |
| 2 | nim-game | python3 | syntax error | correct | 1.9 |
| 3 | find-all-possible-recipes-from-given-supplies | python3 | syntax error | incorrect | 14.1 |
| 4 | sequential-digits | python3 | syntax error | incorrect | 5.1 |
| 5 | check-if-string-is-transformable-with-substring-sort-operations | python3 | syntax error | incorrect | 6.1 |
| 6 | increasing-order-search-tree | python3 | syntax error | incorrect | 7.0 |
| 7 | check-if-one-string-swap-can-make-strings-equal | python3 | syntax error | incorrect | 7.0 |
| 8 | disconnect-path-in-a-binary-matrix-by-at-most-one-flip | python3 | syntax error | incorrect | 15.9 |
| 9 | smallest-string-starting-from-leaf | python3 | syntax error | incorrect | 6.4 |
| 10 | online-election | python3 | syntax error | incorrect | 15.2 |
| 11 | number-complement | python3 | syntax error | incorrect | 3.2 |
| 12 | binary-tree-level-order-traversal-ii | python3 | syntax error | incorrect | 8.4 |
| 13 | maximum-of-absolute-value-expression | python3 | syntax error | incorrect | 5.6 |
| 14 | minimum-cost-to-make-at-least-one-valid-path-in-a-grid | python3 | syntax error | incorrect | 10.3 |
| 15 | alternating-digit-sum | python3 | syntax error | incorrect | 4.1 |
| 16 | best-time-to-buy-and-sell-stock-ii | python3 | syntax error | incorrect | 5.6 |
| 17 | substring-with-concatenation-of-all-words | python3 | syntax error | incorrect | 8.7 |
| 18 | merge-k-sorted-lists | python3 | syntax error | incorrect | 4.9 |
| 19 | find-the-string-with-lcp | python3 | syntax error | incorrect | 10.3 |

### Summary

| Outcome | Count |
|---|---|
| correct | 2 |
| incorrect | 18 |
| no_change | 0 |
| syntax_error | 0 |
| empty_response | 0 |

### By language

| Language | correct | incorrect | no_change | syntax_error | empty_response |
|---|---|---|---|---|---|
| python3 | 2 | 18 | 0 | 0 | 0 |

Full per-problem detail (buggy code, reference solution, raw model
response, extracted code) is in `results.json`.

## Grading method — read this before comparing to other results

Outcomes are graded by **AST comparison**, using Python's `ast` module,
rather than by string comparison or execution:

1. Extract the first fenced code block from the model's raw response
   (fall back to the raw text if there is none).
2. If `ast.parse` on the extracted code raises a `SyntaxError`, label the
   outcome `syntax_error`.
3. Otherwise, normalize the extracted code's AST via
   `ast.dump(tree, annotate_fields=False)` and compare it against the same
   normalized dump of the reference solution. Label `correct` on a match.
4. If not correct, compare the normalized AST of the extracted code against
   the normalized AST of the buggy input (parsed in its own try/except,
   falling back to a plain stripped-string comparison if the buggy code
   itself isn't valid Python). Label `no_change` on a match, `incorrect`
   otherwise.
5. Label `empty_response` if extraction produced nothing, checked before
   any of the above.

Comparing normalized ASTs (rather than raw or normalized strings) means a
fix is recognized as `correct` even when it is formatted, renamed, or
restructured differently from the reference solution — different variable
names, reordered helper functions, or extra comments no longer cause a
false `incorrect`. AST comparison is only possible because the sample is
now filtered to Python (`python3`) exclusively.

**This makes results here more directly comparable to the Python-only,
AST-graded baseline elsewhere in this repo (`code/sula/`)** — both use the
same AST-comparison grading approach on Python-only samples (different
model, different sample).

## Running it

```bash
source .venv/bin/activate
python code/lithma/PoCs/debugbench-gemma-poc/run_poc.py
```

Requires Ollama running locally with `gemma3:4b` pulled
(`ollama pull gemma3:4b`).
