"""Run comparable DebugBench baselines through the canonical TRACER pipeline."""

from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from tracer.config import ExperimentConfig, load_config
from tracer.datasets import dataset_sha256, load_manifest_samples
from tracer.models import OllamaClient
from tracer.prompts import build_code_repair_prompt
from tracer.schemas import ExperimentRecord
from tracer.validators import extract_code, validate_python_response
from tracer.validators.ast_checks import char_ngram_cosine


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as output_file:
            output_file.write(content)
        os.replace(temporary_name, path)
    except Exception:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=list(rows[0]))
            writer.writeheader()
            for row in rows:
                flat = dict(row)
                flat["generation_options"] = json.dumps(
                    flat["generation_options"], sort_keys=True
                )
                writer.writerow(flat)
        os.replace(temporary_name, path)
    except Exception:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def build_summary(
    config: ExperimentConfig,
    run_id: str,
    started_at: str,
    records: list[ExperimentRecord],
) -> dict[str, Any]:
    outcomes = Counter(record.outcome for record in records)
    resolved = [record for record in records if record.correctness is not None]
    correct = sum(record.correctness is True for record in resolved)
    return {
        "run_id": run_id,
        "experiment_name": config.name,
        "experiment_version": config.version,
        "started_at": started_at,
        "finished_at": datetime.now(UTC).isoformat(),
        "model": config.model.name,
        "generation_options": config.model.options,
        "prompt_version": config.prompt.version,
        "sample_count": len(records),
        "resolved_label_count": len(resolved),
        "manual_review_count": sum(record.needs_manual_review for record in records),
        "correct_among_resolved": correct,
        "accuracy_among_resolved": correct / len(resolved) if resolved else None,
        "outcomes": dict(sorted(outcomes.items())),
        "important_note": (
            "DebugBench does not provide executable tests in this cached dataset. "
            "reference_match is an AST-reference label; needs_manual_review is unresolved "
            "and must not be counted as incorrect."
        ),
    }


def write_outputs(
    config: ExperimentConfig,
    records: list[ExperimentRecord],
    summary: dict[str, Any],
) -> None:
    rows = [record.to_dict() for record in records]
    _atomic_write_text(config.output.json_path, json.dumps(rows, indent=2, ensure_ascii=False))
    _write_csv(config.output.csv_path, rows)
    _atomic_write_text(
        config.output.summary_path, json.dumps(summary, indent=2, ensure_ascii=False)
    )


def run(config: ExperimentConfig, *, dry_run: bool = False) -> list[ExperimentRecord]:
    samples = load_manifest_samples(config.dataset.path, config.dataset.manifest)
    checksum = dataset_sha256(config.dataset.path)
    print(f"Experiment: {config.name} v{config.version}")
    print(f"Model: {config.model.name}")
    print(f"Samples: {len(samples)} from {config.dataset.manifest.relative_to(config.repo_root)}")
    print(f"Dataset SHA-256: {checksum}")
    if dry_run:
        for position, sample in enumerate(samples):
            print(f"[{position:02d}] dataset[{sample.dataset_index}] {sample.slug}")
        print("Dry run complete; Ollama was not contacted and no results were written.")
        return []

    client = OllamaClient(config.model)
    run_id = f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"
    started_at = datetime.now(UTC).isoformat()
    records: list[ExperimentRecord] = []

    for position, sample in enumerate(samples):
        print(f"[{position + 1}/{len(samples)}] {sample.slug}")
        prompt = build_code_repair_prompt(sample, config.prompt.version)
        generation = client.generate(prompt)
        extracted = extract_code(generation.response)
        validation = validate_python_response(
            candidate_code=extracted,
            buggy_code=sample.buggy_code,
            reference_solution=sample.reference_solution,
            test_code=sample.test_code,
            validator_config=config.validator,
        )
        print(f"  -> {validation.outcome} ({generation.latency_seconds:.1f}s)")
        records.append(
            ExperimentRecord(
                run_id=run_id,
                experiment_name=config.name,
                experiment_version=config.version,
                prompt_version=config.prompt.version,
                dataset_sha256=checksum,
                sample_manifest=str(config.dataset.manifest.relative_to(config.repo_root)),
                index=position,
                dataset_index=sample.dataset_index,
                slug=sample.slug,
                language=sample.language,
                category=sample.category,
                subtype=sample.subtype,
                question=sample.question,
                buggy_code=sample.buggy_code,
                reference_solution=sample.reference_solution,
                prompt=prompt,
                raw_response=generation.response,
                extracted_code=extracted,
                model=generation.model,
                model_digest=generation.model_digest,
                ollama_version=generation.ollama_version,
                generation_options=config.model.options,
                latency_sec=generation.latency_seconds,
                prompt_tokens=generation.prompt_tokens,
                eval_tokens=generation.completion_tokens,
                outcome=validation.outcome,
                correctness=validation.correctness,
                label_source=validation.label_source,
                needs_manual_review=validation.needs_manual_review,
                check_a_correct=validation.reference_ast_match,
                check_b_unchanged=validation.unchanged,
                check_c_cosine_diagnostic_only=char_ngram_cosine(
                    extracted, sample.reference_solution
                ),
                parses=validation.parses,
                execution_status=validation.execution.status,
                execution_passed=validation.execution.passed,
            )
        )

    summary = build_summary(config, run_id, started_at, records)
    write_outputs(config, records, summary)
    print(f"Records: {config.output.json_path}")
    print(f"Summary: {config.output.summary_path}")
    return records


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Path to an experiment YAML file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration and sample identity without contacting Ollama",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_args(argv)
    run(load_config(arguments.config), dry_run=arguments.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
