"""Deprecated Qwen PoC entry point that delegates to the canonical TRACER runner."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "configs" / "qwen25_coder_baseline.yaml"


def main() -> int:
    # TRACER-30: keep this legacy command only as a compatibility wrapper.
    cli = shutil.which("tracer-baseline")
    if cli is None:
        print('Install the project first: pip install -e ".[dev,viewer]"')
        return 127

    print("TRACER-30: code/sula/run.py is deprecated; using tracer-baseline instead.")
    completed = subprocess.run(
        [cli, "--config", str(CONFIG_PATH)],
        cwd=REPO_ROOT,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
