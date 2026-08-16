"""Non-executing diagnostics for Python responses."""

from __future__ import annotations

import ast
from collections import Counter


def normalized_ast(code: str) -> str:
    return ast.dump(ast.parse(code), annotate_fields=False)


def parses(code: str) -> bool:
    try:
        ast.parse(code)
    except (SyntaxError, ValueError, TypeError):
        return False
    return True


def ast_equal(first: str, second: str) -> bool:
    try:
        return normalized_ast(first) == normalized_ast(second)
    except (SyntaxError, ValueError, TypeError):
        return False


def unchanged_from_buggy(candidate: str, buggy_code: str) -> bool:
    if parses(candidate) and parses(buggy_code):
        return ast_equal(candidate, buggy_code)
    return candidate.strip() == buggy_code.strip()


def char_ngram_cosine(first: str, second: str, n: int = 3) -> float:
    """Diagnostic similarity only; it must never be used as a correctness label."""

    def vector(text: str) -> Counter[str]:
        return Counter(text[index : index + n] for index in range(len(text) - n + 1))

    first_vector = vector(first)
    second_vector = vector(second)
    common = set(first_vector) & set(second_vector)
    dot = sum(first_vector[key] * second_vector[key] for key in common)
    first_norm = sum(value * value for value in first_vector.values()) ** 0.5
    second_norm = sum(value * value for value in second_vector.values()) ** 0.5
    if first_norm == 0 or second_norm == 0:
        return 0.0
    return dot / (first_norm * second_norm)

