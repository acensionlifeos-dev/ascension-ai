"""Windows desktop action executor for the local Ascension shell.

Only allowed actions may be invoked, and each call is tied to the authenticated
shell token. The executor never runs arbitrary shell commands or reads files
outside the public chat surface.
"""

from __future__ import annotations

import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import pyautogui
    pyautogui.PAUSE = 0.05
except Exception:
    pyautogui = None


ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SCREENSHOTS = PUBLIC / "screenshots"

# These are the only actions a local chat may trigger. New capabilities require
# a code change and a restart so the user stays in control of what can run.
ALLOWED_ACTIONS = {
    "open_app",
    "type_text",
    "press_key",
    "click",
    "screenshot",
    "list_windows",
    "search",
    "wait",
    "chain",
}


def _ensure_public_dirs() -> None:
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)


def open_app(app: str) -> dict:
    """Open an installed program by name, path, or protocol."""
    try:
        os.startfile(app)
        return {"status": "opened", "app": app}
    except Exception as error:
        return {"status": "error", "message": str(error)}


def type_text(text: str, interval: float = 0.01) -> dict:
    """Type the supplied text into the currently focused window."""
    try:
        pyautogui.typewrite(text, interval=interval)
        return {"status": "typed", "length": len(text)}
    except Exception as error:
        return {"status": "error", "message": str(error)}


def press_key(key: str) -> dict:
    """Press a single key (e.g. enter, tab, space, ctrl)."""
    try:
        pyautogui.press(key)
        return {"status": "pressed", "key": key}
    except Exception as error:
        return {"status": "error", "message": str(error)}


def click(x: int, y: int, clicks: int = 1) -> dict:
    """Click at screen coordinates."""
    try:
        pyautogui.click(int(x), int(y), clicks=int(clicks))
        return {"status": "clicked", "x": int(x), "y": int(y)}
    except Exception as error:
        return {"status": "error", "message": str(error)}


def screenshot() -> dict:
    """Capture the primary screen and return a /static/ URL for the chat."""
    _ensure_public_dirs()
    filename = f"ascension_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
    path = SCREENSHOTS / filename
    try:
        image = pyautogui.screenshot()
        image.save(str(path))
        return {"status": "screenshot", "url": f"/static/screenshots/{filename}", "path": str(path)}
    except Exception as error:
        return {"status": "error", "message": str(error)}


def list_windows() -> dict:
    """Return the titles of visible windows."""
    try:
        import pygetwindow as gw
        titles = [w.title for w in gw.getAllWindows() if w.title]
        return {"status": "listed", "count": len(titles), "windows": titles[:200]}
    except Exception as error:
        return {"status": "error", "message": str(error)}


def wait(ms: int) -> dict:
    """Pause for the requested number of milliseconds."""
    try:
        time.sleep(max(0, int(ms)) / 1000.0)
        return {"status": "waited", "ms": int(ms)}
    except Exception as error:
        return {"status": "error", "message": str(error)}


def search(query: str) -> dict:
    """Open the default browser on a Google search for the query."""
    try:
        from urllib.parse import quote
        url = f"https://www.google.com/search?q={quote(query)}"
        os.startfile(url)
        return {"status": "searched", "query": query, "url": url}
    except Exception as error:
        return {"status": "error", "message": str(error)}


def chain(commands: list) -> dict:
    """Run a sequence of allowed actions."""
    results = []
    for item in commands:
        action = item.get("action", "")
        params = item.get("params", {}) or {}
        if action not in ALLOWED_ACTIONS:
            results.append({"status": "forbidden", "message": f"Action '{action}' is not allowed in chains."})
            break
        result = run(action, **params)
        results.append(result)
        if result.get("status") in ("error", "forbidden"):
            break
    return {"status": "chained", "count": len(results), "results": results}


def run(action: str, **params: Any) -> dict:
    """Run one allowed Windows action with the supplied parameters."""
    if action not in ALLOWED_ACTIONS:
        return {"status": "forbidden", "message": f"Action '{action}' is not in the allowed list."}
    try:
        handler = globals()[action]
        return handler(**params)
    except TypeError as error:
        return {"status": "error", "message": f"Invalid parameters for {action}: {error}"}
    except Exception as error:
        return {"status": "error", "message": f"Executor failed: {error}"}
