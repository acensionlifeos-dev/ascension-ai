"""Targeted contract checks for streaming inference failures."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.model_runtime import NativeInferenceQueueTimeout
from src.serving.api import stream_error_payload


def main() -> None:
    timeout = stream_error_payload(NativeInferenceQueueTimeout("private runtime detail"))
    assert timeout == {
        "code": "native_inference_queue_timeout",
        "message": "Aerynza AI is busy. Retry this request shortly.",
        "retryable": True,
        "http_equivalent": 504,
    }

    failure = stream_error_payload(RuntimeError("sensitive internal path"))
    assert failure["code"] == "native_inference_failed"
    assert failure["http_equivalent"] == 502
    assert failure["retryable"] is True
    assert "sensitive" not in failure["message"]

    print("PASS streaming error contract")


if __name__ == "__main__":
    main()
