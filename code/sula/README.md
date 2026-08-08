# DebugBench SLM smoke test

Step-zero baseline for the repair-vs-regenerate question: how often does a
small local model get DebugBench Python problems wrong, and what does the
grading pipeline need to look like?

No repair, no routing, no strong model, no API calls. Ten problems, one local
model, three grading checks.

## What this measures

Sends the first 10 `python3` DebugBench problems to a local SLM and asks it to
fix the bug, then grades the response three ways. Current baseline with
`qwen2.5-coder:1.5b`:

| Outcome | Count |
| --- | --- |
| `correct` | 1 |
| `incorrect` | 5 |
| `syntax_error` | 4 |
| `no_change` | 0 |

**Incorrect-response rate: 0.90.** Four of ten responses were not valid Python
at all — a distinct failure mode worth keeping separate from a wrong fix.

## Prerequisites

[Ollama](https://ollama.com) installed and running, with the model pulled:

```bash
ollama pull qwen2.5-coder:1.5b
```

`run.py` expects the Ollama HTTP API at `http://localhost:11434`. Verify with:

```bash
curl -s http://localhost:11434/api/tags
```

Python 3.11 was used for the baseline above.

## Setup

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r code/sula/requirements.txt
```

The venv is gitignored, so each of us creates our own.

## Running

```bash
python code/sula/run.py
```

Takes a couple of minutes — ten sequential requests, one at a time, so it
stays usable on a laptop. It prints each raw model response as it goes, then a
summary, and writes `code/sula/results.json`.

The dataset is already committed at `benchmarking/data/debugbench_full.json`
(full test split, 4253 rows, 1414 of them `python3`), so this runs offline.
Only if that file is missing does `run.py` re-download from Hugging Face.

## Viewing results

```bash
streamlit run code/sula/app.py
```

Table of all ten with outcome labels; select a row to see buggy code, model
output, and reference solution side by side, plus the raw pre-extraction
response. The **Re-run the 10 problems** button regenerates `results.json`
in place, so the numbers can be reproduced live rather than taken on trust.

## Reproducibility

`temperature=0` and `seed=42` are fixed in `run.py`, and the dataset is pinned
in the repo, so a re-run on the same model reproduces the same numbers. If your
results differ, the likely causes are a different model tag, a different Ollama
version, or an edited `PROMPT`.

To try another model, change `MODEL` at the top of `run.py` (`ollama list`
shows what you have pulled). The prompt is a single `PROMPT` constant at the
top of the same file.

## How grading works

Three checks, reported separately and deliberately not collapsed into one score:

- **Check A — AST match.** The correctness verdict. Model output vs. reference
  solution, compared as `ast.dump(ast.parse(code), annotate_fields=False)`, so
  whitespace, comments and formatting are ignored. Output that does not parse
  is recorded as `syntax_error`, not `incorrect`.
- **Check B — no-change.** Same AST comparison against the *buggy input*. A
  match means the model handed back the bug untouched, which is a different
  failure mode from a wrong fix.
- **Check C — cosine similarity.** Character-trigram cosine against the
  reference. **Diagnostic only, not a correctness signal.** Buggy and fixed
  code are near-identical on this dataset, so it sits around 0.97 for
  everything and discriminates nothing. It is logged to demonstrate that, not
  to grade with.

Outcome labels are assigned in priority order: `syntax_error` → `no_change` →
`correct` → `incorrect`.

## Known limitations

- **AST matching produces false negatives.** A model can fix the bug correctly
  but differently from the reference and still be marked `incorrect`. Every
  record has a `manual_verdict` field, `null` by default, for hand review. At
  n=10 all ten are meant to be read by eye; this has not been done yet.
- **n=10 is a smoke test**, not a result. It exists to prove the pipeline works
  and to produce failures worth studying.
- **Some `buggy_code` samples are not valid Python** (the syntax-error
  category includes genuinely unparseable code), so Check B falls back to
  string comparison for those rows.

## Files

| File | Purpose |
| --- | --- |
| `run.py` | Loads data, calls Ollama, grades, writes `results.json` |
| `app.py` | Streamlit viewer |
| `requirements.txt` | `datasets`, `requests`, `streamlit` |
| `results.json` | Generated output, one record per problem |

Each `results.json` record carries the problem slug, bug category and subtype,
buggy code, reference solution, raw and extracted model output, all three
check results, the outcome label, `manual_verdict`, latency, and token counts.
