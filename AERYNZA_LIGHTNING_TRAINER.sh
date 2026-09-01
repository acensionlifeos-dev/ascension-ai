#!/bin/bash
# Aerynza AI — fail-closed Lightning v20 1.7B launcher.
set -euo pipefail

export PATH="/home/zeus/miniconda3/bin:$PATH"
export HOME="/home/zeus"
export HF_HOME="/home/zeus/.hfcache"
export HF_HUB_ENABLE_HF_TRANSFER=1

cd /home/zeus

if [ ! -d "/home/zeus/aerynza" ]; then
    echo "[Aerynza] Cloning repo..."
    git clone --depth 1 https://github.com/acensionlifeos-dev/ascension-ai.git aerynza
fi

cd aerynza

echo "[Aerynza] Installing GPU torch (cu124) and training deps..."
python3 -m pip install -q -U torch==2.4.0 --index-url https://download.pytorch.org/whl/cu124
python3 -m pip install -q -r requirements-training.txt

echo "[Aerynza] Verifying CUDA and GPU memory..."
python3 - <<'PY'
import torch
if not torch.cuda.is_available():
    raise SystemExit("CUDA_REQUIRED: refusing to run v20 on CPU")
gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
print({"gpu": torch.cuda.get_device_name(0), "vram_gb": round(gb, 2)})
if gb < 14:
    raise SystemExit("INSUFFICIENT_VRAM: v20 requires at least 14 GB")
PY

echo "[Aerynza] Building and validating the leakage-resistant v20 curriculum..."
python3 -u scripts/build_aerynza_ambient_v20.py
python3 -u scripts/build_v20_curriculum.py
python3 -u scripts/test_build_v20_curriculum.py
python3 -u scripts/test_aerynza_v20_data_quality.py
python3 -u scripts/train_qwen_ascension_lora.py \
    --curriculum "evals/training/aerynza_v20_balanced_master.jsonl" \
    --eval-curriculum "evals/training/aerynza_v20_ambient_heldout.jsonl" \
    --validate-only

OUT="checkpoints/aerynza_qwen3_1_7b_v20_candidate"
if [ -e "$OUT" ]; then
    echo "OUTPUT_EXISTS: $OUT — refusing to overwrite evidence"
    exit 1
fi

echo "[Aerynza] Starting the 1.7B v20 train-and-prove pipeline. v19 remains protected."
nohup python3 -u scripts/run_v20_pipeline.py > training-v20.log 2>&1 &

echo $! > training-v20.pid

sleep 5

echo "[Aerynza] Training started. Recent log:"
tail -n 40 training-v20.log || true
echo "[Aerynza] Active Python processes:"
ps aux | grep -E 'python.*train_qwen' | grep -v grep || true
echo "[Aerynza] PID: $(cat training-v20.pid)"
echo "[Aerynza] Tail with: tail -f /home/zeus/aerynza/training-v20.log"
