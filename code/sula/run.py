import ast
import json
import os
import re
import time
from collections import Counter

import requests

PROMPT = """The following Python code has a bug.

Problem:
{question}

Buggy code:
```python
{buggy_code}
```

Fix the bug. Respond with only the corrected code in a single Python code block, no explanation."""

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(REPO_ROOT, "benchmarking", "data", "debugbench_full.json")
RESULTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:1.5b"
SEED = 42

def load_full_dataset():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH) as f:
            return json.load(f)
    from datasets import load_dataset
    ds = load_dataset("Rtian/DebugBench")["test"]
    rows = [ds[i] for i in range(len(ds))]
    with open(DATA_PATH, "w") as f:
        json.dump(rows, f)
    return rows

def extract_code(raw):
    match = re.search(r"```(?:python)?\s*\n?(.*?)```", raw, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw.strip()

def normalise(code):
    return ast.dump(ast.parse(code), annotate_fields=False)

def char_ngram_cosine(a, b, n=3):
    def vec(s):
        return Counter(s[i:i + n] for i in range(len(s) - n + 1))
    va, vb = vec(a), vec(b)
    common = set(va) & set(vb)
    dot = sum(va[k] * vb[k] for k in common)
    norm_a = sum(v * v for v in va.values()) ** 0.5
    norm_b = sum(v * v for v in vb.values()) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def call_ollama(question, buggy_code):
    prompt = PROMPT.format(question=question, buggy_code=buggy_code)
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "seed": SEED, "num_predict": 512},
    }
    start = time.time()
    resp = requests.post(OLLAMA_URL, json=payload)
    latency = time.time() - start
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", ""), latency, data.get("prompt_eval_count"), data.get("eval_count")

def grade(model_output, buggy_code, solution):
    try:
        parses = True
        model_ast = normalise(model_output)
    except SyntaxError:
        parses = False
        model_ast = None

    if not parses:
        return False, False, "syntax_error"

    try:
        buggy_ast = normalise(buggy_code)
    except SyntaxError:
        buggy_ast = None

    if buggy_ast is not None:
        unchanged = model_ast == buggy_ast
    else:
        unchanged = model_output.strip() == buggy_code.strip()
    correct = model_ast == normalise(solution)

    if unchanged:
        outcome = "no_change"
    elif correct:
        outcome = "correct"
    else:
        outcome = "incorrect"
    return correct, unchanged, outcome

def main():
    rows = load_full_dataset()
    python_rows = [r for r in rows if r["language"] == "python3"][:10]

    results = []
    for i, row in enumerate(python_rows):
        raw, latency, prompt_tokens, eval_tokens = call_ollama(row["question"], row["buggy_code"])
        print(f"--- [{i}] {row['slug']} raw response ---")
        print(raw)
        print("--- end raw response ---")

        extracted = extract_code(raw)
        correct, unchanged, outcome = grade(extracted, row["buggy_code"], row["solution"])
        cosine = char_ngram_cosine(extracted, row["solution"])

        results.append({
            "index": i,
            "slug": row["slug"],
            "category": row["category"],
            "subtype": row["subtype"],
            "buggy_code": row["buggy_code"],
            "reference_solution": row["solution"],
            "raw_response": raw,
            "extracted_code": extracted,
            "check_a_correct": correct,
            "check_b_unchanged": unchanged,
            "check_c_cosine_diagnostic_only": cosine,
            "outcome": outcome,
            "manual_verdict": None,
            "latency_sec": latency,
            "prompt_tokens": prompt_tokens,
            "eval_tokens": eval_tokens,
        })

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    counts = Counter(r["outcome"] for r in results)
    print("\n=== Summary ===")
    for outcome in ["correct", "incorrect", "syntax_error", "no_change"]:
        print(f"{outcome}: {counts.get(outcome, 0)}")
    incorrect_rate = sum(1 for r in results if r["outcome"] != "correct") / len(results)
    print(f"\nIncorrect-response rate (fraction not marked correct): {incorrect_rate:.2f}")
    print("\nKnown limitation: AST matching produces false negatives when the model")
    print("fixes the bug correctly but differently from the reference. Check manual_verdict")
    print("in results.json for hand-review at this sample size.")

if __name__ == "__main__":
    main()
