"""Provider-key resolution: shell context first, environment fallback."""

from __future__ import annotations

import os


def provider_key(
    context: dict | None,
    provider: str,
    key: str,
    env_names: str | list[str] | tuple[str, ...] | None = None,
    default: str = "",
) -> str:
    """Resolve a provider credential from the shell context, then the environment.

    The shell should pass provider keys under::

        context["provider_keys"][<provider>][<key>]

    If the shell did not supply the key, fall back to the configured environment
    variable name(s). This keeps secrets out of the AI service by default while
    still allowing standalone operation when keys are exported locally.
    """
    if context:
        provider_keys = context.get("provider_keys") or {}
        value = str(provider_keys.get(provider, {}).get(key, "")).strip()
        if value:
            return value
    if env_names:
        names = env_names if isinstance(env_names, (list, tuple)) else (env_names,)
        for name in names:
            value = os.getenv(name, "").strip()
            if value:
                return value
    return default
