"""Native chat endpoint for local testing.

Runs a lightweight HTTP server that invokes the deterministic parts of
the Aerynza contract engine, and falls back to the loaded local model
for open-ended generation. It does not promote the native model to primary;
it is for evaluation and development only.
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
    deterministic_domain_answer,
    deterministic_first_pass,
    deterministic_scope_answer,
    enforce_response_contract,
    prepare_inference,
)
from src.core.contracts import Shell, Tier
from src.core.model_runtime import NativeModelRuntime
from src.core.safety import scan_safety


HOST = os.environ.get('ASCENSION_NATIVE_HOST', '127.0.0.1')
PORT = int(os.environ.get('ASCENSION_NATIVE_PORT', '8000'))

# Lazy-load the native GGUF model once, on first request, to keep startup fast.
_runtime: NativeModelRuntime | None = None


def get_runtime() -> NativeModelRuntime | None:
    global _runtime
    if _runtime is None:
        try:
            _runtime = NativeModelRuntime()
            _runtime.load()
        except Exception:
            _runtime = None
    return _runtime


def handle_chat(body: dict) -> dict:
    """Return a deterministic native response, or fall back to the loaded model."""
    messages = body.get('messages', [])
    capability = body.get('capability', 'ascension_chat')
    shell_name = body.get('shell', 'core')
    surface = body.get('surface', 'chat')
    mode = body.get('mode', 'conversation')
    context = body.get('context', {})
    temperature = body.get('temperature', 0.7)
    max_tokens = body.get('max_tokens', 2048)

    latest = messages[-1].get('content', '') if messages else ''
    safety = scan_safety(latest)
    if safety.action in ('escalate', 'block'):
        return {
            'content': safety.message,
            'model': 'Aerynza Safety Guard',
            'provider': 'Aerynza-Native',
            'tokensUsed': 0,
            'safety': safety.__dict__,
        }

    warn_prefix = ''
    if safety.action == 'warn':
        warn_prefix = safety.message + '\n\n'

    try:
        shell = Shell(shell_name)
    except ValueError:
        shell = Shell.CORE

    tier = Tier.LIFE_OS if shell in (Shell.AP, Shell.LIFE_OS, Shell.NEXUS_HOME) else Tier.FOUNDER_OS
    # General AP chat must retain cross-domain cognition. Specific capability
    # invocations remain tightly scoped to the requested domain.
    allowed = (
        []
        if capability in ('ascension_chat', 'chat', '')
        else [capability.replace('ascension_', '')] if capability.startswith('ascension_') else []
    )

    prepared = prepare_inference(
        shell=shell,
        tier=tier,
        messages=messages,
        context=context,
        surface=surface,
        mode=mode,
        allowed_capabilities=allowed
    )

    first_pass = (
        deterministic_scope_answer(shell, latest)
        or deterministic_conversation_repair(latest, mode)
        or deterministic_domain_answer(shell, latest, mode)
        or deterministic_first_pass(prepared['cognition'], mode)
    )

    if first_pass:
        return {
            'content': warn_prefix + first_pass,
            'model': 'Aerynza Contract Engine',
            'provider': 'Aerynza-Native',
            'tokensUsed': 0,
            'cognition': prepared.get('cognition'),
            'safety_level': safety.level,
        }

    # Deterministic engine had no match; try the loaded local model.
    runtime = get_runtime()
    if runtime is None:
        return {
            'content': warn_prefix + f'Aerynza native response for {capability} (stub: generative model not loaded yet).',
            'model': 'Aerynza AI (stub)',
            'provider': 'Aerynza-Native',
            'tokensUsed': 0,
            'fallback': True,
            'safety_level': safety.level,
        }

    try:
        model_output = runtime.chat(prepared['messages'], temperature, max_tokens)
        guarded_content = enforce_response_contract(
            model_output['content'], prepared['cognition'], context, mode, latest
        )
        return {
            'content': warn_prefix + guarded_content,
            'model': model_output.get('model', runtime.status().get('model', 'Aerynza AI')),
            'provider': 'Aerynza-Native',
            'tokensUsed': model_output.get('tokensUsed', 0),
            'safety_level': safety.level,
            'cognition': prepared.get('cognition'),
        }
    except Exception as error:
        return {
            'content': warn_prefix + f'Aerynza native response for {capability} (model error: {error}).',
            'model': 'Aerynza AI',
            'provider': 'Aerynza-Native',
            'tokensUsed': 0,
            'fallback': True,
            'safety_level': safety.level,
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
            runtime = get_runtime()
            status = runtime.status() if runtime else {
                'ready': False,
                'error': 'Model not loaded'
            }
            self._json_response(200, {
                'status': 'ok' if status.get('ready') else 'model_unavailable',
                'provider': 'Aerynza-Native',
                'candidate_ready': status.get('ready', False),
                'outside_provider': False,
                'model': status
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
