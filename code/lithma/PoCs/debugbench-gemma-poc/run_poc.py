"""Deprecated Gemma PoC entry point that delegates to the canonical TRACER runner."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
CONFIG_PATH = REPO_ROOT / "configs" / "gemma3_baseline.yaml"


def main() -> int:
    # TRACER-30: prevent the legacy PoC from writing a conflicting results.json path.
    cli = shutil.which("tracer-baseline")
    if cli is None:
        print('Install the project first: pip install -e ".[dev,viewer]"')
        return 127

    print(
        "TRACER-30: debugbench-gemma-poc/run_poc.py is deprecated; "
        "using tracer-baseline instead."
    )
    completed = subprocess.run(
        [cli, "--config", str(CONFIG_PATH)],
        cwd=REPO_ROOT,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
