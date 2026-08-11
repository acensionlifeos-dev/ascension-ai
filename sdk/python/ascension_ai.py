"""Truthful Python client for the Ascension AI native intelligence core."""

from __future__ import annotations

from typing import Any

import requests


class AscensionAI:
    """Client for native conversation, cognition, retrieval, and action planning."""

    def __init__(self, api_key: str, base_url: str = "https://ascension-ai.onrender.com", timeout: int = 180):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def _get(self, path: str) -> dict[str, Any]:
        response = self.session.get(f"{self.base_url}{path}", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(f"{self.base_url}{path}", json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        shell: str = "ap",
        tier: str = "lifeos",
        context: dict[str, Any] | None = None,
        surface: str = "chat",
        mode: str = "conversation",
        allowed_capabilities: list[str] | None = None,
        temperature: float = 0.65,
        max_tokens: int = 500,
    ) -> dict[str, Any]:
        return self._post("/v1/intelligence", {
            "shell": shell,
            "tier": tier,
            "messages": messages,
            "context": context or {},
            "surface": surface,
            "mode": mode,
            "allowed_capabilities": allowed_capabilities or [],
            "temperature": temperature,
            "max_tokens": max_tokens,
        })

    def plan(
        self,
        trigger: str,
        *,
        shell: str = "ap",
        tier: str = "lifeos",
        context: dict[str, Any] | None = None,
        available_actions: list[str] | None = None,
        allowed_capabilities: list[str] | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/agent/plan", {
            "shell": shell,
            "tier": tier,
            "trigger": trigger,
            "context": context or {},
            "available_actions": available_actions or [],
            "allowed_capabilities": allowed_capabilities or [],
        })

    def retrieve(self, query: str, context: dict[str, Any], top_k: int = 6) -> dict[str, Any]:
        return self._post("/v1/retrieve", {"query": query, "context": context, "top_k": top_k})

    def memory_candidates(self, text: str) -> dict[str, Any]:
        return self._post("/v1/memory/candidates", {"text": text})

    def get_model_info(self) -> dict[str, Any]:
        return self._get("/model/info")

    def get_capabilities(self) -> dict[str, Any]:
        return self._get("/v1/capabilities")

    def get_talents(self) -> dict[str, Any]:
        return self._get("/v1/talents")


class AscensionAIImage:
    """Reserved interface; image generation is not active in the native core yet."""

    def generate_image(self, *_: Any, **__: Any) -> dict[str, Any]:
        raise NotImplementedError("Native image generation remains a gated Ascension AI roadmap capability.")


class AscensionAIAudio:
    """Reserved interface; native speech generation is not active yet."""

    def text_to_speech(self, *_: Any, **__: Any) -> dict[str, Any]:
        raise NotImplementedError("Native voice remains a shell-required Ascension AI roadmap capability.")
