"""Shared helpers for launching canonical TRACER baseline runs from viewers."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class BaselineCliUnavailableError(RuntimeError):
    """Raised when the installed ``tracer-baseline`` entry point cannot be found."""


@dataclass(frozen=True)
class ViewerRunResult:
    returncode: int
    stdout: str
    stderr: str
    output_exists: bool
    output_refreshed: bool

    @property
    def success(self) -> bool:
        return self.returncode == 0 and self.output_exists and self.output_refreshed


def run_canonical_baseline(
    config_path: Path,
    results_path: Path,
    repo_root: Path,
) -> ViewerRunResult:
    """Run ``tracer-baseline`` and verify that its expected output was refreshed."""

    # TRACER-30: viewer success depends on the canonical CLI and the expected file,
    # not merely on a legacy subprocess returning exit code zero.
    cli = shutil.which("tracer-baseline")
    if cli is None:
        raise BaselineCliUnavailableError(
            '`tracer-baseline` is not installed. Run: pip install -e ".[dev,viewer]"'
        )

    previous_mtime = results_path.stat().st_mtime_ns if results_path.exists() else None
    completed = subprocess.run(
        [cli, "--config", str(config_path)],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    output_exists = results_path.exists()
    current_mtime = results_path.stat().st_mtime_ns if output_exists else None
    output_refreshed = current_mtime is not None and current_mtime != previous_mtime
    return ViewerRunResult(
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        output_exists=output_exists,
        output_refreshed=output_refreshed,
    )
