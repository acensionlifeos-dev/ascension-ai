"""Static durability checks for the long-running causal general trainer."""

from pathlib import Path


SOURCE = (Path(__file__).resolve().parent / "train_ascension_general_v5.py").read_text(encoding="utf-8")


def main() -> int:
    checks = {
        "explicit resume flag": '"--resume"' in SOURCE,
        "missing recovery fails closed": "Resume requested but recovery checkpoint is missing" in SOURCE,
        "configuration mismatch fails closed": "saved_config_values != config.__dict__" in SOURCE,
        "step range is validated": "outside the resumable range" in SOURCE,
        "model state is restored": 'model.load_state_dict(recovery["model_state_dict"])' in SOURCE,
        "optimizer state is restored": 'optimizer.load_state_dict(recovery["optimizer_state_dict"])' in SOURCE,
        "scheduler state is saved": '"scheduler_state_dict": scheduler.state_dict()' in SOURCE,
        "scheduler state is restored": 'scheduler.load_state_dict(recovery["scheduler_state_dict"])' in SOURCE,
        "legacy recovery does not restart warmup": "scheduler.last_epoch = saved_step" in SOURCE,
        "loss state is durable": all(field in SOURCE for field in ('"best_loss": best_loss', '"total_loss": total_loss', '"window_loss": window_loss')),
        "final checkpoint records step": '"step": step' in SOURCE,
    }
    for label, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} {label}")
    if not all(checks.values()):
        return 1
    print(f"General v5 resume contract passed: {len(checks)}/{len(checks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
