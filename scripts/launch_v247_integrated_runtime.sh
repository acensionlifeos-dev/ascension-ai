#!/usr/bin/env bash
set -euo pipefail

cd /workspace/aerynza-ai
mkdir -p logs evals/results

# Run integrated runtime for v247-a; use GPU 0 since both are idle
CUDA_VISIBLE_DEVICES=0 nohup python -u scripts/evaluate_qwen_integrated_runtime.py \
  --model Qwen/Qwen3-1.7B \
  --adapter checkpoints/v20_v247_presence_mesh_a \
  --tokens 128 \
  --output evals/results/v20_v247_presence_mesh_a_integrated_runtime_gate.json \
  > logs/v20_v247_presence_mesh_a_integrated_runtime_gate.log 2>&1 &
echo "v20_v247_presence_mesh_a pid=$!"
