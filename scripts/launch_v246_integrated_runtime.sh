#!/usr/bin/env bash
set -euo pipefail

cd /workspace/aerynza-ai
mkdir -p logs evals/results

run_gate() {
  local gpu="$1"
  local name="$2"

  if pgrep -f "adapter checkpoints/${name}" >/dev/null; then
    echo "${name} already running"
    return
  fi

  CUDA_VISIBLE_DEVICES="${gpu}" nohup python -u scripts/evaluate_qwen_integrated_runtime.py \
    --model Qwen/Qwen3-1.7B \
    --adapter "checkpoints/${name}" \
    --tokens 128 \
    --output "evals/results/${name}_integrated_runtime_gate.json" \
    > "logs/${name}_integrated_runtime_gate.log" 2>&1 &
  echo "${name} pid=$! gpu=${gpu}"
}

run_gate 0 v20_v246_balanced_repair_a
run_gate 1 v20_v246_balanced_repair_b
