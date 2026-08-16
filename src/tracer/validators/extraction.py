"""Extract code from common language-model response formats."""

import re

FENCED_BLOCK = re.compile(
    r"```[ \t]*(?:python|python3|py)?[ \t]*\r?\n?(.*?)```", re.IGNORECASE | re.DOTALL
)


def extract_code(raw_response: str) -> str:
    """Return the first fenced code block, or the stripped raw response."""

    match = FENCED_BLOCK.search(raw_response)
    if match:
        return match.group(1).strip()
    return raw_response.strip()

