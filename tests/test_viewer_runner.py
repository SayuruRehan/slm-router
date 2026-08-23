from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tracer.experiments import viewer_runner


# TRACER-30: test the shared viewer contract instead of executing Streamlit at import time.
def test_viewer_runner_requires_canonical_cli(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(viewer_runner.shutil, "which", lambda _name: None)

    with pytest.raises(viewer_runner.BaselineCliUnavailableError):
        viewer_runner.run_canonical_baseline(
            tmp_path / "config.yaml",
            tmp_path / "records.json",
            tmp_path,
        )


def test_viewer_runner_reports_success_only_for_refreshed_expected_file(
    tmp_path: Path, monkeypatch
):
    results = tmp_path / "records.json"
    config = tmp_path / "config.yaml"
    config.write_text("experiment: {}\n", encoding="utf-8")
    monkeypatch.setattr(viewer_runner.shutil, "which", lambda _name: "/bin/tracer-baseline")

    def fake_run(*_args, **_kwargs):
        results.write_text("[]\n", encoding="utf-8")
        return subprocess.CompletedProcess([], 0, stdout="ok", stderr="")

    monkeypatch.setattr(viewer_runner.subprocess, "run", fake_run)
    outcome = viewer_runner.run_canonical_baseline(config, results, tmp_path)

    assert outcome.success is True
    assert outcome.output_exists is True
    assert outcome.output_refreshed is True


def test_viewer_runner_rejects_stale_output_even_when_cli_exits_zero(
    tmp_path: Path, monkeypatch
):
    results = tmp_path / "records.json"
    results.write_text("[]\n", encoding="utf-8")
    config = tmp_path / "config.yaml"
    config.write_text("experiment: {}\n", encoding="utf-8")
    monkeypatch.setattr(viewer_runner.shutil, "which", lambda _name: "/bin/tracer-baseline")
    monkeypatch.setattr(
        viewer_runner.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess([], 0, stdout="ok", stderr=""),
    )

    outcome = viewer_runner.run_canonical_baseline(config, results, tmp_path)

    assert outcome.returncode == 0
    assert outcome.output_exists is True
    assert outcome.output_refreshed is False
    assert outcome.success is False
