# TRACER-35 — Execution, Static/AST, and Reviewed-Label Comparison

## Purpose
Compare objective Docker execution evidence, static/AST evidence, and reviewed expected labels for the five-sample TRACER-32 pilot.

## Evidence used
- `sample_manifests/tracer32_execution_pilot.json`
- `results/pilot/tracer32_expected_results.csv`
- `results/pilot/tracer32_execution_comparison.csv`
- `results/manual_review/tracer17_final_labels.csv`
- `methodology/correctness-evidence-hierarchy.md`

## Findings
All 20 pilot candidates were compared.

- No case produced a true contradiction between the reviewed correctness label and Docker execution.
- Exact/reference AST matches were supported by execution in this pilot.
- Syntax-invalid candidates failed execution as expected.
- Several functionally correct candidates were not exact AST/reference matches.
- Therefore AST mismatch must not be treated as a negative correctness label.

### Important disagreements between AST/reference matching and functional correctness

| Sample | Candidate | Static/AST result | Reviewed label | Docker | Interpretation |
|---|---|---|---|---|---|
| sequential-digits | Qwen | non-match / unresolved | correct | pass | Alternative implementation is functionally correct. |
| sequential-digits | Gemma | non-match / unresolved | correct | pass | AST identity is unnecessary for correctness. |
| one-string-swap | Gemma | non-match / unresolved | correct | pass | Different control flow still satisfies the task. |
| number-complement | Gemma | non-match / unresolved | correct | pass | Structural mismatch is not evidence of failure. |
| alternating-digit-sum | Gemma | non-match / unresolved | correct | pass | Execution confirms correctness despite AST difference. |
| nim-game | Qwen | unresolved | incorrect | fail | Manual review identified the inverted condition; execution confirmed it. |

## Final evidence precedence
1. **Valid executable tests** — primary correctness evidence when available.
2. **Syntax/compile failure** — definitive negative for executable Python tasks.
3. **Normalized reference/AST exact match** — strong positive evidence only.
4. **Manual review for unresolved cases** — used only when objective tests are unavailable or incomplete.
5. **Similarity/confidence diagnostics** — never ground truth.

## Unresolved-label policy
- If authoritative executable tests are available, their result is the final correctness label.
- Infrastructure failures are recorded separately and never converted into candidate failures.
- Syntax/compile failure can establish incorrectness for executable Python tasks.
- Exact normalized reference/AST match may establish a positive label, but AST mismatch must **not** establish a negative label.
- If objective tests are absent or insufficient, route the case to a documented manual-review process.
- If review remains uncertain, retain the case as unresolved/excluded instead of forcing a binary label.
- Reference solutions, gold labels, and test outcomes remain offline supervision/evaluation data only and must not become inference-time ACRE features.

## Decision
The five-sample pilot supports the existing correctness-evidence hierarchy. The central result is that **objective execution outranks structural similarity, and AST mismatch alone is not evidence of incorrectness**.

## Approval
Technical comparison is complete. Jira closure requires the team to approve this hierarchy and unresolved-label policy.
