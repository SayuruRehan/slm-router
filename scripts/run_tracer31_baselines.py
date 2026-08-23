"""Run and verify the paired TRACER-31 Qwen/Gemma 20-sample baselines."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import socket
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tracer.config import ExperimentConfig, load_config

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = REPO_ROOT / "results" / "baselines"
RUN_MANIFEST_PATH = RESULT_DIR / "tracer31_run_manifest.json"


@dataclass(frozen=True)
class BaselineSpec:
    label: str
    config_path: Path
    records_path: Path
    summary_path: Path


BASELINES = (
    BaselineSpec(
        label="qwen",
        config_path=REPO_ROOT / "configs" / "qwen25_coder_baseline.yaml",
        records_path=RESULT_DIR / "qwen25_coder_records.json",
        summary_path=RESULT_DIR / "qwen25_coder_summary.json",
    ),
    BaselineSpec(
        label="gemma",
        config_path=REPO_ROOT / "configs" / "gemma3_baseline.yaml",
        records_path=RESULT_DIR / "gemma3_records.json",
        summary_path=RESULT_DIR / "gemma3_summary.json",
    ),
)

REQUIRED_RECORD_FIELDS = {
    "dataset_index",
    "slug",
    "model",
    "model_digest",
    "ollama_version",
    "latency_sec",
    "prompt_tokens",
    "eval_tokens",
    "raw_response",
    "extracted_code",
    "outcome",
    "label_source",
    "execution_status",
    "execution_passed",
    "execution_exit_code",
    "execution_duration_sec",
    "execution_stdout",
    "execution_stderr",
    "validator_config",
}

REQUIRED_VALIDATOR_FIELDS = {
    "backend",
    "execution_enabled",
    "docker_image",
    "timeout_seconds",
    "memory_mb",
    "cpu_limit",
    "pids_limit",
    "network_mode",
    "python_isolated_mode",
}


def _runtime_environment() -> dict[str, str | None]:
    # TRACER-31: preserve host hardware/OS context for the paired baseline run.
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_release": platform.release(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or None,
        "python_version": platform.python_version(),
    }


def _validate_shared_controls(configs: list[ExperimentConfig]) -> None:
    first, second = configs
    comparisons = {
        "dataset": first.dataset.path.resolve() == second.dataset.path.resolve(),
        "manifest": first.dataset.manifest.resolve() == second.dataset.manifest.resolve(),
        "prompt_version": first.prompt.version == second.prompt.version,
        "generation_options": first.model.options == second.model.options,
        "validator": first.validator.to_metadata() == second.validator.to_metadata(),
    }
    mismatches = [name for name, matches in comparisons.items() if not matches]
    if mismatches:
        raise RuntimeError(
            "TRACER-31 shared-control check failed: " + ", ".join(sorted(mismatches))
        )


def _run_baseline(cli: str, spec: BaselineSpec, *, dry_run: bool) -> None:
    command = [cli, "--config", str(spec.config_path)]
    if dry_run:
        command.append("--dry-run")

    previous_mtime = spec.records_path.stat().st_mtime_ns if spec.records_path.exists() else None
    print(f"\n=== TRACER-31: {spec.label.upper()} ===")
    completed = subprocess.run(command, cwd=REPO_ROOT, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"{spec.label} baseline failed with exit code {completed.returncode}"
        )

    if dry_run:
        return

    if not spec.records_path.exists() or not spec.summary_path.exists():
        raise RuntimeError(
            f"{spec.label} completed but standardized records/summary files are missing"
        )
    current_mtime = spec.records_path.stat().st_mtime_ns
    if previous_mtime is not None and current_mtime == previous_mtime:
        raise RuntimeError(
            f"{spec.label} completed but {spec.records_path.name} was not refreshed"
        )


def _load_and_validate_records(spec: BaselineSpec) -> list[dict[str, Any]]:
    raw = json.loads(spec.records_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise RuntimeError(f"{spec.records_path.name} must contain a JSON list")
    if len(raw) != 20:
        raise RuntimeError(
            f"{spec.label} must contain exactly 20 records; found {len(raw)}"
        )

    seen: set[tuple[int, str]] = set()
    for index, record in enumerate(raw):
        missing = REQUIRED_RECORD_FIELDS - set(record)
        if missing:
            raise RuntimeError(
                f"{spec.label} record {index} is missing: {', '.join(sorted(missing))}"
            )
        validator = record.get("validator_config") or {}
        missing_validator = REQUIRED_VALIDATOR_FIELDS - set(validator)
        if missing_validator:
            raise RuntimeError(
                f"{spec.label} record {index} validator metadata is missing: "
                f"{', '.join(sorted(missing_validator))}"
            )
        identity = (int(record["dataset_index"]), str(record["slug"]))
        if identity in seen:
            raise RuntimeError(f"{spec.label} contains duplicate sample identity {identity}")
        seen.add(identity)
    return raw


def _identity(records: list[dict[str, Any]]) -> list[tuple[int, str]]:
    return [(int(record["dataset_index"]), str(record["slug"])) for record in records]


def _load_summary(spec: BaselineSpec) -> dict[str, Any]:
    summary = json.loads(spec.summary_path.read_text(encoding="utf-8"))
    if summary.get("sample_count") != 20:
        raise RuntimeError(f"{spec.label} summary does not report 20 samples")
    if not summary.get("validator_config"):
        raise RuntimeError(f"{spec.label} summary is missing validator configuration")
    if not summary.get("runtime_environment"):
        raise RuntimeError(f"{spec.label} summary is missing runtime environment metadata")
    return summary


def _write_run_manifest(
    records_by_label: dict[str, list[dict[str, Any]]],
    summaries: dict[str, dict[str, Any]],
) -> None:
    qwen_identity = _identity(records_by_label["qwen"])
    specs_by_label = {spec.label: spec for spec in BASELINES}
    manifest = {
        "jira": "TRACER-31",
        "completed_at": datetime.now(UTC).isoformat(),
        "runtime_environment": _runtime_environment(),
        "sample_count": len(qwen_identity),
        "sample_ids": [
            {"dataset_index": dataset_index, "slug": slug}
            for dataset_index, slug in qwen_identity
        ],
        "runs": {
            label: {
                "model": summaries[label].get("model"),
                "run_id": summaries[label].get("run_id"),
                "model_digests": sorted(
                    {
                        str(record["model_digest"])
                        for record in records
                        if record.get("model_digest") is not None
                    }
                ),
                "ollama_versions": sorted(
                    {
                        str(record["ollama_version"])
                        for record in records
                        if record.get("ollama_version") is not None
                    }
                ),
                "records": str(
                    specs_by_label[label].records_path.relative_to(REPO_ROOT)
                ),
                "summary": str(
                    specs_by_label[label].summary_path.relative_to(REPO_ROOT)
                ),
            }
            for label, records in records_by_label.items()
        },
    }
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    RUN_MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate both frozen configs through tracer-baseline without contacting Ollama",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cli = shutil.which("tracer-baseline")
    if cli is None:
        raise SystemExit('Install the project first: pip install -e ".[dev,viewer]"')

    configs = [load_config(spec.config_path) for spec in BASELINES]
    _validate_shared_controls(configs)

    # TRACER-31: every model is invoked through the same canonical runner and controls.
    for spec in BASELINES:
        _run_baseline(cli, spec, dry_run=args.dry_run)

    if args.dry_run:
        print("\nTRACER-31 dry run passed for both frozen baseline configurations.")
        return 0

    records_by_label = {
        spec.label: _load_and_validate_records(spec) for spec in BASELINES
    }
    identities = {label: _identity(records) for label, records in records_by_label.items()}
    if identities["qwen"] != identities["gemma"]:
        raise RuntimeError("Qwen and Gemma did not run the same ordered 20 sample IDs")

    summaries = {spec.label: _load_summary(spec) for spec in BASELINES}
    _write_run_manifest(records_by_label, summaries)
    print(f"\nTRACER-31 complete: {RUN_MANIFEST_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
