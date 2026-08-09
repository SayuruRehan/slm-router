"""Combine syntax, unchanged, reference, execution, and review signals."""

from __future__ import annotations

from tracer.config import ValidatorConfig
from tracer.schemas import ExecutionResult, ValidationResult
from tracer.validators.ast_checks import ast_equal, parses, unchanged_from_buggy
from tracer.validators.execution import DockerPythonSandbox, SandboxUnavailableError


def validate_python_response(
    candidate_code: str,
    buggy_code: str,
    reference_solution: str,
    test_code: str | None,
    validator_config: ValidatorConfig,
) -> ValidationResult:
    if not candidate_code.strip():
        return ValidationResult(
            outcome="empty_response",
            correctness=False,
            label_source="static_validation",
            needs_manual_review=False,
            parses=False,
            unchanged=False,
            reference_ast_match=False,
        )

    candidate_parses = parses(candidate_code)
    if not candidate_parses:
        return ValidationResult(
            outcome="syntax_error",
            correctness=False,
            label_source="static_validation",
            needs_manual_review=False,
            parses=False,
            unchanged=False,
            reference_ast_match=False,
        )

    unchanged = unchanged_from_buggy(candidate_code, buggy_code)
    reference_match = ast_equal(candidate_code, reference_solution)
    if not test_code:
        execution = ExecutionResult(False, None, "no_tests_available")
    elif validator_config.backend == "disabled":
        execution = ExecutionResult(False, None, "execution_disabled")
    else:
        execution = ExecutionResult(False, None, "not_attempted")

    if test_code and validator_config.backend == "docker":
        try:
            execution = DockerPythonSandbox(validator_config).run(candidate_code, test_code)
        except SandboxUnavailableError:
            execution = ExecutionResult(False, None, "sandbox_unavailable")
        if execution.attempted:
            return ValidationResult(
                outcome="test_passed" if execution.passed else "test_failed",
                correctness=execution.passed,
                label_source="sandboxed_tests",
                needs_manual_review=False,
                parses=True,
                unchanged=unchanged,
                reference_ast_match=reference_match,
                execution=execution,
            )

    if unchanged:
        return ValidationResult(
            outcome="no_change",
            correctness=False,
            label_source="static_validation",
            needs_manual_review=False,
            parses=True,
            unchanged=True,
            reference_ast_match=reference_match,
            execution=execution,
        )
    if reference_match:
        return ValidationResult(
            outcome="reference_match",
            correctness=True,
            label_source="reference_ast",
            needs_manual_review=False,
            parses=True,
            unchanged=False,
            reference_ast_match=True,
            execution=execution,
        )
    return ValidationResult(
        outcome="needs_manual_review",
        correctness=None,
        label_source="unresolved_without_tests",
        needs_manual_review=True,
        parses=True,
        unchanged=False,
        reference_ast_match=False,
        execution=execution,
    )
