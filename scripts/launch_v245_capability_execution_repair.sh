#!/usr/bin/env bash
# v245 capability-execution repair from the proven v242-B release candidate.
# Targets the 40 failures surfaced by v242-B's capability execution gate.
set -euo pipefail

cd /workspace/aerynza-ai
mkdir -p logs checkpoints evals/results

CURRICULUM="evals/training/aerynza_product_v245_capability_execution_repair.jsonl"
PARENT="checkpoints/v20_v242_final_canonical_repair_b"

launch_candidate() {
  local gpu="$1"
  local name="$2"
  local learning_rate="$3"

  if pgrep -f "output-dir checkpoints/${name}" >/dev/null; then
    echo "${name} already running"
    return
  fi
  if [[ -d "checkpoints/${name}" ]] && [[ -n "$(ls -A "checkpoints/${name}" 2>/dev/null)" ]]; then
    echo "${name} already has output; refusing to overwrite"
    return
  fi

  CUDA_VISIBLE_DEVICES="${gpu}" nohup python -u scripts/train_qwen_ascension_lora.py \
    --model Qwen/Qwen3-1.7B \
    --model-revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e \
    --curriculum "${CURRICULUM}" \
    --resume-adapter "${PARENT}" \
    --output-dir "checkpoints/${name}" \
    --epochs 2.0 \
    --learning-rate "${learning_rate}" \
    --max-length 768 \
    > "logs/${name}.log" 2>&1 &
  echo "${name} pid=$! gpu=${gpu} lr=${learning_rate}"
}

launch_candidate 0 v20_v245_capability_execution_repair_a 6.0e-6
launch_candidate 1 v20_v245_capability_execution_repair_b 8.0e-6
