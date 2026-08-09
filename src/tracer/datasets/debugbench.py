"""Load a fixed, versioned subset of the cached DebugBench dataset."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from tracer.schemas import DebugBenchSample


class DatasetError(ValueError):
    """Raised when the cached dataset and sample manifest do not agree."""


def dataset_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as dataset_file:
        for chunk in iter(lambda: dataset_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    if not path.exists():
        raise DatasetError(f"Required file does not exist: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DatasetError(f"Invalid JSON in {path}: {exc}") from exc


def load_manifest_samples(
    dataset_path: str | Path, manifest_path: str | Path
) -> list[DebugBenchSample]:
    """Return samples in manifest order and fail on any identity mismatch."""

    dataset_file = Path(dataset_path)
    manifest_file = Path(manifest_path)
    dataset = _read_json(dataset_file)
    manifest = _read_json(manifest_file)

    if not isinstance(dataset, list):
        raise DatasetError("DebugBench cache must contain a JSON list")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("samples"), list):
        raise DatasetError("Manifest must contain a 'samples' list")

    expected_sha = manifest.get("dataset_sha256")
    if expected_sha and dataset_sha256(dataset_file) != expected_sha:
        raise DatasetError(
            "Dataset checksum does not match the manifest. Do not silently run a different dataset."
        )

    samples: list[DebugBenchSample] = []
    seen_indexes: set[int] = set()
    seen_slugs: set[str] = set()
    for position, entry in enumerate(manifest["samples"]):
        if not isinstance(entry, dict):
            raise DatasetError(f"Manifest sample {position} must be an object")
        try:
            index = int(entry["dataset_index"])
            expected_slug = str(entry["slug"])
            expected_language = str(entry["language"])
            row = dataset[index]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise DatasetError(f"Invalid manifest sample at position {position}") from exc

        if index in seen_indexes or expected_slug in seen_slugs:
            raise DatasetError(f"Duplicate sample in manifest: {expected_slug}")
        if row.get("slug") != expected_slug or row.get("language") != expected_language:
            raise DatasetError(
                f"Manifest mismatch at dataset index {index}: expected "
                f"{expected_slug}/{expected_language}, found "
                f"{row.get('slug')}/{row.get('language')}"
            )

        seen_indexes.add(index)
        seen_slugs.add(expected_slug)
        samples.append(
            DebugBenchSample(
                dataset_index=index,
                slug=expected_slug,
                language=expected_language,
                category=str(row.get("category", "")),
                subtype=str(row.get("subtype", "")),
                question=str(row["question"]),
                buggy_code=str(row["buggy_code"]),
                reference_solution=str(row["solution"]),
                test_code=entry.get("test_code"),
            )
        )
    if not samples:
        raise DatasetError("The manifest contains no samples")
    return samples

