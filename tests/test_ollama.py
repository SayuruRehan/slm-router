from tracer.config import ModelConfig
from tracer.models.ollama import OllamaClient


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self.data


class FakeSession:
    def __init__(self):
        self.post_payload = None

    def post(self, url, json, timeout):
        self.post_payload = json
        return FakeResponse(
            {"response": "```python\nx = 1\n```", "prompt_eval_count": 10, "eval_count": 5}
        )

    def get(self, url, timeout):
        if url.endswith("/api/version"):
            return FakeResponse({"version": "test-version"})
        return FakeResponse({"models": [{"name": "test:1b", "digest": "sha256:test"}]})


def test_generation_controls_are_nested_under_options():
    session = FakeSession()
    config = ModelConfig(
        name="test:1b",
        options={"temperature": 0, "seed": 42, "num_predict": 512},
    )

    result = OllamaClient(config, session=session).generate("hello")

    assert session.post_payload == {
        "model": "test:1b",
        "prompt": "hello",
        "stream": False,
        "options": {"temperature": 0, "seed": 42, "num_predict": 512},
    }
    assert result.model_digest == "sha256:test"
    assert result.ollama_version == "test-version"

