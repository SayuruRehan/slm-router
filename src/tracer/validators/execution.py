"""Execute generated Python only inside a resource-limited Docker container."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from tracer.config import ValidatorConfig
from tracer.schemas import ExecutionResult


class SandboxUnavailableError(RuntimeError):
    """Raised when test execution is requested but Docker is unavailable."""


class DockerPythonSandbox:
    """A deliberately restrictive runner for untrusted model output.

    This is not a claim of perfect isolation. Keep Docker patched and use a
    dedicated research machine. The runner disables networking, limits CPU,
    memory and processes, and mounts the generated files read-only.
    """

    def __init__(self, config: ValidatorConfig):
        self.config = config

    def available(self) -> bool:
        return shutil.which("docker") is not None

    def build_command(self, workspace: Path) -> list[str]:
        return [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
            "--memory",
            f"{self.config.memory_mb}m",
            "--cpus",
            str(self.config.cpu_limit),
            "--pids-limit",
            str(self.config.pids_limit),
            "--read-only",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=64m",
            "--mount",
            f"type=bind,src={workspace.resolve()},dst=/workspace,readonly",
            "--workdir",
            "/workspace",
            self.config.docker_image,
            "python",
            "-I",
            "-B",
            "test_runner.py",
        ]

    def run(self, candidate_code: str, test_code: str) -> ExecutionResult:
        if not self.available():
            raise SandboxUnavailableError(
                "Docker is required for executing generated code. Install Docker or disable "
                "execution; TRACER will not run untrusted code directly on the host."
            )

        with tempfile.TemporaryDirectory(prefix="tracer-validation-") as temp_directory:
            workspace = Path(temp_directory)
            (workspace / "candidate.py").write_text(candidate_code, encoding="utf-8")
            runner = "from candidate import *  # noqa: F403\n\n" + test_code + "\n"
            (workspace / "test_runner.py").write_text(runner, encoding="utf-8")
            started = time.monotonic()
            try:
                completed = subprocess.run(
                    self.build_command(workspace),
                    capture_output=True,
                    text=True,
                    timeout=self.config.timeout_seconds,
                    check=False,
                )
            except subprocess.TimeoutExpired as exc:
                return ExecutionResult(
                    attempted=True,
                    passed=False,
                    status="timeout",
                    duration_seconds=time.monotonic() - started,
                    stdout=(exc.stdout or "")[-10_000:],
                    stderr=(exc.stderr or "")[-10_000:],
                )
            duration = time.monotonic() - started
            return ExecutionResult(
                attempted=True,
                passed=completed.returncode == 0,
                status="passed" if completed.returncode == 0 else "failed",
                exit_code=completed.returncode,
                duration_seconds=duration,
                stdout=completed.stdout[-10_000:],
                stderr=completed.stderr[-10_000:],
            )

