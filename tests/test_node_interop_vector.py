"""Node-to-Python canonical JSON and HMAC interoperability regression."""
import base64
import hashlib
import hmac
import json

from src.serving.request_integrity import canonical_payload, payload_sha256
from src.serving.envelope_signature import verify_signed_envelope

PAYLOAD = {"shell": "ap", "text": "Hello Aerynza"}
ENVELOPE = {
    "request_id": "request-123",
    "issuer": "aerynza-product",
    "subject": "user-123",
    "shell": "ap",
    "key_id": "current",
    "nonce": "nonce-123",
    "issued_at": 1760000000,
    "expires_at": 1760000060,
    "http_method": "POST",
    "http_path": "/v1/retrieve",
    "payload_hash": "88c6b84eba9e19eb15156f1592a49ba7db70f30c45d7ab8bf1eda73f2c0df513",
}
SIGNATURE = "c53c0ce2cb60b51bd50d3740acecaf9437cb0a00461da2380cb4d2cac0ed87f4"
KEY = base64.b64decode("c3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3M=")


def test_node_hmac_vector_is_accepted_by_python():
    assert payload_sha256(PAYLOAD) == ENVELOPE["payload_hash"]
    assert hmac.new(KEY, canonical_payload(ENVELOPE), hashlib.sha256).hexdigest() == SIGNATURE
    assert verify_signed_envelope(
        ENVELOPE, PAYLOAD, SIGNATURE,
        keys={"current": KEY}, trusted_issuer="aerynza-product", now=1760000030
    )


def test_tampered_node_vector_is_rejected():
    import pytest
    from src.serving.envelope_validation import InvalidEnvelope
    with pytest.raises(InvalidEnvelope):
        verify_signed_envelope(
            ENVELOPE, {"shell": "ap", "text": "changed"}, SIGNATURE,
            keys={"current": KEY}, trusted_issuer="aerynza-product", now=1760000030
        )
