"""Canonical prompt used by the comparable DebugBench baselines."""

from tracer.schemas import DebugBenchSample

SUPPORTED_PROMPT_VERSION = "debugbench-code-repair-v1"


def build_code_repair_prompt(sample: DebugBenchSample, version: str) -> str:
    if version != SUPPORTED_PROMPT_VERSION:
        raise ValueError(
            f"Unsupported prompt version {version!r}; expected {SUPPORTED_PROMPT_VERSION!r}"
        )
    return f"""You are a code-fixing assistant. The following Python solution has a bug.

Problem:
{sample.question}

Buggy code:
```python
{sample.buggy_code}
```

Fix the bug. Respond with only the complete corrected code in one Python code block.
Do not include an explanation."""

