from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tracer.config import ValidatorConfig
from tracer.validators.execution import DockerPythonSandbox


# TRACER-28: retain every pre-existing Docker isolation assertion while fixing imports.
def test_docker_command_has_required_isolation_controls(tmp_path: Path):
    command = DockerPythonSandbox(ValidatorConfig()).build_command(tmp_path)
    joined = " ".join(command)

    assert "--network none" in joined
    assert "--read-only" in command
    assert "--cap-drop ALL" in joined
    assert "no-new-privileges" in command
    assert "--memory 256m" in joined
    assert "--pids-limit 64" in joined
    assert "readonly" in joined
    assert "python -I -B test_runner.py" in joined


def test_old_isolated_import_reproduces_module_not_found(tmp_path: Path):
    """Document the TRACER-28 regression that the old runner triggered."""

    (tmp_path / "candidate.py").write_text("VALUE = 42\n", encoding="utf-8")
    legacy_runner = tmp_path / "legacy_runner.py"
    legacy_runner.write_text(
        "from candidate import VALUE\nassert VALUE == 42\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [sys.executable, "-I", "-B", str(legacy_runner)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode != 0
    assert "ModuleNotFoundError" in completed.stderr
    assert "candidate" in completed.stderr


def test_explicit_path_runner_works_under_isolated_mode(tmp_path: Path):
    """The TRACER-28 runner must work without adding the workspace to sys.path."""

    candidate = tmp_path / "candidate.py"
    candidate.write_text("VALUE = 42\n", encoding="utf-8")
    runner = tmp_path / "runner.py"
    source = DockerPythonSandbox(ValidatorConfig()).build_runner_source(
        "assert VALUE == 42",
        candidate_path=str(candidate),
    )
    runner.write_text(source, encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, "-I", "-B", str(runner)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "from candidate import" not in source
    assert "spec_from_file_location" in source


@pytest.fixture(scope="module")
def docker_image() -> str:
    """Make Docker execution tests deterministic when Docker is available."""

    if shutil.which("docker") is None:
        pytest.skip("Docker is not available for TRACER-28 integration tests")

    image = "python:3.11-slim"
    inspect = subprocess.run(
        ["docker", "image", "inspect", image],
        capture_output=True,
        text=True,
        check=False,
    )
    if inspect.returncode != 0:
        try:
            pull = subprocess.run(
                ["docker", "pull", image],
                capture_output=True,
                text=True,
                timeout=180,
                check=False,
            )
        except subprocess.TimeoutExpired:
            pytest.skip("Timed out pulling the Docker image for TRACER-28 tests")
        if pull.returncode != 0:
            pytest.skip(f"Could not pull {image}: {pull.stderr[-500:]}")
    return image


def test_known_correct_candidate_passes_in_isolated_container(docker_image: str):
    sandbox = DockerPythonSandbox(
        ValidatorConfig(docker_image=docker_image, timeout_seconds=30)
    )
    result = sandbox.run(
        "def add(a, b):\n    return a + b\n",
        "assert add(2, 3) == 5\nassert add(-1, 1) == 0",
    )

    assert result.attempted is True
    assert result.passed is True
    assert result.status == "passed"


def test_known_incorrect_candidate_fails_for_assertion(docker_image: str):
    sandbox = DockerPythonSandbox(
        ValidatorConfig(docker_image=docker_image, timeout_seconds=30)
    )
    result = sandbox.run(
        "def add(a, b):\n    return a - b\n",
        "assert add(2, 3) == 5",
    )

    assert result.attempted is True
    assert result.passed is False
    assert result.status == "failed"
    assert "AssertionError" in result.stderr
    assert "ModuleNotFoundError" not in result.stderr


def test_syntax_error_candidate_fails_in_isolated_container(docker_image: str):
    sandbox = DockerPythonSandbox(
        ValidatorConfig(docker_image=docker_image, timeout_seconds=30)
    )
    result = sandbox.run(
        "def add(a, b)\n    return a + b\n",
        "assert True",
    )

    assert result.attempted is True
    assert result.passed is False
    assert result.status == "failed"
    assert "SyntaxError" in result.stderr


def test_timeout_candidate_is_terminated(docker_image: str):
    sandbox = DockerPythonSandbox(
        ValidatorConfig(docker_image=docker_image, timeout_seconds=2)
    )
    result = sandbox.run(
        "def run_forever():\n    while True:\n        pass\n",
        "run_forever()",
    )

    assert result.attempted is True
    assert result.passed is False
    assert result.status == "timeout"
