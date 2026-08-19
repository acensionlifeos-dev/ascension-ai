"""Deploy the current Ascension AI repo to a Vast.ai GPU instance and start training.

Usage:
    python scripts/vast_gpu_launch.py --host 142.214.185.187 --port 20544

Requires an SSH key already added to the Vast account and the instance running.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTE_DIR = "/workspace/ascension-ai"
IDENTITY = Path.home() / ".ssh" / "id_ed25519_vast_ascension"


def run(cmd: list[str], check: bool = True) -> int:
    print("[Vast] " + " ".join(str(c) for c in cmd), flush=True)
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    if check and result.returncode != 0:
        print(f"[Vast] Command failed with exit code {result.returncode}", flush=True)
        sys.exit(result.returncode)
    return result.returncode


def ssh(host: str, port: int, command: str) -> None:
    run([
        "ssh",
        "-p", str(port),
        "-i", str(IDENTITY),
        "-o", "StrictHostKeyChecking=accept-new",
        f"root@{host}",
        command,
    ])


def rsync_repo(host: str, port: int) -> None:
    """Sync repo to remote using rsync (preferred) or scp fallback."""
    ssh_path = f"ssh -p {port} -i {IDENTITY} -o StrictHostKeyChecking=accept-new"
    if subprocess.run(["which", "rsync"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        run([
            "rsync", "-avz", "--delete",
            "-e", ssh_path,
            str(ROOT) + "/",
            f"root@{host}:{REMOTE_DIR}/",
        ])
    else:
        run([
            "scp", "-P", str(port), "-i", str(IDENTITY), "-r",
            str(ROOT),
            f"root@{host}:{REMOTE_DIR}",
        ])


def setup_and_train(host: str, port: int, args: argparse.Namespace) -> None:
    setup_cmd = (
        f"mkdir -p {REMOTE_DIR} && "
        f"cd {REMOTE_DIR} && "
        f"python3 -m pip install -q -r requirements-training.txt && "
        f"python3 scripts/setup_gpu_training.py "
        f"--version {args.version} "
        f"--steps {args.steps} "
        f"--batch-size {args.batch_size} "
        f"--learning-rate {args.learning_rate} "
        f"--product-repeats {args.product_repeats} "
        f"--general-replay-ratio {args.general_replay_ratio} "
        f"--save-every {args.save_every} "
        f"--print-every {args.print_every}"
    )
    if args.resume_latest:
        setup_cmd += " --resume-latest"
    if args.assistant_only_loss:
        setup_cmd += " --assistant-only-loss"
    setup_cmd += " && nohup python3 -u scripts/setup_gpu_training.py"
    if args.torchrun:
        setup_cmd = (
            f"cd {REMOTE_DIR} && "
            f"python3 -m pip install -q -r requirements-training.txt && "
            f"nohup python3 -m torch.distributed.run --nproc_per_node={args.gpus} "
            f"scripts/setup_gpu_training.py --batch-size {args.batch_size} "
            f"--steps {args.steps} --learning-rate {args.learning_rate}"
        )
    ssh(host, port, setup_cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy and launch Ascension AI training on a Vast.ai GPU instance")
    parser.add_argument("--host", required=True, help="Vast instance IP address")
    parser.add_argument("--port", type=int, required=True, help="Vast instance SSH port")
    parser.add_argument("--version", default="ascension_product_v6")
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--product-repeats", type=int, default=12)
    parser.add_argument("--general-replay-ratio", type=float, default=0.2)
    parser.add_argument("--save-every", type=int, default=2500)
    parser.add_argument("--print-every", type=int, default=250)
    parser.add_argument("--resume-latest", action="store_true")
    parser.add_argument("--assistant-only-loss", action="store_true")
    parser.add_argument("--torchrun", action="store_true", help="use torchrun for multi-GPU")
    parser.add_argument("--gpus", type=int, default=2, help="number of GPUs for torchrun")
    parser.add_argument("--sync-only", action="store_true", help="only sync repo, do not start training")
    args = parser.parse_args()

    if not IDENTITY.exists():
        print(f"[Vast] SSH key not found: {IDENTITY}", file=sys.stderr)
        return 1

    print(f"[Vast] Syncing repo to {args.host}:{args.port} ...")
    rsync_repo(args.host, args.port)

    if args.sync_only:
        print("[Vast] Sync complete. Training not started.")
        return 0

    print("[Vast] Starting training on remote GPU...")
    setup_and_train(args.host, args.port, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
