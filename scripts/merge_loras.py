"""Merge two LoRA adapters: result = base_adapter + scale * (capable_adapter - base_adapter)."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge two PEFT LoRAs")
    parser.add_argument("--base-adapter", required=True)
    parser.add_argument("--capable-adapter", required=True)
    parser.add_argument("--scale", type=float, default=0.2)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    from safetensors.torch import load_file, save_file

    root = Path(__file__).resolve().parents[1]
    base_path = root / args.base_adapter
    cap_path = root / args.capable_adapter
    out_path = root / args.output
    out_path.mkdir(parents=True, exist_ok=True)

    base = load_file(base_path / "adapter_model.safetensors")
    cap = load_file(cap_path / "adapter_model.safetensors")
    merged = {}
    for key in base:
        if key in cap:
            merged[key] = base[key] + args.scale * (cap[key] - base[key])
        else:
            merged[key] = base[key]
    for key in cap:
        if key not in merged:
            merged[key] = cap[key]

    save_file(merged, out_path / "adapter_model.safetensors")
    for name in ("adapter_config.json", "tokenizer_config.json"):
        src = cap_path / name
        if src.is_file():
            shutil.copy(src, out_path / name)
    (out_path / "README.md").write_text(f"Merged adapter from {base_path.name} + {args.scale} * {cap_path.name}\n", encoding="utf-8")
    print(f"Merged {len(merged)} tensors into {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
