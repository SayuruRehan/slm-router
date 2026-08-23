#!/usr/bin/env python3
"""TRACER-32: execute the fixed five-sample pilot with the hardened Docker validator."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from tracer.config import ValidatorConfig
from tracer.validators.execution import DockerPythonSandbox, SandboxUnavailableError


# TRACER-32: classify execution failures without treating infrastructure errors as model errors.
def failure_category(result) -> str:
    if result.status == "timeout":
        return "timeout"
    stderr = result.stderr or ""
    if "IndentationError" in stderr:
        return "indentation_error"
    if "SyntaxError" in stderr:
        return "syntax_error"
    if "AssertionError" in stderr:
        return "assertion_failure"
    if result.passed:
        return "none"
    return "runtime_or_other_failure"


def main() -> None:
    qwen = {
        r["slug"]: r
        for r in json.loads(Path("results/baselines/qwen25_coder_records.json").read_text())
    }
    gemma = {
        r["slug"]: r
        for r in json.loads(Path("results/baselines/gemma3_records.json").read_text())
    }
    fixtures = json.loads(Path("sample_manifests/tracer32_execution_pilot.json").read_text())

    config = ValidatorConfig(
        backend="docker",
        docker_image="python:3.11-slim",
        timeout_seconds=10.0,
        memory_mb=256,
        cpu_limit=0.5,
        pids_limit=64,
    )
    sandbox = DockerPythonSandbox(config)
    if not sandbox.available():
        raise SandboxUnavailableError(
            "TRACER-32 requires Docker; no host execution fallback is allowed."
        )

    results = []
    for fixture in fixtures:
        slug = fixture["slug"]
        q = qwen[slug]
        g = gemma[slug]
        preamble = fixture["candidate_preamble"]
        candidates = {
            "buggy": q["buggy_code"],
            "reference": q["reference_solution"],
            "qwen": q["extracted_code"],
            "gemma": g["extracted_code"],
        }

        per_sample = {}
        for candidate_type, code in candidates.items():
            result = sandbox.run(preamble + "\n" + code, fixture["test_code"])
            row = {
                "jira": "TRACER-32",
                "slug": slug,
                "dataset_index": fixture["dataset_index"],
                "candidate_type": candidate_type,
                "passed": result.passed,
                "status": result.status,
                "failure_category": failure_category(result),
                "exit_code": result.exit_code,
                "duration_seconds": result.duration_seconds,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "validator_config": config.to_metadata(),
            }
            results.append(row)
            per_sample[candidate_type] = row
            print(f"{slug} / {candidate_type}: {row['status']} ({row['failure_category']})")

        # TRACER-32: fixture sanity gate.
        if not per_sample["reference"]["passed"]:
            raise SystemExit(f"Reference fixture failed for {slug}; do not approve this pilot.")
        if per_sample["buggy"]["passed"]:
            raise SystemExit(
                f"Buggy fixture passed for {slug}; tests are not discriminative enough."
            )

    out = Path("results/pilot")
    out.mkdir(parents=True, exist_ok=True)
    (out / "tracer32_execution_results.json").write_text(json.dumps(results, indent=2))

    csv_fields = [
        "slug", "dataset_index", "candidate_type", "passed", "status",
        "failure_category", "exit_code", "duration_seconds",
    ]
    with (out / "tracer32_execution_comparison.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        for row in results:
            writer.writerow({key: row[key] for key in csv_fields})

    summary = {
        "jira": "TRACER-32",
        "sample_count": len(fixtures),
        "candidate_run_count": len(results),
        "reference_pass_count": sum(
            r["passed"]
            for r in results
            if r["candidate_type"] == "reference"
        ),
        "buggy_fail_count": sum(not r["passed"] for r in results if r["candidate_type"] == "buggy"),
        "qwen_pass_count": sum(r["passed"] for r in results if r["candidate_type"] == "qwen"),
        "gemma_pass_count": sum(r["passed"] for r in results if r["candidate_type"] == "gemma"),
        "sanity_gate_passed": True,
        "validator_config": config.to_metadata(),
    }
    (out / "tracer32_execution_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
