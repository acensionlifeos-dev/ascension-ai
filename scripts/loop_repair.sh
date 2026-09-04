#!/usr/bin/env bash
# Continuous repair loop: train -> evaluate -> gate -> build next curriculum.
# Run inside a tmux/screen session on a Vast GPU instance.
set -euo pipefail

cd /workspace/aerynza-ai
mkdir -p logs checkpoints evals/results

# Starting point defaults to the best v237 recovery adapter; override via env vars.
PARENT="${PARENT:-checkpoints/v20_v237_recovery_d}"
PARENT_NAME="${PARENT_NAME:-v237_recovery_d}"
GEN="${GEN:-238}"

# Keep iterating until the semantic gate reports 640/640 effective passes.
while true; do
  echo "=== Generation v${GEN} repair starting at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

  # 1. Build curriculum from the previous best gate report.
  CURRICULUM="evals/training/aerynza_product_v${GEN}_repair.jsonl"
  python3 scripts/build_repair_curriculum.py \
    --gate-report "evals/results/v20_${PARENT_NAME}_semantic_gate_v2.json" \
    --output "${CURRICULUM}" \
    --version-tag "v${GEN}" \
    --fix-repetitions 12 \
    --canonical-repetitions 16 \
    > "logs/v${GEN}_build.log" 2>&1
  echo "Curriculum built: ${CURRICULUM}"

  # 2. Launch two repair candidates on the two GPUs.
  NAME_A="v20_v${GEN}_repair_a"
  NAME_B="v20_v${GEN}_repair_b"

  CUDA_VISIBLE_DEVICES=0 nohup python3 -u scripts/train_qwen_ascension_lora.py \
    --model Qwen/Qwen3-1.7B \
    --model-revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e \
    --curriculum "${CURRICULUM}" \
    --resume-adapter "${PARENT}" \
    --output-dir "checkpoints/${NAME_A}" \
    --epochs 1.0 \
    --learning-rate 1.0e-5 \
    --max-length 768 \
    > "logs/${NAME_A}.log" 2>&1 &
  PID_A=$!

  CUDA_VISIBLE_DEVICES=1 nohup python3 -u scripts/train_qwen_ascension_lora.py \
    --model Qwen/Qwen3-1.7B \
    --model-revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e \
    --curriculum "${CURRICULUM}" \
    --resume-adapter "${PARENT}" \
    --output-dir "checkpoints/${NAME_B}" \
    --epochs 1.0 \
    --learning-rate 2.0e-5 \
    --max-length 768 \
    > "logs/${NAME_B}.log" 2>&1 &
  PID_B=$!

  echo "Training: ${NAME_A} pid=${PID_A} gpu=0 lr=1.0e-5; ${NAME_B} pid=${PID_B} gpu=1 lr=2.0e-5"
  wait ${PID_A}
  wait ${PID_B}
  echo "Training finished at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

  # 3. Evaluate both candidates.
  python3 scripts/evaluate_per_capability.py \
    --adapter "checkpoints/${NAME_A}" \
    --output "evals/results/${NAME_A}_per_capability_gate.json" \
    --tokens 128 \
    > "logs/${NAME_A}_eval.log" 2>&1

  python3 scripts/evaluate_per_capability.py \
    --adapter "checkpoints/${NAME_B}" \
    --output "evals/results/${NAME_B}_per_capability_gate.json" \
    --tokens 128 \
    > "logs/${NAME_B}_eval.log" 2>&1

  echo "Evaluation finished at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

  # 4. Run semantic gates.
  python3 scripts/semantic_release_gate_v2.py \
    --report "evals/results/${NAME_A}_per_capability_gate.json" \
    --output "evals/results/${NAME_A}_semantic_gate_v2.json" \
    --omit-full-responses \
    > "logs/${NAME_A}_gate.log" 2>&1

  python3 scripts/semantic_release_gate_v2.py \
    --report "evals/results/${NAME_B}_per_capability_gate.json" \
    --output "evals/results/${NAME_B}_semantic_gate_v2.json" \
    --omit-full-responses \
    > "logs/${NAME_B}_gate.log" 2>&1

  echo "Gates finished at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

  # 5. Pick the best candidate and update parent for next generation.
  BEST_INFO=$(python3 scripts/pick_best_candidate.py "${NAME_A}" "${NAME_B}")

  BEST_NAME=$(echo "${BEST_INFO}" | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])")
  BEST_PASSED=$(echo "${BEST_INFO}" | python3 -c "import sys,json; print(json.load(sys.stdin)['effective_passed'])")
  BEST_RATE=$(echo "${BEST_INFO}" | python3 -c "import sys,json; print(json.load(sys.stdin)['effective_rate'])")
  BEST_GATE=$(echo "${BEST_INFO}" | python3 -c "import sys,json; print(json.load(sys.stdin)['gate_passed'])")

  echo "Best candidate: ${BEST_NAME} effective_passed=${BEST_PASSED}/${BEST_RATE} gate_passed=${BEST_GATE}"

  if [[ "${BEST_GATE}" == "True" ]]; then
    echo "=== Semantic gate passed at generation v${GEN}. Stopping loop. ==="
    exit 0
  fi

  PARENT="checkpoints/${BEST_NAME}"
  PARENT_NAME="${BEST_NAME}"
  GEN=$((GEN + 1))
  echo "=== Moving to generation v${GEN} from parent ${PARENT} ==="
done
