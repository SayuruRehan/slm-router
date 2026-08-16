"""Serializable schemas shared by datasets, models, validators, and experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class DebugBenchSample:
    dataset_index: int
    slug: str
    language: str
    category: str
    subtype: str
    question: str
    buggy_code: str
    reference_solution: str
    test_code: str | None = None


@dataclass(frozen=True)
class GenerationResult:
    response: str
    latency_seconds: float
    prompt_tokens: int | None
    completion_tokens: int | None
    model: str
    model_digest: str | None = None
    ollama_version: str | None = None


@dataclass(frozen=True)
class ExecutionResult:
    attempted: bool
    passed: bool | None
    status: str
    exit_code: int | None = None
    duration_seconds: float | None = None
    stdout: str = ""
    stderr: str = ""


@dataclass(frozen=True)
class ValidationResult:
    outcome: str
    correctness: bool | None
    label_source: str
    needs_manual_review: bool
    parses: bool
    unchanged: bool
    reference_ast_match: bool
    execution: ExecutionResult = field(
        default_factory=lambda: ExecutionResult(False, None, "not_attempted")
    )


@dataclass
class ExperimentRecord:
    run_id: str
    experiment_name: str
    experiment_version: str
    prompt_version: str
    dataset_sha256: str
    sample_manifest: str
    index: int
    dataset_index: int
    slug: str
    language: str
    category: str
    subtype: str
    question: str
    buggy_code: str
    reference_solution: str
    prompt: str
    raw_response: str
    extracted_code: str
    model: str
    model_digest: str | None
    ollama_version: str | None
    generation_options: dict[str, Any]
    latency_sec: float
    prompt_tokens: int | None
    eval_tokens: int | None
    outcome: str
    correctness: bool | None
    label_source: str
    needs_manual_review: bool
    check_a_correct: bool
    check_b_unchanged: bool
    check_c_cosine_diagnostic_only: float
    parses: bool
    execution_status: str
    execution_passed: bool | None
    manual_verdict: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
