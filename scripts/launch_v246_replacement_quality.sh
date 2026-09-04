#!/usr/bin/env bash
set -euo pipefail

cd /workspace/aerynza-ai
mkdir -p logs evals/results

run_eval() {
  local gpu="$1"
  local name="$2"

  if pgrep -f "adapter checkpoints/${name}" >/dev/null; then
    echo "${name} already running"
    return
  fi

  CUDA_VISIBLE_DEVICES="${gpu}" nohup python -u scripts/evaluate_qwen_replacement_quality.py \
    --model Qwen/Qwen3-1.7B \
    --adapter "checkpoints/${name}" \
    --tokens 220 \
    --output "evals/results/${name}_replacement_quality.json" \
    > "logs/${name}_replacement_quality.log" 2>&1 &
  echo "${name} pid=$! gpu=${gpu}"
}

run_eval 0 v20_v246_balanced_repair_a
run_eval 1 v20_v246_balanced_repair_b
