#!/usr/bin/env bash
# Start the native Ascension AI chat endpoint for local development
set -e
export PYTHONPATH="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$(dirname "$0")/native_chat_endpoint.py"
