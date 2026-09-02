"""iPhone bridge using iOS Shortcuts webhooks.

The Windows side hosts a FastAPI endpoint. The iPhone reaches the PC over the
local network and/or a user-configured webhook URL.

Required environment:
    IPHONE_WEBHOOK_URL  - the URL of an iOS Shortcut that can receive POST JSON.

The iPhone can also POST to /v1/iphone/inbox to send data to Ascension.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
INBOX_FILE = DATA / "iphone_inbox.json"
IPHONE_WEBHOOK_URL = os.environ.get("IPHONE_WEBHOOK_URL", "").strip()


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


def send(message: str) -> dict:
    """Send a message to the configured iOS Shortcut webhook."""
    if not IPHONE_WEBHOOK_URL:
        return {
            "status": "error",
            "message": "IPHONE_WEBHOOK_URL is not set. Add it to ascension.env and restart.",
        }
    try:
        payload = {
            "message": message,
            "from": "Ascension AI",
            "sent_at": datetime.now(timezone.utc).isoformat(),
        }
        response = requests.post(IPHONE_WEBHOOK_URL, json=payload, timeout=30)
        return {
            "status": "sent",
            "url": IPHONE_WEBHOOK_URL,
            "response_status": response.status_code,
            "body": response.text[:500],
        }
    except Exception as error:
        return {"status": "error", "message": str(error)}


def list_messages() -> dict:
    """Return messages received from the iPhone inbox."""
    inbox = _load_inbox()
    return {"status": "listed", "count": len(inbox), "messages": inbox[-50:]}


def receive(payload: dict) -> dict:
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
