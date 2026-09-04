#!/usr/bin/env bash
set -euo pipefail

cd /workspace/aerynza-ai
mkdir -p logs checkpoints

CURRICULUM="evals/training/aerynza_product_v247_presence_mesh.jsonl"
PARENT="checkpoints/v20_v242_final_canonical_repair_b"

gpu=1
name="v20_v247_presence_mesh_a"

if pgrep -f "output-dir checkpoints/${name}" >/dev/null; then
  echo "${name} already running"
  exit 0
fi
if [[ -d "checkpoints/${name}" ]] && [[ -n "$(ls -A "checkpoints/${name}" 2>/dev/null)" ]]; then
  echo "${name} already has output; refusing to overwrite"
  exit 0
fi

CUDA_VISIBLE_DEVICES="${gpu}" nohup python -u scripts/train_qwen_ascension_lora.py \
  --model Qwen/Qwen3-1.7B \
  --model-revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e \
  --curriculum "${CURRICULUM}" \
  --resume-adapter "${PARENT}" \
  --output-dir "checkpoints/${name}" \
  --epochs 1.0 \
  --learning-rate 3.0e-6 \
  --max-length 768 \
  > "logs/${name}.log" 2>&1 &
echo "${name} pid=$! gpu=${gpu}"
