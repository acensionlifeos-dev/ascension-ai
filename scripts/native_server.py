"""Native Ascension AI HTTP server for local development.

Exposes the same surface used by AscensionLifeOS:
- POST /v1/intelligence
- POST /v1/surface_plan
- GET  /v1/readiness

The server calls src.core.orchestrator.surface_plan. It does not load a neural
model by itself; it uses the existing Python orchestration logic. This is the
first native replacement gate for the OpenAI fallback in AscensionLifeOS.
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.contracts import Shell, Tier
from src.core.orchestrator import surface_plan

PORT = int(os.environ.get("ASCENSION_AI_PORT", "8000"))
HOST = os.environ.get("ASCENSION_AI_HOST", "127.0.0.1")
EXPECTED_TOKEN = os.environ.get("ASCENSION_AI_SERVICE_TOKEN", "").strip()


def _resolve_shell(value: str | None) -> Shell:
    try:
        return Shell(value or "ap")
    except ValueError:
        return Shell.AP


def _resolve_tier(value: str | None) -> Tier:
    mapping = {
        "freeos": Tier.FREE_OS,
        "free": Tier.FREE_OS,
        "lifeos": Tier.LIFE_OS,
        "lifeos_plus": Tier.LIFE_OS_PLUS,
        "pro": Tier.LIFE_OS_PLUS,
        "founderos": Tier.FOUNDER_OS,
        "founder": Tier.FOUNDER_OS,
        "lifeos_infinite": Tier.LIFE_OS_INFINITE,
        "infinite": Tier.LIFE_OS_INFINITE,
    }
    try:
        return mapping.get((value or "").lower().strip(), Tier.LIFE_OS)
    except Exception:
        return Tier.LIFE_OS


def _extract_trigger(body: dict[str, Any]) -> str:
    """Pull the latest user turn or a raw trigger from the payload."""
    messages = body.get("messages") or []
    if isinstance(messages, list):
        for message in reversed(messages):
            if isinstance(message, dict) and message.get("role") == "user":
                return str(message.get("content", "")).strip()
    return str(body.get("trigger", "")).strip() or "Hello."


def _format_intelligence_response(plan: dict[str, Any]) -> dict[str, Any]:
    """Convert a surface_plan result into the /v1/intelligence chat response."""
    cognition = plan.get("cognition") or {}
    domains = cognition.get("domains") or []
    proposed = (plan.get("execution_contract", {}).get("proposed_actions") or [{}])[0]
    proposed_action = proposed.get("action") if isinstance(proposed, dict) else None

    content = f"Ascension AI surface plan: {plan.get('trigger', '')}\n"
    content += f"Detected domains: {', '.join(domains) or 'general'}\n"
    if proposed_action:
        content += f"Proposed action: {proposed_action}\n"
    content += "(Native response is a dev-level surface plan summary. A trained native model will return natural language here.)"

    return {
        "content": content,
        "model": "ascension-native",
        "usage": None,
        "shell": plan.get("shell", "ap"),
        "tier": plan.get("tier", "lifeos"),
        "domains": domains,
        "capabilities": plan.get("capabilities") or {},
        "cognition": cognition,
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[native-server] {fmt % args}")

    def _send_json(self, status: int, data: dict[str, Any]) -> None:
        payload = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if not length:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def _authorize(self) -> bool:
        if not EXPECTED_TOKEN:
            return True
        auth = self.headers.get("Authorization", "")
        if auth == f"Bearer {EXPECTED_TOKEN}":
            return True
        self._send_json(401, {"error": "unauthorized"})
        return False

    def do_GET(self) -> None:
        if self.path == "/v1/readiness":
            self._send_json(200, {"ready": True, "surface": "ascension-native"})
        else:
            self._send_json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        if not self._authorize():
            return

        try:
            body = self._read_json()
        except json.JSONDecodeError as exc:
            self._send_json(400, {"error": f"invalid_json: {exc}"})
            return

        if self.path == "/v1/surface_plan":
            plan = surface_plan(
                shell=_resolve_shell(body.get("shell")),
                tier=_resolve_tier(body.get("tier")),
                trigger=_extract_trigger(body),
                context=body.get("context", {}),
                available_actions=body.get("available_actions", []),
                allowed_capabilities=body.get("allowed_capabilities", []),
            )
            self._send_json(200, plan)
            return

        if self.path == "/v1/intelligence":
            plan = surface_plan(
                shell=_resolve_shell(body.get("shell")),
                tier=_resolve_tier(body.get("tier")),
                trigger=_extract_trigger(body),
                context=body.get("context", {}),
                available_actions=body.get("allowed_capabilities", []),
                allowed_capabilities=body.get("allowed_capabilities", []),
            )
            self._send_json(200, _format_intelligence_response(plan))
            return

        self._send_json(404, {"error": "not_found"})


def main() -> int:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Ascension native server listening on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
