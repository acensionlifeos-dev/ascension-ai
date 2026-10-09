"""Canonical request payload integrity helpers for the planned service envelope."""
import hashlib
import json


def canonical_payload(payload: dict) -> bytes:
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def payload_sha256(payload: dict) -> str:
    return hashlib.sha256(canonical_payload(payload)).hexdigest()
