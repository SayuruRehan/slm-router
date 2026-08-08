from tracer.config import ValidatorConfig
from tracer.validators.python import validate_python_response

CONFIG = ValidatorConfig(backend="disabled")
BUGGY = "def add(a, b):\n    return a - b"
REFERENCE = "def add(a, b):\n    return a + b"


def validate(candidate):
    return validate_python_response(candidate, BUGGY, REFERENCE, None, CONFIG)


def test_empty_is_definitively_invalid():
    result = validate("")
    assert result.outcome == "empty_response"
    assert result.correctness is False


def test_syntax_error_is_definitively_invalid():
    result = validate("def broken(")
    assert result.outcome == "syntax_error"
    assert result.correctness is False


def test_unchanged_response_is_a_distinct_failure():
    result = validate(BUGGY)
    assert result.outcome == "no_change"
    assert result.correctness is False
    assert result.unchanged is True


def test_reference_ast_match_is_labelled_as_reference_evidence():
    result = validate("def add(a,b):\n return a+b")
    assert result.outcome == "reference_match"
    assert result.correctness is True
    assert result.label_source == "reference_ast"


def test_alternative_parsing_solution_requires_review_without_tests():
    result = validate("def add(a, b):\n    return sum((a, b))")
    assert result.outcome == "needs_manual_review"
    assert result.correctness is None
    assert result.needs_manual_review is True

