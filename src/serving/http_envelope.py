"""HTTP admission for opt-in Aerynza service-to-service signed requests."""
import base64
import json
import os

from src.serving.envelope_gateway import admit_request
from src.serving.envelope_validation import InvalidEnvelope
from src.serving.replay_guard import RedisNonceStore


def signing_enabled() -> bool:
    return os.getenv("ASCENSION_AI_REQUIRE_SIGNED_REQUESTS", "").lower() == "true"


def load_signing_configuration():
    """Read key material only from the server environment, never request data."""
    issuer = os.getenv("ASCENSION_AI_TRUSTED_ISSUER", "").strip()
    key_id = os.getenv("ASCENSION_AI_SIGNING_KEY_ID", "").strip()
    encoded = os.getenv("ASCENSION_AI_SIGNING_KEY_BASE64", "").strip()
    redis_url = os.getenv("ASCENSION_AI_REPLAY_REDIS_URL", "").strip()
    if not (issuer and key_id and encoded and redis_url):
        raise RuntimeError("Signed requests require issuer, key ID, key, and shared Redis")
    try:
        key = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise RuntimeError("Invalid signed-request key encoding") from exc
    if len(key) < 32:
        raise RuntimeError("Signed-request key must contain at least 32 bytes")
    if not redis_url.startswith(("redis://", "rediss://")):
        raise RuntimeError("Replay store must use a Redis URL")
    return issuer, {key_id: key}, redis_url


def check_http_envelope(headers, payload, *, config, nonce_store, method, path):
    """Verify cryptography and consume single-use nonce; errors reject request."""
    raw = headers.get("x-aerynza-envelope", "")
    signature = headers.get("x-aerynza-signature", "")
    if not raw or len(raw) > 4096:
        raise InvalidEnvelope("Missing or oversized envelope")
    try:
        envelope = json.loads(raw)
    except (TypeError, ValueError) as exc:
        raise InvalidEnvelope("Malformed envelope JSON") from exc
    if envelope.get("http_method") != method or envelope.get("http_path") != path:
        raise InvalidEnvelope("Signed HTTP target mismatch")
    issuer, keys, _ = config
    return admit_request(
        envelope, payload, signature, keys=keys,
        trusted_issuer=issuer, nonce_store=nonce_store,
    )


def redis_nonce_store(redis_url):
    import redis
    client = redis.Redis.from_url(redis_url, socket_connect_timeout=2, socket_timeout=2)
    return RedisNonceStore(client)
