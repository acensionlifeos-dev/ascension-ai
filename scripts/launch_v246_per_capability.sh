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

  CUDA_VISIBLE_DEVICES="${gpu}" nohup python -u scripts/evaluate_per_capability.py \
    --model Qwen/Qwen3-1.7B \
    --model-revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e \
    --adapter "checkpoints/${name}" \
    --tokens 128 \
    --output "evals/results/${name}_per_capability_gate.json" \
    --capability-gates evals/per_capability_gates.json \
    > "logs/${name}_per_capability_gate.log" 2>&1 &
  echo "${name} pid=$! gpu=${gpu}"
}

run_eval 0 v20_v246_balanced_repair_a
run_eval 1 v20_v246_balanced_repair_b
