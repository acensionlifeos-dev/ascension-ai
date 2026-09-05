"""Plaid balance client for Aerynza Financial Intelligence."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request


BALANCE_QUERY_RE = re.compile(
    r"\b(?:how\s+much\s+(?:do\s+i\s+have|is\s+in|money|cash|funds)|"
    r"what(?:'s|s| is)\s+(?:my|the)\s+(?:balance|account\s+balance|bank\s+balance|cash\s+balance|funds)|"
    r"account\s+balance|bank\s+balance|cash\s+balance|funds)\b",
    re.I,
)


def _plaid_env_url() -> str:
    env = os.getenv("PLAID_ENV", "production").strip().lower()
    if env in ("sandbox", "development"):
        return f"https://{env}.plaid.com"
    return "https://production.plaid.com"


def _plaid_credentials(context: dict | None = None) -> tuple[str, str, str]:
    """Read Plaid credentials from shell context first, then environment."""
    if context:
        provider_keys = context.get("provider_keys") or {}
        plaid = provider_keys.get("plaid", {})
        client_id = str(plaid.get("client_id", "")).strip() or os.getenv("PLAID_CLIENT_ID", "").strip()
        secret = str(plaid.get("secret", "")).strip() or os.getenv("PLAID_SECRET", "").strip()
        access_token = str(plaid.get("access_token", "")).strip() or os.getenv("PLAID_ACCESS_TOKEN", "").strip()
    else:
        client_id = os.getenv("PLAID_CLIENT_ID", "").strip()
        secret = os.getenv("PLAID_SECRET", "").strip()
        access_token = os.getenv("PLAID_ACCESS_TOKEN", "").strip()
    return client_id, secret, access_token


def parse_balance_query(text: str) -> bool:
    """Detect a request for current cash/account balance."""
    return bool(BALANCE_QUERY_RE.search(str(text or "")))


def format_balances(accounts: list[dict]) -> str:
    lines = []
    total = 0.0
    for account in accounts:
        name = account.get("name", "Account")
        mask = account.get("mask")
        subtype = account.get("subtype", "")
        balances = account.get("balances", {})
        current = balances.get("current")
        available = balances.get("available")
        currency = balances.get("iso_currency_code", "USD")
        if current is None:
            continue
        total += float(current)
        label = name
        if mask:
            label = f"{name} ···{mask}"
        if subtype:
            label = f"{label} ({subtype})"
        if available is not None and available != current:
            lines.append(f"- {label}: ${current:,.2f} current, ${available:,.2f} available ({currency})")
        else:
            lines.append(f"- {label}: ${current:,.2f} ({currency})")
    if lines:
        return (
            f"Current account balances:\n" + "\n".join(lines) + f"\nTotal current: ${total:,.2f}"
        )
    return "No account balances were returned from Plaid."


def get_balances(context: dict | None = None) -> dict:
    """Fetch current balances from Plaid if credentials are configured."""
    client_id, secret, access_token = _plaid_credentials(context)
    if not (client_id and secret and access_token):
        return {
            "status": "no_key",
            "message": (
                "Plaid is not configured. The shell can supply credentials in "
                "context['provider_keys']['plaid'] with 'client_id', 'secret', and 'access_token', "
                "or set PLAID_CLIENT_ID, PLAID_SECRET, and PLAID_ACCESS_TOKEN in the environment."
            ),
        }

    payload = json.dumps({
        "client_id": client_id,
        "secret": secret,
        "access_token": access_token,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{_plaid_env_url()}/accounts/balance/get",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        accounts = data.get("accounts", [])
        return {
            "status": "ok",
            "accounts": accounts,
            "message": format_balances(accounts),
        }
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        return {"status": "error", "message": f"Plaid API error ({error.code}): {body}"}
    except Exception as error:
        return {"status": "error", "message": f"Could not reach Plaid: {error}"}
