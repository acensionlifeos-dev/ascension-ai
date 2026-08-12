#!/usr/bin/env bash
# Dev startup: native endpoint + TypeScript API
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$(cd "$SCRIPT_DIR/.." && pwd)"

python3 "$SCRIPT_DIR/native_chat_endpoint.py" &
NATIVE_PID=$!

cleanup() {
  kill $NATIVE_PID 2>/dev/null || true
}
trap cleanup EXIT

sleep 2
cd "$SCRIPT_DIR/.."
export ASCENSION_NATIVE_ENABLED=true
export ASCENSION_NATIVE_URL=http://localhost:8000/chat
npm run dev
