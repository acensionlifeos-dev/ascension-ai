#!/usr/bin/env bash
set -euo pipefail

cd /workspace/aerynza-ai

ADAPTER="checkpoints/v20_v248_blocker_repair_a"
BASE="Qwen/Qwen3-1.7B"
REVISION="70d244cc86ccca08cf5af4e1e306ecf908b1ad5e"
GPU=1

echo "=== v248-a evaluation queue waiting for training to finish ==="
# wait for training receipt
while [[ ! -f "${ADAPTER}/ascension_training_receipt.json" ]]; do
  sleep 10
done
# wait for process to release checkpoint directory lock (train script writes receipt at end)
sleep 30

mkdir -p logs evals/results

run_step() {
  local name="$1"
  shift
  echo "=== ${name} ==="
  if "$@" > "logs/${name}.log" 2>&1; then
    echo "PASS ${name}"
    return 0
  else
    echo "FAIL ${name}"
    return 1
  fi
}

# Integrated runtime gate
echo "=== v248-a integrated runtime gate ==="
CUDA_VISIBLE_DEVICES="${GPU}" python -u scripts/evaluate_qwen_integrated_runtime.py \
  --model "${BASE}" --adapter "${ADAPTER}" \
  --tokens 128 --output "evals/results/v20_v248_blocker_repair_a_integrated_runtime_gate.json" \
  > logs/v20_v248_blocker_repair_a_integrated_runtime_gate.log 2>&1
python3 -c "
import json, pathlib, sys
p=pathlib.Path('evals/results/v20_v248_blocker_repair_a_integrated_runtime_gate.json')
d=json.loads(p.read_text())
print('canonical:', d.get('canonical_pass_count'), '/', d.get('canonical_case_count'))
print('receipt:', d.get('receipt_truth_pass_count'), '/', d.get('receipt_truth_case_count'))
print('automatic_gate_passed:', d.get('automatic_gate_passed'))
print('promotion_status:', d.get('promotion_status'))
sys.exit(0 if d.get('automatic_gate_passed') else 1)
"

# Replacement quality gate
echo "=== v248-a replacement quality gate ==="
CUDA_VISIBLE_DEVICES="${GPU}" python -u scripts/evaluate_qwen_replacement_quality.py \
  --model "${BASE}" --adapter "${ADAPTER}" \
  --tokens 128 --output "evals/results/v20_v248_blocker_repair_a_replacement_quality.json" \
  > logs/v20_v248_blocker_repair_a_replacement_quality.log 2>&1
python3 -c "
import json, pathlib, sys
p=pathlib.Path('evals/results/v20_v248_blocker_repair_a_replacement_quality.json')
d=json.loads(p.read_text())
print('replacement:', d.get('passed'), '/', d.get('total'))
print('production_replacement_ready:', d.get('production_replacement_ready'))
sys.exit(0 if d.get('automatic_gate_passed') else 1)
"

# 640-capability gate
echo "=== v248-a 640-capability gate ==="
CUDA_VISIBLE_DEVICES="${GPU}" python -u scripts/evaluate_per_capability.py \
  --model "${BASE}" --model-revision "${REVISION}" --adapter "${ADAPTER}" \
  --tokens 128 --output "evals/results/v20_v248_blocker_repair_a_per_capability_gate.json" \
  --capability-gates evals/per_capability_gates.json \
  > logs/v20_v248_blocker_repair_a_per_capability_gate.log 2>&1
python3 -c "
import json, pathlib, sys
p=pathlib.Path('evals/results/v20_v248_blocker_repair_a_per_capability_gate.json')
d=json.loads(p.read_text())
print('640:', d.get('passed'), '/', d.get('total_capabilities'), 'rate', d.get('pass_rate'))
sys.exit(0 if d.get('pass_rate',0)>=0.99 else 1)
"

# Semantic release gate v2
echo "=== v248-a semantic release gate v2 ==="
python -u scripts/semantic_release_gate_v2.py \
  --report "evals/results/v20_v248_blocker_repair_a_per_capability_gate.json" \
  --capability-gates evals/per_capability_gates.json \
  --output "evals/results/v20_v248_blocker_repair_a_semantic_release_gate_v2.json" \
  > logs/v20_v248_blocker_repair_a_semantic_release_gate_v2.log 2>&1
python3 -c "
import json, pathlib, sys
p=pathlib.Path('evals/results/v20_v248_blocker_repair_a_semantic_release_gate_v2.json')
d=json.loads(p.read_text())
print('semantic automatic:', d.get('summary',{}).get('automatic_passed'), '/', d.get('summary',{}).get('total'))
print('semantic effective:', d.get('summary',{}).get('effective_passed'), '/', d.get('summary',{}).get('total'))
print('semantic_release_gate_passed:', d.get('summary',{}).get('semantic_release_gate_passed'))
"

echo "=== v248-a evaluation queue complete ==="
