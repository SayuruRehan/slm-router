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


def test_end_to_end_runner_writes_standard_outputs(tmp_path, monkeypatch):
    config = load_config(REPO_ROOT / "configs/qwen25_coder_baseline.yaml")
    config = replace(
        config,
        output=OutputConfig(
            json_path=tmp_path / "records.json",
            csv_path=tmp_path / "records.csv",
            summary_path=tmp_path / "summary.json",
        ),
    )
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
    summary = json.loads(config.output.summary_path.read_text(encoding="utf-8"))
    assert summary["sample_count"] == 20
    assert summary["manual_review_count"] == 20
