from pathlib import Path

import pytest

from tracer.datasets.debugbench import DatasetError, load_manifest_samples

REPO_ROOT = Path(__file__).resolve().parents[1]
DATASET = REPO_ROOT / "benchmarking/data/debugbench_full.json"
MANIFEST = REPO_ROOT / "sample_manifests/debugbench_python_first_20.json"


def test_manifest_selects_fixed_python_samples():
    samples = load_manifest_samples(DATASET, MANIFEST)

    assert len(samples) == 20
    assert samples[0].dataset_index == 2839
    assert samples[0].slug == "moving-stones-until-consecutive-ii"
    assert samples[-1].dataset_index == 2858
    assert all(sample.language == "python3" for sample in samples)


def test_manifest_identity_mismatch_fails(tmp_path):
    bad_manifest = tmp_path / "manifest.json"
    bad_manifest.write_text(
        '{"samples":[{"dataset_index":2839,"slug":"wrong","language":"python3"}]}',
        encoding="utf-8",
    )

    with pytest.raises(DatasetError, match="Manifest mismatch"):
        load_manifest_samples(DATASET, bad_manifest)

