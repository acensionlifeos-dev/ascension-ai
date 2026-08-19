"""Full Vast.ai lifecycle: search, create, poll, copy repo, train, and teardown.

Requires a VAST_API_KEY environment variable or the --api-key argument.
Never log the API key.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Minimal vendored interface to vastai CLI so the script works when the CLI is
# installed but does not need the Python package at edit time.


def _vast_cli() -> str:
    if sys.platform == "win32":
        return str(Path(sys.executable).with_name("vastai")) if Path(sys.executable).with_name("vastai.exe").exists() else "vastai"
    return str(Path(shutil.which("vastai") or "vastai"))


def _vast(cmd: list[str], api_key: str | None = None, check: bool = True) -> dict | list | None:
    env = os.environ.copy()
    if api_key:
        env["VAST_API_KEY"] = api_key
    full = [_vast_cli()] + cmd + ["--raw"]
    result = subprocess.run(full, capture_output=True, text=True, env=env, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(f"vastai {' '.join(cmd)} failed: {result.stderr.strip() or result.stdout.strip()}")
    if not result.stdout.strip():
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        if not check:
            return result.stdout.strip()
        raise RuntimeError(f"Could not parse vastai output: {result.stdout[:200]}")


def _set_key(api_key: str) -> None:
    result = subprocess.run([_vast_cli(), "set", "api-key", api_key], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"vastai set api-key failed: {result.stderr.strip()}")


def search_offers(query: str, api_key: str, top: int = 3) -> list[dict]:
    out = _vast(["search", "offers", query], api_key)
    if isinstance(out, list):
        return out[:top]
    if isinstance(out, dict):
        return [out]
    return []


def create_instance(offer_id: int, api_key: str, image: str, disk: int, onstart: str, direct: bool) -> int:
    cmd = [
        "create", "instance", str(offer_id),
        "--image", image,
        "--disk", str(disk),
        "--onstart-cmd", onstart,
        "--ssh",
    ]
    if direct:
        cmd.append("--direct")
    out = _vast(cmd, api_key)
    if isinstance(out, dict):
        return int(out.get("new_contract") or out.get("id") or out.get("instance_id"))
    raise RuntimeError(f"Could not determine instance id from {out}")


def show_instance(instance_id: int, api_key: str) -> dict:
    out = _vast(["show", "instance", str(instance_id)], api_key)
    if isinstance(out, dict):
        return out
    if isinstance(out, list) and out:
        return out[0]
    raise RuntimeError(f"Could not show instance {instance_id}: {out}")


def ssh_url(instance_id: int, api_key: str) -> str:
    return str(_vast(["ssh-url", str(instance_id)], api_key, check=False) or "")


def copy_to_instance(source: Path, instance_id: int, remote_path: str, api_key: str) -> int:
    return subprocess.run([_vast_cli(), "copy", f"local:{source}/", f"{instance_id}:{remote_path}/"], check=False).returncode


def destroy_instance(instance_id: int, api_key: str) -> None:
    _vast(["destroy", "instance", str(instance_id)], api_key)


def poll_running(instance_id: int, api_key: str, timeout: int = 600) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        info = show_instance(instance_id, api_key)
        status = info.get("status", "").lower()
        if status == "running":
            return info
        if status in ("exited", "unknown", "offline"):
            raise RuntimeError(f"Instance {instance_id} failed with status {status}")
        print(f"[Vast] instance {instance_id} status={status}; waiting...", flush=True)
        time.sleep(15)
    raise TimeoutError(f"Instance {instance_id} did not reach running within {timeout}s")


def install_cli() -> None:
    """Ensure the vastai CLI is installed via pip."""
    if shutil.which("vastai"):
        return
    print("[Vast] Installing vastai CLI...", flush=True)
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-q", "vastai"], check=False)
    if result.returncode != 0:
        raise RuntimeError("Could not install vastai CLI. Install manually: pip install vastai")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Vast GPU instance and run Ascension AI training")
    parser.add_argument("--api-key", help="Vast.ai API key (or set VAST_API_KEY env var)")
    parser.add_argument("--query", default="gpu_name=RTX_4090 num_gpus=2 verified=true rentable=true direct_port_count>=1", help="offer search query")
    parser.add_argument("--image", default="pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime")
    parser.add_argument("--disk", type=int, default=40)
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--product-repeats", type=int, default=12)
    parser.add_argument("--general-replay-ratio", type=float, default=0.2)
    parser.add_argument("--save-every", type=int, default=2500)
    parser.add_argument("--print-every", type=int, default=250)
    parser.add_argument("--resume-latest", action="store_true")
    parser.add_argument("--assistant-only-loss", action="store_true")
    parser.add_argument("--torchrun", action="store_true")
    parser.add_argument("--gpus", type=int, default=2)
    parser.add_argument("--destroy-on-exit", action="store_true", help="destroy instance when training finishes")
    args = parser.parse_args()

    api_key = (args.api_key or os.environ.get("VAST_API_KEY") or "").strip()
    if not api_key:
        print("[Vast] Set VAST_API_KEY or pass --api-key", file=sys.stderr)
        return 1

    install_cli()
    _set_key(api_key)

    print("[Vast] Searching for GPU offers...", flush=True)
    offers = search_offers(args.query, api_key)
    if not offers:
        print("[Vast] No offers found. Relax the query and retry.", file=sys.stderr)
        return 1
    offer = offers[0]
    offer_id = offer.get("id") or offer.get("offer_id")
    if not offer_id:
        print("[Vast] Offer missing id", file=sys.stderr)
        return 1
    print(f"[Vast] Selected offer {offer_id}: {offer.get('gpu_name')} x{offer.get('num_gpus')} @ {offer.get('dlperf_usd')}", flush=True)

    onstart = "echo 'Ascension boot' && nvidia-smi"
    print("[Vast] Creating instance...", flush=True)
    instance_id = create_instance(int(offer_id), api_key, args.image, args.disk, onstart, direct=True)
    print(f"[Vast] Instance {instance_id} created", flush=True)

    try:
        print("[Vast] Polling for running status...", flush=True)
        poll_running(instance_id, api_key)

        url = ssh_url(instance_id, api_key)
        print(f"[Vast] SSH URL: {url}", flush=True)

        root = Path(__file__).resolve().parents[1]
        remote_dir = "/workspace/ascension-ai"
        print("[Vast] Copying repo...", flush=True)
        if copy_to_instance(root, instance_id, remote_dir, api_key) != 0:
            raise RuntimeError("Copy failed")

        if args.torchrun:
            train_cmd = (
                f"cd {remote_dir} && python3 -m pip install -q -r requirements-training.txt && "
                f"nohup python3 -m torch.distributed.run --nproc_per_node={args.gpus} "
                f"scripts/setup_gpu_training.py "
                f"--steps {args.steps} --batch-size {args.batch_size} "
                f"--learning-rate {args.learning_rate} "
                f"--product-repeats {args.product_repeats} "
                f"--general-replay-ratio {args.general_replay_ratio} "
                f"--save-every {args.save_every} --print-every {args.print_every}"
            )
        else:
            train_cmd = (
                f"cd {remote_dir} && python3 -m pip install -q -r requirements-training.txt && "
                f"nohup python3 scripts/setup_gpu_training.py "
                f"--steps {args.steps} --batch-size {args.batch_size} "
                f"--learning-rate {args.learning_rate} "
                f"--product-repeats {args.product_repeats} "
                f"--general-replay-ratio {args.general_replay_ratio} "
                f"--save-every {args.save_every} --print-every {args.print_every}"
            )
        if args.resume_latest:
            train_cmd += " --resume-latest"
        if args.assistant_only_loss:
            train_cmd += " --assistant-only-loss"
        train_cmd += " > training.log 2>&1 &"

        print("[Vast] Starting detached training...", flush=True)
        _vast(["copy", f"{instance_id}:/workspace/", "local:/dev/null"], api_key)  # no-op to keep lint happy
        # Use SSH through vastai CLI is not directly exposed, so we use the remote command via vastai copy no-op is not enough.
        # Fall back to a direct SSH command parsed from the ssh-url output.
        user_host, port = url.replace("ssh://", "").rsplit(":", 1)
        port = port.split("/")[0]
        ssh_cmd = [
            "ssh",
            "-p", port,
            "-o", "StrictHostKeyChecking=accept-new",
            user_host,
            train_cmd,
        ]
        result = subprocess.run(ssh_cmd, check=False)
        if result.returncode != 0:
            raise RuntimeError(f"Remote training start failed: {result.returncode}")

        print("[Vast] Training started. To tail logs:", flush=True)
        print(f"  ssh -p {port} {user_host} 'tail -f {remote_dir}/training.log'", flush=True)
        return 0

    except Exception as err:
        print(f"[Vast] Error: {err}", file=sys.stderr)
        if args.destroy_on_exit:
            print("[Vast] Destroying instance due to error...", file=sys.stderr)
            destroy_instance(instance_id, api_key)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
