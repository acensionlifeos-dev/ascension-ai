"""Targeted test for the native inference queue timeout."""

from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.model_runtime import NativeInferenceQueueTimeout, NativeModelRuntime


def test_chat_queue_timeout():
    runtime = NativeModelRuntime()
    runtime.queue_timeout_seconds = 0.1
    runtime.model = object()  # dummy; should never be reached
    runtime.lock.acquire()

    def release_later():
        time.sleep(0.5)
        runtime.lock.release()

    threading.Thread(target=release_later, daemon=True).start()
    try:
        runtime.chat([{"role": "user", "content": "hello"}], 0.7, 32)
        raise AssertionError("expected RuntimeError for queue timeout")
    except NativeInferenceQueueTimeout as exc:
        assert "Native inference queue timeout" in str(exc), str(exc)
    assert runtime.queue_depth == 0, "timed-out chat requests must leave the queue"
    assert runtime.timeout_requests == 1, "chat timeout must be counted once"
    assert runtime.failed_requests == 1, "chat timeout must be counted as a failed request"
    time.sleep(0.6)


def test_stream_chat_queue_timeout():
    runtime = NativeModelRuntime()
    runtime.queue_timeout_seconds = 0.1
    runtime.model = object()
    runtime.lock.acquire()

    def release_later():
        time.sleep(0.5)
        runtime.lock.release()

    threading.Thread(target=release_later, daemon=True).start()
    try:
        list(runtime.stream_chat([{"role": "user", "content": "hello"}], 0.7, 32))
        raise AssertionError("expected RuntimeError for queue timeout")
    except NativeInferenceQueueTimeout as exc:
        assert "Native inference queue timeout" in str(exc), str(exc)
    assert runtime.timeout_requests == 1, "stream timeout must be counted once"
    assert runtime.failed_requests == 1, "stream timeout must be counted as a failed request"
    time.sleep(0.6)


def test_status_includes_timeout_metrics():
    runtime = NativeModelRuntime()
    status = runtime.status()
    assert "queue" in status
    assert "timeout_requests" in status["queue"]
    assert "queue_timeout_seconds" in status["queue"]
    assert status["queue"]["queue_timeout_seconds"] == runtime.queue_timeout_seconds


if __name__ == "__main__":
    test_chat_queue_timeout()
    test_stream_chat_queue_timeout()
    test_status_includes_timeout_metrics()
    print("PASS queue timeout wiring")
