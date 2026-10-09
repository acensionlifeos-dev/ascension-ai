"""HTTP integration tests for staged signed request enforcement."""
import base64
import hashlib
import hmac
import json
import time

import httpx
import pytest

from src.serving import api
from src.serving.request_integrity import canonical_payload, payload_sha256


class NonceStore:
    def __init__(self):
        self.seen = set()

    def claim(self, key, ttl_seconds):
        if key in self.seen:
            return False
        self.seen.add(key)
        return True


@pytest.fixture
def signing(monkeypatch):
    key = b"s" * 32
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "production")
    monkeypatch.setenv("ASCENSION_AI_REQUIRE_SIGNED_REQUESTS", "true")
    monkeypatch.setenv("ASCENSION_AI_SERVICE_TOKEN", "test-service-token")
    monkeypatch.setenv("ASCENSION_AI_SERVICE_SHELLS", "ap")
    monkeypatch.setenv("ASCENSION_AI_TRUSTED_ISSUER", "aerynza-product")
    monkeypatch.setenv("ASCENSION_AI_SIGNING_KEY_ID", "current")
    monkeypatch.setenv("ASCENSION_AI_SIGNING_KEY_BASE64", base64.b64encode(key).decode())
    monkeypatch.setenv("ASCENSION_AI_REPLAY_REDIS_URL", "redis://localhost:6379/0")
    store = NonceStore()
    monkeypatch.setattr(api, "redis_nonce_store", lambda _url: store)
    return key


def auth_headers(body, key, *, nonce="nonce-1", shell="ap"):
    now = int(time.time())
    envelope = {
        "request_id": nonce, "issuer": "aerynza-product", "subject": "user-123",
        "shell": shell, "key_id": "current", "nonce": nonce,
        "issued_at": now - 1, "expires_at": now + 60,
        "payload_hash": payload_sha256(body),
    }
    signature = hmac.new(key, canonical_payload(envelope), hashlib.sha256).hexdigest()
    return {
        "Authorization": "Bearer test-service-token",
        "X-Aerynza-Envelope": json.dumps(envelope),
        "X-Aerynza-Signature": signature,
    }


@pytest.mark.asyncio
async def test_unsigned_production_post_rejected(signing):
    transport = httpx.ASGITransport(app=api.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/v1/memory/candidates", json={"text": "hello"},
            headers={"Authorization": "Bearer test-service-token"},
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_signed_request_accepted_once_only(signing):
    body = {"text": "Remember my preference"}
    headers = auth_headers(body, signing)
    transport = httpx.ASGITransport(app=api.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        first = await client.post("/v1/memory/candidates", json=body, headers=headers)
        replay = await client.post("/v1/memory/candidates", json=body, headers=headers)
    assert first.status_code == 200, first.text
    assert replay.status_code == 401


@pytest.mark.asyncio
async def test_payload_tampering_rejected(signing):
    headers = auth_headers({"text": "authorized"}, signing)
    transport = httpx.ASGITransport(app=api.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/v1/memory/candidates", json={"text": "altered"}, headers=headers,
        )
    assert response.status_code == 401
