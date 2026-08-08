"""
PoC: how often does gemma3:4b (local, via Ollama) fix bugs correctly on the
first 20 Python (python3) problems of the DebugBench dataset.

Grading is AST-based (Python's `ast` module), not string comparison, since
the sample is filtered to Python-only. See README.md for caveats.

Author: Lithma
"""

import ast
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests
from datasets import load_dataset

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:4b"
NUM_PROBLEMS = 20
OUT_DIR = Path(__file__).parent
RESULTS_PATH = OUT_DIR / "results.json"

CODE_BLOCK_RE = re.compile(r"```(?:\w+)?\s*\n(.*?)```", re.DOTALL)


def build_prompt(row):
    return f"""You are a code fixing assistant. Below is a buggy {row['language']} solution.

Problem description:
{row['question']}

Buggy code:
```{row['language']}
{row['buggy_code']}
```

Fix the bug. Respond with ONLY the corrected code in a single code block.
Do not include any explanation.
"""


def call_ollama(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": 0,
        "seed": 42,
        "num_predict": 512,
    }
    start = time.time()
    resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
    latency = time.time() - start
    resp.raise_for_status()
    return resp.json()["response"], latency


def extract_code(raw_response):
    match = CODE_BLOCK_RE.search(raw_response)
    if match:
        return match.group(1).strip()
    return raw_response.strip()


def normalized_ast(code):
    return ast.dump(ast.parse(code), annotate_fields=False)


def grade(extracted_code, reference_solution, buggy_code):
    if not extracted_code.strip():
        return "empty_response"

    try:
        norm_extracted = normalized_ast(extracted_code)
    except SyntaxError:
        return "syntax_error"

    if norm_extracted == normalized_ast(reference_solution):
        return "correct"

    try:
        buggy_matches = norm_extracted == normalized_ast(buggy_code)
    except SyntaxError:
        buggy_matches = extracted_code.strip() == buggy_code.strip()

    if buggy_matches:
        return "no_change"

    return "incorrect"


def main():
    dataset = load_dataset("Rtian/DebugBench")["test"]
    dataset = dataset.filter(lambda row: row["language"] == "python3")
    rows = [dataset[i] for i in range(NUM_PROBLEMS)]

    results = []
    for i, row in enumerate(rows):
        print(f"[{i + 1}/{NUM_PROBLEMS}] {row['slug']} ({row['language']}) ...")
        prompt = build_prompt(row)
        raw_response, latency = call_ollama(prompt)
        extracted_code = extract_code(raw_response)
        outcome = grade(extracted_code, row["solution"], row["buggy_code"])
        print(f"    -> {outcome} ({latency:.1f}s)")

        results.append(
            {
                "index": i,
                "slug": row["slug"],
                "language": row["language"],
                "category": row["category"],
                "subtype": row["subtype"],
                "buggy_code": row["buggy_code"],
                "reference_solution": row["solution"],
                "raw_response": raw_response,
                "extracted_code": extracted_code,
                "outcome": outcome,
                "latency_sec": latency,
            }
        )

    RESULTS_PATH.write_text(json.dumps(results, indent=2))

    outcome_counts = Counter(r["outcome"] for r in results)
    by_language = defaultdict(Counter)
    for r in results:
        by_language[r["language"]][r["outcome"]] += 1

    print("\n=== Summary ===")
    for outcome, count in outcome_counts.most_common():
        print(f"{outcome}: {count}")

    print("\n=== By language ===")
    for language, counts in by_language.items():
        counts_str = ", ".join(f"{o}={c}" for o, c in counts.items())
        print(f"{language}: {counts_str}")

    print(f"\nResults written to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
