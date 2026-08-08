from pathlib import Path

from tracer.experiments.run_baseline import main

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_dry_run_validates_without_ollama(capsys):
    exit_code = main(
        ["--config", str(REPO_ROOT / "configs/gemma3_baseline.yaml"), "--dry-run"]
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Samples: 20" in output
    assert "Dry run complete" in output

