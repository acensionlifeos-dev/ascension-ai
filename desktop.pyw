"""Ascension AI — native desktop wrapper.

Starts the local server if it isn't already running, then opens the chat
in a dedicated pywebview window so it feels like a desktop app.
"""

import subprocess
import sys
import time
from pathlib import Path

import requests
import shutil
import webview


REPO = Path(__file__).resolve().parent
SERVER_URL = "http://127.0.0.1:8000/health"
WEBVIEW_STORAGE = REPO / ".webview"


def server_running() -> bool:
    try:
        response = requests.get(SERVER_URL, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def main():
    server = None
    if not server_running():
        start_script = REPO / "start.ps1"
        server = subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(start_script)],
            cwd=str(REPO),
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        for _ in range(60):
            if server_running():
                break
            time.sleep(1)
        else:
            webview.create_window(
                "Ascension AI — Error",
                "data:text/html,<h1 style='font-family:sans-serif;padding:40px'>The Ascension server did not start. Please check the logs.</h1>",
                width=500,
                height=300,
            )
            webview.start()
            return

    cache_buster = str(int(time.time()))
    if WEBVIEW_STORAGE.exists():
        shutil.rmtree(str(WEBVIEW_STORAGE), ignore_errors=True)
    webview.create_window(
        "Ascension AI",
        f"http://127.0.0.1:8000?v={cache_buster}",
        width=1280,
        height=860,
        resizable=True,
        text_select=True,
    )
    webview.start(debug=True, storage_path=str(WEBVIEW_STORAGE))

    if server:
        try:
            server.terminate()
        except Exception:
            pass


if __name__ == "__main__":
    main()
