import csv
import json
from dataclasses import replace
from pathlib import Path

from tracer.config import OutputConfig, load_config
from tracer.experiments import run_baseline
from tracer.schemas import GenerationResult

REPO_ROOT = Path(__file__).resolve().parents[1]


class FakeOllamaClient:
    def __init__(self, config):
        self.config = config

    def generate(self, prompt):
        return GenerationResult(
            response="```python\nx = 1\n```",
            latency_seconds=0.01,
            prompt_tokens=10,
            completion_tokens=5,
            model=self.config.name,
            model_digest="sha256:test",
            ollama_version="test",
        )


def _temporary_outputs(tmp_path: Path, prefix: str) -> OutputConfig:
    return OutputConfig(
        json_path=tmp_path / f"{prefix}_records.json",
        csv_path=tmp_path / f"{prefix}_records.csv",
        summary_path=tmp_path / f"{prefix}_summary.json",
    )


def test_end_to_end_runner_writes_standard_outputs(tmp_path, monkeypatch):
    config = load_config(REPO_ROOT / "configs/qwen25_coder_baseline.yaml")
    config = replace(config, output=_temporary_outputs(tmp_path, "qwen"))
    monkeypatch.setattr(run_baseline, "OllamaClient", FakeOllamaClient)

    records = run_baseline.run(config)

    assert len(records) == 20
    assert config.output.json_path.exists()
    assert config.output.csv_path.exists()
    assert config.output.summary_path.exists()
    first = json.loads(config.output.json_path.read_text(encoding="utf-8"))[0]
    assert first["question"]
    assert first["prompt"].startswith("You are a code-fixing assistant")
    assert first["model_digest"] == "sha256:test"
    assert "execution_stdout" in first
    assert "execution_stderr" in first
    assert "execution_exit_code" in first

    # TRACER-29: JSON, CSV, and summary must all preserve validator provenance.
    assert first["validator_config"]["backend"] == "docker"
    assert first["validator_config"]["network_mode"] == "none"
    with config.output.csv_path.open(encoding="utf-8", newline="") as csv_file:
        csv_first = next(csv.DictReader(csv_file))
    csv_validator = json.loads(csv_first["validator_config"])
    assert csv_validator["docker_image"] == "python:3.11-slim"
    assert csv_validator["python_isolated_mode"] is True

    summary = json.loads(config.output.summary_path.read_text(encoding="utf-8"))
    assert summary["sample_count"] == 20
    assert summary["manual_review_count"] == 20
    assert summary["validator_config"]["backend"] == "docker"
    assert summary["validator_config"]["pids_limit"] == 64

    # TRACER-31: the baseline summary freezes sample identity and host environment.
    assert len(summary["sample_ids"]) == 20
    assert summary["runtime_environment"]["os"]
    assert summary["runtime_environment"]["machine"]
    assert summary["runtime_environment"]["python_version"]


def test_disabled_validator_is_distinguishable_in_outputs(tmp_path, monkeypatch):
    config = load_config(REPO_ROOT / "configs/qwen25_coder_baseline.yaml")
    config = replace(
        config,
        validator=replace(config.validator, backend="disabled"),
        output=_temporary_outputs(tmp_path, "disabled"),
    )
    monkeypatch.setattr(run_baseline, "OllamaClient", FakeOllamaClient)

    run_baseline.run(config)

    first = json.loads(config.output.json_path.read_text(encoding="utf-8"))[0]
    summary = json.loads(config.output.summary_path.read_text(encoding="utf-8"))
    assert first["validator_config"]["backend"] == "disabled"
    assert first["validator_config"]["execution_enabled"] is False
    assert summary["validator_config"]["backend"] == "disabled"
