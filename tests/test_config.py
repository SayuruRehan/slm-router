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


def test_rejects_missing_required_values(tmp_path):
    config_dir = tmp_path / "configs"
    config_dir.mkdir()
    invalid = config_dir / "invalid.yaml"
    invalid.write_text("experiment:\n  name: missing-version\n", encoding="utf-8")

    with pytest.raises(ConfigError, match="experiment.version"):
        load_config(invalid)

