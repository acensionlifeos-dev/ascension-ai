#!/usr/bin/env bash
set -euo pipefail

cd /workspace/aerynza-ai
python -u scripts/evaluate_integrated_promotion.py \
  --candidate-gate evals/results/v20_v246_balanced_repair_a_integrated_runtime_gate.json \
  --output evals/results/v20_v246_balanced_repair_a_integrated_promotion_gate.json \
  > logs/v20_v246_balanced_repair_a_integrated_promotion_gate.log 2>&1
