"""iPhone bridge using iOS Shortcuts webhooks.

The Windows side hosts a FastAPI endpoint. The iPhone reaches the PC over the
local network and/or a user-configured webhook URL.

The webhook URL can be supplied by the shell in::

    context["provider_keys"]["iphone"]["webhook_url"]

or by the environment variable IPHONE_WEBHOOK_URL.

The iPhone can also POST to /v1/iphone/inbox to send data to Ascension.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.core.provider_keys import provider_key


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
INBOX_FILE = DATA / "iphone_inbox.json"


def _webhook_url(context: dict | None = None) -> str:
    return provider_key(context, "iphone", "webhook_url", "IPHONE_WEBHOOK_URL")


def _ensure_data() -> None:
    DATA.mkdir(parents=True, exist_ok=True)


def _load_inbox() -> list:
    _ensure_data()
    if not INBOX_FILE.is_file():
        return []
    try:
        with open(INBOX_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def _save_inbox(inbox: list) -> None:
    _ensure_data()
    with open(INBOX_FILE, "w", encoding="utf-8") as file:
        json.dump(inbox, file, indent=2)


def send(message: str, context: dict | None = None) -> dict:
    """Send a message to the configured iOS Shortcut webhook."""
    url = _webhook_url(context)
    if not url:
        return {
            "status": "error",
            "message": "iPhone webhook URL is not set. Supply it in context['provider_keys']['iphone']['webhook_url'] or set IPHONE_WEBHOOK_URL.",
        }
    try:
        payload = {
            "message": message,
            "from": "Ascension AI",
            "sent_at": datetime.now(timezone.utc).isoformat(),
        }
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", errors="replace")[:500]
        return {
            "status": "sent",
            "url": url,
            "response_status": response.status,
            "body": body,
        }
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")[:500]
        return {"status": "error", "message": f"iPhone webhook returned {error.code}: {body}"}
    except Exception as error:
        return {"status": "error", "message": str(error)}


def list_messages(context: dict | None = None) -> dict:
    """Return messages received from the iPhone inbox."""
    inbox = _load_inbox()
    return {"status": "listed", "count": len(inbox), "messages": inbox[-50:]}


def receive(payload: dict, context: dict | None = None) -> dict:
    """Store a payload received from the iPhone."""
    inbox = _load_inbox()
    item = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    inbox.append(item)
    _save_inbox(inbox)
    return {"status": "received", "inbox_count": len(inbox)}


IPHONE_HANDLERS = {
    "send": send,
    "list": list_messages,
    "receive": receive,
}


def run(action: str, **params: Any) -> dict:
    if action not in IPHONE_HANDLERS:
        return {"status": "forbidden", "message": f"iPhone action '{action}' is not allowed."}
    try:
        handler = IPHONE_HANDLERS[action]
        return handler(**params)
    except TypeError as error:
        return {"status": "error", "message": f"Invalid parameters for {action}: {error}"}
    except Exception as error:
        return {"status": "error", "message": f"iPhone bridge failed: {error}"}
