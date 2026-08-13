"""Targeted tests for native inference hang detection and watchdog.

The watchdog is the process-level backstop: if an active llama.cpp call
exceeds ASCENSION_INFERENCE_TIMEOUT_SECONDS, the configured exit callback is
called and the container runtime (Render) restarts the service. Tests mock
that callback and never kill the test process.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.model_runtime import NativeModelRuntime


def test_hung_flag_when_inference_exceeds_timeout():
    runtime = NativeModelRuntime(exit_callback=lambda: None)
    runtime.inference_timeout_seconds = 0.05
    runtime.active_requests = 1
    runtime.inference_started_at = time.perf_counter() - 0.1
    status = runtime.status()
    assert status["queue"]["inference_hung"] is True, "inference should be marked hung after timeout"
    assert status["queue"]["inference_timeout_seconds"] == 0.05
    assert status["queue"]["watchdog_enabled"] is False


def test_not_hung_when_inference_active_within_timeout():
    runtime = NativeModelRuntime(exit_callback=lambda: None)
    runtime.inference_timeout_seconds = 10.0
    runtime.active_requests = 1
    runtime.inference_started_at = time.perf_counter() - 1.0
    status = runtime.status()
    assert status["queue"]["inference_hung"] is False, "inference should not be marked hung within budget"


def test_not_hung_when_no_active_inference():
    runtime = NativeModelRuntime(exit_callback=lambda: None)
    runtime.inference_timeout_seconds = 0.05
    runtime.active_requests = 0
    runtime.inference_started_at = None
    status = runtime.status()
    assert status["queue"]["inference_hung"] is False, "no active inference means not hung"


def test_watchdog_fires_with_hung_inference():
    mock_exit = MagicMock()
    runtime = NativeModelRuntime(exit_callback=mock_exit)
    runtime.watchdog_enabled = True
    runtime.inference_timeout_seconds = 0.05
    runtime.inference_started_at = time.perf_counter() - 0.1
    runtime.active_requests = 1
    runtime._watchdog_tick()
    mock_exit.assert_called_once()


def test_watchdog_does_not_fire_when_not_hung():
    mock_exit = MagicMock()
    runtime = NativeModelRuntime(exit_callback=mock_exit)
    runtime.inference_timeout_seconds = 10.0
    runtime.inference_started_at = time.perf_counter()
    runtime.active_requests = 1
    runtime._watchdog_tick()
    mock_exit.assert_not_called()


def test_watchdog_disabled_by_default():
    mock_exit = MagicMock()
    runtime = NativeModelRuntime(exit_callback=mock_exit)
    runtime.inference_timeout_seconds = 0.05
    runtime.inference_started_at = time.perf_counter() - 0.1
    runtime.active_requests = 1
    assert runtime.watchdog_enabled is False
    runtime._watchdog_tick()
    mock_exit.assert_not_called()


def test_chat_clears_inference_started_at_on_completion():
    runtime = NativeModelRuntime(exit_callback=lambda: None)
    runtime.inference_timeout_seconds = 1.0
    runtime.model = MagicMock()
    runtime.model.create_chat_completion.return_value = {
        "choices": [{"message": {"content": "Hello"}}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
    }
    result = runtime.chat([{"role": "user", "content": "hello"}], 0.7, 32)
    assert result["content"] == "Hello"
    assert runtime.inference_started_at is None, "inference_started_at must be cleared after chat"
    assert runtime.active_requests == 0
    assert runtime.queue_depth == 0


def test_stream_chat_clears_inference_started_at_on_completion():
    runtime = NativeModelRuntime(exit_callback=lambda: None)
    runtime.inference_timeout_seconds = 1.0
    runtime.model = MagicMock()
    runtime.model.create_chat_completion.return_value = [
        {"choices": [{"delta": {"content": "Hello"}}]},
        {"choices": [{"delta": {"content": " world"}}]},
    ]
    tokens = list(runtime.stream_chat([{"role": "user", "content": "hello"}], 0.7, 32))
    assert "Hello" in "".join(tokens)
    assert runtime.inference_started_at is None, "inference_started_at must be cleared after stream"
    assert runtime.active_requests == 0


if __name__ == "__main__":
    test_hung_flag_when_inference_exceeds_timeout()
    test_not_hung_when_inference_active_within_timeout()
    test_not_hung_when_no_active_inference()
    test_watchdog_fires_with_hung_inference()
    test_watchdog_does_not_fire_when_not_hung()
    test_watchdog_disabled_by_default()
    test_chat_clears_inference_started_at_on_completion()
    test_stream_chat_clears_inference_started_at_on_completion()
    print("PASS inference hang detection and watchdog")
