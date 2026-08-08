"""Small, testable adapter for Ollama's generate API."""

from __future__ import annotations

import time
from typing import Any

import requests

from tracer.config import ModelConfig
from tracer.schemas import GenerationResult


class OllamaError(RuntimeError):
    """Raised when Ollama cannot complete an experiment request."""


class OllamaClient:
    def __init__(self, config: ModelConfig, session: requests.Session | None = None):
        self.config = config
        self.session = session or requests.Session()
        self._cached_server_version: str | None = None
        self._server_version_loaded = False
        self._cached_model_digest: str | None = None
        self._model_digest_loaded = False

    def _get_json(self, path: str) -> dict[str, Any]:
        response = self.session.get(
            f"{self.config.base_url}{path}", timeout=min(self.config.timeout_seconds, 10)
        )
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, dict) else {}

    def server_version(self) -> str | None:
        if self._server_version_loaded:
            return self._cached_server_version
        try:
            self._cached_server_version = self._get_json("/api/version").get("version")
        except (requests.RequestException, ValueError):
            self._cached_server_version = None
        self._server_version_loaded = True
        return self._cached_server_version

    def model_digest(self) -> str | None:
        if self._model_digest_loaded:
            return self._cached_model_digest
        try:
            tags = self._get_json("/api/tags")
        except (requests.RequestException, ValueError):
            tags = {}
        self._cached_model_digest = next(
            (
                model.get("digest")
                for model in tags.get("models", [])
                if model.get("name") == self.config.name
                or model.get("model") == self.config.name
            ),
            None,
        )
        self._model_digest_loaded = True
        return self._cached_model_digest

    def generate(self, prompt: str) -> GenerationResult:
        payload = {
            "model": self.config.name,
            "prompt": prompt,
            "stream": False,
            # Ollama generation controls belong in `options`, not at the top level.
            "options": dict(self.config.options),
        }
        started = time.monotonic()
        try:
            response = self.session.post(
                f"{self.config.base_url}/api/generate",
                json=payload,
                timeout=self.config.timeout_seconds,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise OllamaError(
                f"Ollama request failed for {self.config.name!r} at "
                f"{self.config.base_url}: {exc}"
            ) from exc

        if not isinstance(data, dict) or "response" not in data:
            raise OllamaError("Ollama returned an unexpected response body")
        return GenerationResult(
            response=str(data.get("response", "")),
            latency_seconds=time.monotonic() - started,
            prompt_tokens=data.get("prompt_eval_count"),
            completion_tokens=data.get("eval_count"),
            model=self.config.name,
            model_digest=self.model_digest(),
            ollama_version=self.server_version(),
        )
