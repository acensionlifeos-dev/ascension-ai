"""Regression tests for the native API production authentication boundary."""
import pytest
from fastapi import HTTPException

from src.serving import api


def test_production_requires_service_secret(monkeypatch):
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "production")
    monkeypatch.delenv("ASCENSION_AI_SERVICE_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="ASCENSION_AI_SERVICE_TOKEN"):
        api.validate_auth_configuration()


def test_production_rejects_email_test_and_session_tokens(monkeypatch):
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "production")
    monkeypatch.setenv("ASCENSION_AI_SERVICE_TOKEN", "real-service-secret")
    monkeypatch.setenv("ASCENSION_AI_ALLOWED_EMAIL", "owner@example.test")
    monkeypatch.setenv("ASCENSION_AI_TEST_TOKEN", "test-secret")
    monkeypatch.setenv("ASCENSION_AI_LOCAL_DEV_BYPASS", "true")
    api.SESSIONS.add("desktop-session-secret")
    try:
        for token in ("owner@example.test", "test-secret", "desktop-session-secret"):
            with pytest.raises(HTTPException) as error:
                api.require_access("Bearer " + token)
            assert error.value.status_code == 401
        api.require_access("Bearer real-service-secret")
    finally:
        api.SESSIONS.discard("desktop-session-secret")


def test_development_bypass_requires_explicit_mode(monkeypatch):
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "development")
    monkeypatch.setenv("ASCENSION_AI_LOCAL_DEV_BYPASS", "true")
    api.require_access(None)
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "production")
    with pytest.raises(HTTPException) as error:
        api.require_access(None)
    assert error.value.status_code == 401


def test_malformed_auth_and_unknown_mode_fail_closed(monkeypatch):
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "production")
    monkeypatch.setenv("ASCENSION_AI_SERVICE_TOKEN", "real-service-secret")
    for value in (None, "", "Basic real-service-secret", "Bearer wrong"):
        with pytest.raises(HTTPException):
            api.require_access(value)
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "invalid")
    with pytest.raises(RuntimeError):
        api.validate_auth_configuration()


@pytest.mark.asyncio
async def test_production_disables_desktop_login(monkeypatch):
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "production")
    with pytest.raises(HTTPException) as error:
        await api.login(api.LoginRequest(email="owner@example.test", password="not-a-secret"))
    assert error.value.status_code == 404


def test_production_shell_allowlist_denies_unlisted_shell(monkeypatch):
    from src.core.contracts import Shell
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "production")
    monkeypatch.setenv("ASCENSION_AI_SERVICE_TOKEN", "service-secret")
    monkeypatch.setenv("ASCENSION_AI_SERVICE_SHELLS", Shell.AP.value)
    api.validate_auth_configuration()
    api.enforce_shell_access(Shell.AP)
    with pytest.raises(HTTPException) as error:
        api.enforce_shell_access(Shell.NEXUS_FAMILY)
    assert error.value.status_code == 403


def test_production_requires_explicit_shell_allowlist(monkeypatch):
    monkeypatch.setenv("ASCENSION_AI_AUTH_MODE", "production")
    monkeypatch.setenv("ASCENSION_AI_SERVICE_TOKEN", "service-secret")
    monkeypatch.delenv("ASCENSION_AI_SERVICE_SHELLS", raising=False)
    with pytest.raises(RuntimeError, match="ASCENSION_AI_SERVICE_SHELLS"):
        api.validate_auth_configuration()
