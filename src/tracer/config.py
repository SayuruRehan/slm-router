"""Validated YAML configuration for a TRACER baseline experiment."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class ConfigError(ValueError):
    """Raised when an experiment configuration is incomplete or invalid."""


@dataclass(frozen=True)
class DatasetConfig:
    path: Path
    manifest: Path


@dataclass(frozen=True)
class ModelConfig:
    name: str
    base_url: str = "http://localhost:11434"
    timeout_seconds: float = 300.0
    options: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PromptConfig:
    version: str = "debugbench-code-repair-v1"


@dataclass(frozen=True)
class ValidatorConfig:
    backend: str = "docker"
    docker_image: str = "python:3.11-slim"
    timeout_seconds: float = 10.0
    memory_mb: int = 256
    cpu_limit: float = 0.5
    pids_limit: int = 64

    def to_metadata(self) -> dict[str, Any]:
        """Return the effective validator settings that produced an experiment label."""

        # TRACER-29: persist the effective validator provenance with every result.
        if self.backend == "disabled":
            return {
                "backend": "disabled",
                "execution_enabled": False,
                "docker_image": None,
                "timeout_seconds": None,
                "memory_mb": None,
                "cpu_limit": None,
                "pids_limit": None,
                "network_mode": None,
                "read_only_root": None,
                "workspace_read_only": None,
                "cap_drop": None,
                "no_new_privileges": None,
                "tmpfs": None,
                "python_isolated_mode": None,
                "python_no_bytecode": None,
            }

        return {
            "backend": "docker",
            "execution_enabled": True,
            "docker_image": self.docker_image,
            "timeout_seconds": self.timeout_seconds,
            "memory_mb": self.memory_mb,
            "cpu_limit": self.cpu_limit,
            "pids_limit": self.pids_limit,
            "network_mode": "none",
            "read_only_root": True,
            "workspace_read_only": True,
            "cap_drop": ["ALL"],
            "no_new_privileges": True,
            "tmpfs": "/tmp:rw,noexec,nosuid,size=64m",
            "python_isolated_mode": True,
            "python_no_bytecode": True,
        }


@dataclass(frozen=True)
class OutputConfig:
    json_path: Path
    csv_path: Path
    summary_path: Path


@dataclass(frozen=True)
class ExperimentConfig:
    name: str
    version: str
    dataset: DatasetConfig
    model: ModelConfig
    prompt: PromptConfig
    validator: ValidatorConfig
    output: OutputConfig
    config_path: Path
    repo_root: Path


def _required(mapping: dict[str, Any], key: str, section: str) -> Any:
    value = mapping.get(key)
    if value is None or value == "":
        raise ConfigError(f"Missing required value: {section}.{key}")
    return value


def _repo_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def load_config(path: str | Path) -> ExperimentConfig:
    config_path = Path(path).resolve()
    if not config_path.exists():
        raise ConfigError(f"Configuration file does not exist: {config_path}")

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ConfigError("The configuration root must be a mapping")

    repo_root = config_path.parent.parent
    experiment = raw.get("experiment") or {}
    dataset = raw.get("dataset") or {}
    model = raw.get("model") or {}
    prompt = raw.get("prompt") or {}
    validator = raw.get("validator") or {}
    output = raw.get("output") or {}

    backend = str(validator.get("backend", "docker"))
    if backend not in {"docker", "disabled"}:
        raise ConfigError("validator.backend must be 'docker' or 'disabled'")

    model_options = model.get("options") or {}
    if not isinstance(model_options, dict):
        raise ConfigError("model.options must be a mapping")

    return ExperimentConfig(
        name=str(_required(experiment, "name", "experiment")),
        version=str(_required(experiment, "version", "experiment")),
        dataset=DatasetConfig(
            path=_repo_path(repo_root, str(_required(dataset, "path", "dataset"))),
            manifest=_repo_path(repo_root, str(_required(dataset, "manifest", "dataset"))),
        ),
        model=ModelConfig(
            name=str(_required(model, "name", "model")),
            base_url=str(model.get("base_url", "http://localhost:11434")).rstrip("/"),
            timeout_seconds=float(model.get("timeout_seconds", 300)),
            options=model_options,
        ),
        prompt=PromptConfig(version=str(prompt.get("version", "debugbench-code-repair-v1"))),
        validator=ValidatorConfig(
            backend=backend,
            docker_image=str(validator.get("docker_image", "python:3.11-slim")),
            timeout_seconds=float(validator.get("timeout_seconds", 10)),
            memory_mb=int(validator.get("memory_mb", 256)),
            cpu_limit=float(validator.get("cpu_limit", 0.5)),
            pids_limit=int(validator.get("pids_limit", 64)),
        ),
        output=OutputConfig(
            json_path=_repo_path(repo_root, str(_required(output, "json_path", "output"))),
            csv_path=_repo_path(repo_root, str(_required(output, "csv_path", "output"))),
            summary_path=_repo_path(
                repo_root, str(_required(output, "summary_path", "output"))
            ),
        ),
        config_path=config_path,
        repo_root=repo_root,
    )
