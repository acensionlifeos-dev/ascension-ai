"""Thread-safe local GGUF inference runtime for Ascension AI."""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROFILES_PATH = ROOT / "config" / "model_profiles.json"


class NativeModelRuntime:
    def __init__(self) -> None:
        self.model = None
        self.profile_name = os.getenv("ASCENSION_MODEL_PROFILE", "starter").strip().lower()
        self.profile: dict = {}
        self.loaded_at: float | None = None
        self.load_error: str | None = None
        self.lock = threading.Lock()

    def _read_profile(self) -> dict:
        profiles = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
        if self.profile_name not in profiles:
            raise RuntimeError(f"Unknown model profile: {self.profile_name}")
        return profiles[self.profile_name]

    def _model_path(self) -> Path:
        override = os.getenv("ASCENSION_MODEL_PATH", "").strip()
        return Path(override) if override else ROOT / "models" / self.profile["filename"]

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def load(self) -> None:
        try:
            from llama_cpp import Llama
            self.profile = self._read_profile()
            path = self._model_path()
            if not path.is_file():
                raise RuntimeError("Pinned model file is missing. Run scripts/download_model.py during the build.")
            if os.getenv("ASCENSION_VERIFY_MODEL_ON_BOOT", "1") != "0" and self._sha256(path) != self.profile["sha256"]:
                raise RuntimeError("Pinned model checksum verification failed.")
            self.model = Llama(
                model_path=str(path),
                n_ctx=int(os.getenv("ASCENSION_MODEL_CONTEXT", self.profile["context_tokens"])),
                n_threads=int(os.getenv("ASCENSION_MODEL_THREADS", self.profile["threads"])),
                n_batch=int(os.getenv("ASCENSION_MODEL_BATCH", "16")),
                use_mmap=True,
                use_mlock=False,
                verbose=False,
            )
            self.loaded_at = time.time()
            self.load_error = None
        except Exception as error:
            self.model = None
            self.load_error = str(error)
            raise

    def status(self) -> dict:
        return {
            "ready": self.model is not None,
            "profile": self.profile_name,
            "model": self.profile.get("label"),
            "repo_id": self.profile.get("repo_id"),
            "filename": self.profile.get("filename"),
            "context_tokens": self.profile.get("context_tokens"),
            "loaded_at": self.loaded_at,
            "error": self.load_error,
            "inference": "local_gguf_llama_cpp",
            "outside_provider": False,
        }

    def chat(self, messages: list[dict], temperature: float, max_tokens: int) -> dict:
        if self.model is None:
            raise RuntimeError(self.load_error or "Native model is not loaded.")
        started = time.perf_counter()
        with self.lock:
            result = self.model.create_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,
                repeat_penalty=1.08,
            )
        content = str(result.get("choices", [{}])[0].get("message", {}).get("content", "")).strip()
        if not content:
            raise RuntimeError("Native model returned an empty response.")
        return {
            "content": content,
            "model": self.profile.get("label") or self.profile_name,
            "provider": "ascension-native",
            "usage": result.get("usage") or {},
            "latency_ms": round((time.perf_counter() - started) * 1000),
        }

    def stream_chat(self, messages: list[dict], temperature: float, max_tokens: int):
        if self.model is None:
            raise RuntimeError(self.load_error or "Native model is not loaded.")
        with self.lock:
            chunks = self.model.create_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,
                repeat_penalty=1.08,
                stream=True,
            )
            for chunk in chunks:
                token = str(chunk.get("choices", [{}])[0].get("delta", {}).get("content", ""))
                if token:
                    yield token


runtime = NativeModelRuntime()
