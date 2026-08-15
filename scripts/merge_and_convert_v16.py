"""Merge proven_parent and v6b full models and convert to a single GGUF."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LLAMA_CPP = ROOT / "vendor" / "llama.cpp"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_llama_cpp() -> None:
    if not (LLAMA_CPP / "convert_hf_to_gguf.py").is_file():
        LLAMA_CPP.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", "https://github.com/ggerganov/llama.cpp.git", str(LLAMA_CPP)],
            check=True,
        )
    subprocess.run(["pip", "install", "-q", "gguf", "torch"], check=True)


def merge_into_state_dict(adapter_path: str, device: str = "0") -> dict:
    import gc
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM

    base = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3-1.7B",
        torch_dtype=torch.bfloat16,
        device_map=f"cuda:{device}",
    )
    peft = PeftModel.from_pretrained(base, adapter_path)
    merged = peft.merge_and_unload()
    sd = {k: v.to("cpu") for k, v in merged.state_dict().items()}
    del peft, merged, base
    gc.collect()
    torch.cuda.empty_cache()
    return sd


def main() -> int:
    ensure_llama_cpp()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    proven = merge_into_state_dict("checkpoints/proven_parent_grow018_v7_a", device="0")
    v6b = merge_into_state_dict("checkpoints/grow161_all_v6b_a", device="0")

    # Weighted full-model average: 70% proven (generic safety) + 30% v6b (capabilities)
    merged_state = {k: 0.7 * proven[k] + 0.3 * v6b[k] for k in proven if k in v6b}

    base = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3-1.7B",
        torch_dtype=torch.bfloat16,
        device_map="cpu",
    )
    base.load_state_dict(merged_state, strict=True)

    out_dir = ROOT / "models" / "v16_merged_full"
    out_dir.mkdir(parents=True, exist_ok=True)
    base.save_pretrained(out_dir)

    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-1.7B")
    tokenizer.save_pretrained(out_dir)

    gguf_out = ROOT / "models" / "v16_merged_70_30.gguf"
    subprocess.run(
        [
            sys.executable,
            str(LLAMA_CPP / "convert_hf_to_gguf.py"),
            str(out_dir),
            "--outfile", str(gguf_out),
            "--outtype", "q8_0",
        ],
        check=True,
    )

    digest = sha256(gguf_out)
    print(f"v16 merged GGUF: {gguf_out}  sha256: {digest}  size: {gguf_out.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
