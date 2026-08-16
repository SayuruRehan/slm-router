from tracer.validators.extraction import extract_code


def test_extracts_python_fence():
    assert extract_code("before\n```python\nprint('ok')\n```\nafter") == "print('ok')"


def test_extracts_unlabelled_fence():
    assert extract_code("```\nx = 1\n```") == "x = 1"


def test_falls_back_to_raw_text():
    assert extract_code("  x = 1  ") == "x = 1"


def test_empty_response_stays_empty():
    assert extract_code("   ") == ""

