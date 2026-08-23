from dataclasses import replace
from pathlib import Path

import pytest

from tracer.config import ConfigError, load_config

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_loads_qwen_config_with_repo_relative_paths():
    config = load_config(REPO_ROOT / "configs/qwen25_coder_baseline.yaml")

    assert config.model.name == "qwen2.5-coder:1.5b"
    assert config.model.options == {"temperature": 0, "seed": 42, "num_predict": 512}
    assert config.dataset.path == REPO_ROOT / "benchmarking/data/debugbench_full.json"
    assert config.validator.backend == "docker"


def test_validator_metadata_records_effective_isolation_policy():
    config = load_config(REPO_ROOT / "configs/qwen25_coder_baseline.yaml")

    # TRACER-29: validator provenance must identify every effective isolation control.
    metadata = config.validator.to_metadata()
    assert metadata["backend"] == "docker"
    assert metadata["docker_image"] == "python:3.11-slim"
    assert metadata["timeout_seconds"] == 10
    assert metadata["memory_mb"] == 256
    assert metadata["cpu_limit"] == 0.5
    assert metadata["pids_limit"] == 64
    assert metadata["network_mode"] == "none"
    assert metadata["read_only_root"] is True
    assert metadata["workspace_read_only"] is True
    assert metadata["cap_drop"] == ["ALL"]
    assert metadata["no_new_privileges"] is True
    assert metadata["python_isolated_mode"] is True


def test_disabled_validator_metadata_is_unambiguous():
    config = load_config(REPO_ROOT / "configs/qwen25_coder_baseline.yaml")
    disabled = replace(config.validator, backend="disabled")

    metadata = disabled.to_metadata()
    assert metadata["backend"] == "disabled"
    assert metadata["execution_enabled"] is False
    assert metadata["docker_image"] is None
    assert metadata["network_mode"] is None


def test_rejects_missing_required_values(tmp_path):
    config_dir = tmp_path / "configs"
    config_dir.mkdir()
    invalid = config_dir / "invalid.yaml"
    invalid.write_text("experiment:\n  name: missing-version\n", encoding="utf-8")

    with pytest.raises(ConfigError, match="experiment.version"):
        load_config(invalid)


def test_tracer31_qwen_and_gemma_configs_share_frozen_controls():
    # TRACER-31: model identity is the only intended experimental difference.
    qwen = load_config(REPO_ROOT / "configs/qwen25_coder_baseline.yaml")
    gemma = load_config(REPO_ROOT / "configs/gemma3_baseline.yaml")

    assert qwen.dataset.path == gemma.dataset.path
    assert qwen.dataset.manifest == gemma.dataset.manifest
    assert qwen.prompt.version == gemma.prompt.version
    assert qwen.model.options == gemma.model.options
    assert qwen.validator.to_metadata() == gemma.validator.to_metadata()
    assert qwen.model.name != gemma.model.name
    assert qwen.output.json_path.name == "qwen25_coder_records.json"
    assert gemma.output.json_path.name == "gemma3_records.json"
