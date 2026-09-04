#!/usr/bin/env bash
# Pick up after a manual evaluation/gate run and continue the repair loop.
set -euo pipefail

cd /workspace/aerynza-ai

# Wait for any running per-capability evaluations to finish.
echo "Waiting for evaluations to finish at $(date -u +%Y-%m-%dT%H:%M:%SZ)..."
while pgrep -f "evaluate_per_capability.py" >/dev/null; do
  sleep 60
done
echo "Evaluations finished at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Default: continue from v238 results.
BASE_GEN="${BASE_GEN:-238}"
CANDIDATE_A="v20_v${BASE_GEN}_repair_a"
CANDIDATE_B="v20_v${BASE_GEN}_repair_b"

# Run gates if they do not already exist.
for cand in "${CANDIDATE_A}" "${CANDIDATE_B}"; do
  gate="evals/results/${cand}_semantic_gate_v2.json"
  report="evals/results/${cand}_per_capability_gate.json"
  if [[ ! -f "${gate}" ]] && [[ -f "${report}" ]]; then
    echo "Running semantic gate for ${cand}..."
    python3 scripts/semantic_release_gate_v2.py \
      --report "${report}" \
      --output "${gate}" \
      --omit-full-responses \
      > "logs/${cand}_gate.log" 2>&1
  fi
done

# Pick the best candidate.
BEST_NAME=$(python3 scripts/pick_best_candidate.py "${CANDIDATE_A}" "${CANDIDATE_B}")

if [[ "${BEST_NAME}" == "MISSING" ]]; then
  echo "Gate results missing for one or both candidates; cannot continue automatically."
  exit 1
fi

BEST=$(echo "${BEST_NAME}" | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])")
PASSED=$(echo "${BEST_NAME}" | python3 -c "import sys,json; print(json.load(sys.stdin)['effective_passed'])")
RATE=$(echo "${BEST_NAME}" | python3 -c "import sys,json; print(json.load(sys.stdin)['effective_rate'])")
GATE_PASSED=$(echo "${BEST_NAME}" | python3 -c "import sys,json; print(json.load(sys.stdin)['gate_passed'])")

echo "Best v${BASE_GEN} candidate: ${BEST} effective_passed=${PASSED} rate=${RATE} gate_passed=${GATE_PASSED}"

if [[ "${GATE_PASSED}" == "True" ]]; then
  echo "Semantic gate passed. Stopping."
  exit 0
fi

# Continue the loop starting from the next generation.
NEXT_GEN=$((BASE_GEN + 1))
export PARENT="checkpoints/${BEST}"
export PARENT_NAME="${BEST#v20_}"
export GEN="${NEXT_GEN}"
exec bash scripts/loop_repair.sh
