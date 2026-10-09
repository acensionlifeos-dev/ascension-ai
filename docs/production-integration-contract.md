# Aerynza native AI production integration contract (draft)

This document describes requirements for the **main Aerynza backend**, not a completed integration. Do not deploy the native service until the corresponding backend signer and resource authorization have been implemented and tested.

## Service admission

Production requires `ASCENSION_AI_AUTH_MODE=production`, `ASCENSION_AI_REQUIRE_SIGNED_REQUESTS=true`, a strong service Bearer token, an explicit `ASCENSION_AI_SERVICE_SHELLS` allowlist, trusted issuer/key ID, a base64 HMAC key of at least 32 bytes, and a reachable shared Redis replay store. Never expose these secrets in a browser, mobile client, or log.

The trusted backend sends `Authorization: Bearer <service token>`, `X-Aerynza-Envelope: <JSON>`, and `X-Aerynza-Signature: <hex HMAC SHA-256>`. Compute the signature over the canonical JSON envelope using `src.serving.request_integrity.canonical_payload`. Set `payload_hash` to `payload_sha256` of the JSON object body (for signed GET without a body, use `{}`). Include `request_id`, `issuer`, `subject`, `shell`, `key_id`, `nonce`, `issued_at`, `expires_at`, `http_method`, and `http_path`. Sign the exact method and path; do not include query parameters in the path. Use a unique cryptographically random nonce for every attempt; do not replay after an ambiguous timeout. Use a short validity period (at most 120 seconds). Ensure service clocks are synchronized.

**Critical limitation:** The HMAC proves a trusted service produced the envelope. It does **not** establish that `subject` owns a session, household, family, child, or other resource. The native service currently has no authoritative resource-ownership resolver. The product backend must authenticate the user, check entitlements and current membership/consent for each resource, and produce permission-scoped context. Native production session storage and sensitive family/home/child thesis and contribution routes remain denied until an independently verifiable ownership/consent mechanism is implemented.

## Deployment gates

1. Backend-to-native signer compatibility tests: valid POST and GET; body tamper; wrong method/path; shell mismatch; expired envelope; nonce replay; Redis outage; key rotation.
2. Authorization tests: two distinct users with identical session IDs; revoked household membership; child guardian consent; family sharing scope; tenant isolation; role changes.
3. Reliability tests: model not ready, timeouts, retries with fresh nonces, backpressure, failed Redis, observability with redacted request content.
4. Operational controls: secrets rotation, TLS between services, service isolation, rollback, and on-call alerts.
5. CI must run and pass before review/merge; draft PR commits are not proof of passing tests.

Do not send raw private records or action authority solely because an envelope is signed. An AI-generated permission statement is not an authorization grant.
