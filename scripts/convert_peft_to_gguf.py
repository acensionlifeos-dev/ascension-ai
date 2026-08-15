"""Convert a Qwen PEFT LoRA to a llama.cpp GGUF LoRA for the native runtime."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LLAMA_CPP = ROOT / "vendor" / "llama.cpp"


def ensure_llama_cpp() -> None:
    if not (LLAMA_CPP / "convert_lora_to_gguf.py").is_file():
        LLAMA_CPP.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", "https://github.com/ggerganov/llama.cpp.git", str(LLAMA_CPP)],
            check=True,
        )
    subprocess.run(["pip", "install", "-q", "gguf", "torch", "peft", "transformers", "huggingface-hub"], check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert a PEFT LoRA to a llama.cpp GGUF LoRA")
    parser.add_argument("--adapter", required=True, help="Path to PEFT adapter directory")
    parser.add_argument("--base-model", default="Qwen/Qwen3-1.7B", help="Base model for LoRA")
    parser.add_argument("--outtype", default="f16", help="Output type for LoRA")
    parser.add_argument("--output", default="models/ascension_lora.gguf", help="Output GGUF LoRA path")
    args = parser.parse_args(argv)

    ensure_llama_cpp()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(LLAMA_CPP) + os.pathsep + env.get("PYTHONPATH", "")
    subprocess.run(
        [
            sys.executable,
            str(LLAMA_CPP / "convert_lora_to_gguf.py"),
            "--outtype", args.outtype,
            "--model-base", args.base_model,
            args.adapter,
            str(output),
        ],
        env=env,
        check=True,
    )
    print(f"Converted LoRA saved to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
