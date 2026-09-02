"""Android phone bridge using a local adb binary.

Expects Android Platform Tools to be unpacked at:
    <repo root>/tools/adb/platform-tools/

The phone must have USB debugging enabled and be authorized on this PC.
"""

from __future__ import annotations

import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
SCREENSHOTS = PUBLIC / "screenshots"
ADB_DIR = ROOT / "tools" / "adb" / "platform-tools"
ADB_EXE = ADB_DIR / "adb.exe"


ADB = shutil.which("adb") or (str(ADB_EXE) if ADB_EXE.is_file() else "adb")

ALLOWED_ACTIONS = {
    "list_devices",
    "list_apps",
    "screenshot",
    "tap",
    "swipe",
    "type_text",
    "press_key",
    "home",
    "back",
    "recent",
    "launch_app",
}

KEY_MAP = {
    "home": "3",
    "back": "4",
    "enter": "66",
    "space": "62",
    "menu": "82",
    "power": "26",
    "recent": "187",
    "volume_up": "24",
    "volume_down": "25",
}


def _ensure_public_dirs() -> None:
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)


def _call(args: list, binary: bool = False, timeout: int = 30) -> tuple:
    command = [ADB, *args]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            timeout=timeout,
            text=not binary,
        )
        return (result.returncode, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return (1, "", "adb command timed out")
    except FileNotFoundError:
        return (1, "", f"adb not found at {ADB}. Run setup.ps1 or install Android Platform Tools.")


def _device(serial: str | None = None) -> list:
    return ["-s", serial] if serial else []


def list_devices() -> dict:
    rc, out, err = _call(["devices", "-l"], timeout=15)
    if rc != 0:
        return {"status": "error", "message": err or "adb failed"}
    devices = [line for line in out.strip().splitlines() if line and not line.startswith("List")]
    parsed = []
    for line in devices:
        parts = line.split()
        if len(parts) >= 2:
            parsed.append({"serial": parts[0], "state": parts[1], "info": " ".join(parts[2:])})
    return {"status": "listed", "count": len(parsed), "devices": parsed}


def list_apps() -> dict:
    rc, out, err = _call(["shell", "pm", "list", "packages", "-3"], timeout=30)
    if rc != 0:
        return {"status": "error", "message": err or "adb failed"}
    packages = [line.replace("package:", "").strip() for line in out.splitlines() if line.startswith("package:")]
    return {"status": "listed", "count": len(packages), "apps": packages[:200]}


def screenshot(serial: str | None = None) -> dict:
    _ensure_public_dirs()
    filename = f"android_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
    local_path = SCREENSHOTS / filename
    remote = "/sdcard/ascension_screenshot.png"
    rc, _, err = _call(_device(serial) + ["shell", "screencap", "-p", remote], timeout=30)
    if rc != 0:
        return {"status": "error", "message": err or "screencap failed"}
    rc, _, err = _call(_device(serial) + ["pull", remote, str(local_path)], timeout=30)
    if rc != 0:
        return {"status": "error", "message": err or "pull failed"}
    _call(_device(serial) + ["shell", "rm", remote], timeout=15)
    return {"status": "screenshot", "url": f"/static/screenshots/{filename}", "path": str(local_path)}


def tap(x: int, y: int, serial: str | None = None) -> dict:
    rc, _, err = _call(_device(serial) + ["shell", "input", "tap", str(int(x)), str(int(y))], timeout=15)
    return {"status": "tapped" if rc == 0 else "error", "x": int(x), "y": int(y), "message": err if rc != 0 else ""}


def swipe(x1: int, y1: int, x2: int, y2: int, ms: int = 300, serial: str | None = None) -> dict:
    rc, _, err = _call(_device(serial) + ["shell", "input", "swipe", str(int(x1)), str(int(y1)), str(int(x2)), str(int(y2)), str(int(ms))], timeout=15)
    return {"status": "swiped" if rc == 0 else "error", "message": err if rc != 0 else ""}


def type_text(text: str, serial: str | None = None) -> dict:
    escaped = text.replace("'", "'\\''")
    rc, _, err = _call(_device(serial) + ["shell", "input", "text", f"'{escaped}'"], timeout=15)
    return {"status": "typed" if rc == 0 else "error", "length": len(text), "message": err if rc != 0 else ""}


def press_key(key: str, serial: str | None = None) -> dict:
    code = KEY_MAP.get(key.lower(), key)
    rc, _, err = _call(_device(serial) + ["shell", "input", "keyevent", str(code)], timeout=15)
    return {"status": "pressed" if rc == 0 else "error", "key": key, "message": err if rc != 0 else ""}


def home(serial: str | None = None) -> dict:
    return press_key("home", serial)


def back(serial: str | None = None) -> dict:
    return press_key("back", serial)


def recent(serial: str | None = None) -> dict:
    return press_key("recent", serial)


def launch_app(package: str, serial: str | None = None) -> dict:
    rc, _, err = _call(_device(serial) + ["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"], timeout=15)
    return {"status": "launched" if rc == 0 else "error", "package": package, "message": err if rc != 0 else ""}


def run(action: str, **params: Any) -> dict:
    if action not in ALLOWED_ACTIONS:
        return {"status": "forbidden", "message": f"Action '{action}' is not in the allowed list."}
    try:
        handler = globals()[action]
        return handler(**params)
    except TypeError as error:
        return {"status": "error", "message": f"Invalid parameters for {action}: {error}"}
    except Exception as error:
        return {"status": "error", "message": f"Android bridge failed: {error}"}
