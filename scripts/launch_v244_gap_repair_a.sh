#!/usr/bin/env bash
# v244-a gap-repair companion run, lower LR, same proven v242-B parent.
set -euo pipefail

cd /workspace/aerynza-ai
mkdir -p logs checkpoints evals/results

CURRICULUM="evals/training/aerynza_product_v243_semantic_precision.jsonl"
PARENT="checkpoints/v20_v242_final_canonical_repair_b"
NAME="v20_v244_gap_repair_a"

if pgrep -f "output-dir checkpoints/${NAME}" >/dev/null; then
  echo "${NAME} already running"
  exit 0
fi
if [[ -d "checkpoints/${NAME}" ]] && [[ -n "$(ls -A "checkpoints/${NAME}" 2>/dev/null)" ]]; then
  echo "${NAME} already has output; refusing to overwrite"
  exit 0
fi

CUDA_VISIBLE_DEVICES=1 nohup python -u scripts/train_qwen_ascension_lora.py \
  --model Qwen/Qwen3-1.7B \
  --model-revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e \
  --curriculum "${CURRICULUM}" \
  --resume-adapter "${PARENT}" \
  --output-dir "checkpoints/${NAME}" \
  --epochs 2.0 \
  --learning-rate 5.0e-6 \
  --max-length 768 \
  > "logs/${NAME}.log" 2>&1 &
echo "${NAME} pid=$! gpu=1 lr=5.0e-6 parent=${PARENT}"
