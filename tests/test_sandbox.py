from pathlib import Path

from tracer.config import ValidatorConfig
from tracer.validators.execution import DockerPythonSandbox


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

