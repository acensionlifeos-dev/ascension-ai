#!/usr/bin/env bash
set -euo pipefail

cd /workspace/aerynza-ai
mkdir -p logs evals/results

python -u scripts/semantic_release_gate_v2.py \
  --report evals/results/v20_v246_balanced_repair_a_per_capability_gate.json \
  --capability-gates evals/per_capability_gates.json \
  --output evals/results/v20_v246_balanced_repair_a_semantic_release_gate_v2.json \
  > logs/v20_v246_balanced_repair_a_semantic_release_gate_v2.log 2>&1
