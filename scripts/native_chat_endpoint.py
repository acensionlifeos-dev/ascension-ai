"""Native chat endpoint for local testing.

Runs a lightweight HTTP server that invokes the deterministic parts of
the Ascension contract engine. It does not load model weights and does not
promote the native model to primary; it is for evaluation and development only.
"""

import json
import os
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# Ensure src/ is importable
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.orchestrator import (
    deterministic_conversation_repair,
    deterministic_first_pass,
    deterministic_scope_answer,
    prepare_inference,
)
from src.core.contracts import Shell, Tier


HOST = os.environ.get('ASCENSION_NATIVE_HOST', '127.0.0.1')
PORT = int(os.environ.get('ASCENSION_NATIVE_PORT', '8000'))


def handle_chat(body: dict) -> dict:
    """Return a deterministic native response or a stub."""
    messages = body.get('messages', [])
    capability = body.get('capability', 'ascension_chat')
    shell_name = body.get('shell', 'core')
    surface = body.get('surface', 'chat')
    mode = body.get('mode', 'conversation')
    context = body.get('context', {})

    try:
        shell = Shell(shell_name)
    except ValueError:
        shell = Shell.CORE

    tier = Tier.LIFE_OS if shell in (Shell.AP, Shell.LIFE_OS, Shell.NEXUS_HOME) else Tier.FOUNDER_OS
    allowed = [capability.replace('ascension_', '')] if capability.startswith('ascension_') else []

    prepared = prepare_inference(
        shell=shell,
        tier=tier,
        messages=messages,
        context=context,
        surface=surface,
        mode=mode,
        allowed_capabilities=allowed
    )

    latest = messages[-1].get('content', '') if messages else ''
    first_pass = (
        deterministic_scope_answer(shell, latest)
        or deterministic_conversation_repair(latest, mode)
        or deterministic_first_pass(prepared['cognition'], mode)
    )

    if first_pass:
        return {
            'content': first_pass,
            'model': 'Ascension Contract Engine',
            'provider': 'ascension-native',
            'tokensUsed': 0,
            'cognition': prepared.get('cognition'),
        }

    return {
        'content': f'Ascension native response for {capability} (stub: generative model not loaded yet).',
        'model': 'Ascension Candidate 3B (stub)',
        'provider': 'ascension-native',
        'tokensUsed': 0,
        'fallback': True,
    }


class NativeChatHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Suppress request logging to avoid leaking details
        pass

    def _json_response(self, status: int, data: dict):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode('utf-8'))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != '/chat':
            self._json_response(404, {'error': 'Not found'})
            return

        length = int(self.headers.get('Content-Length', 0))
        if not length:
            self._json_response(400, {'error': 'Empty body'})
            return

        try:
            body = json.loads(self.rfile.read(length).decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._json_response(400, {'error': 'Invalid JSON'})
            return

        start = time.perf_counter()
        result = handle_chat(body)
        latency_ms = round((time.perf_counter() - start) * 1000)
        result['latency_ms'] = latency_ms
        self._json_response(200, result)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/health':
            self._json_response(200, {
                'status': 'ok',
                'provider': 'ascension-native',
                'candidate_ready': True,
                'outside_provider': False,
            })
            return
        self._json_response(404, {'error': 'Not found'})


def main():
    server = HTTPServer((HOST, PORT), NativeChatHandler)
    print(f'Native chat endpoint listening on {HOST}:{PORT}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down', flush=True)
        server.shutdown()


if __name__ == '__main__':
    main()
