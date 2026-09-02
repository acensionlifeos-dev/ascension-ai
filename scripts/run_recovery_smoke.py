"""Ten-step CPU adapter mechanics test; never a promotion or readiness gate."""
from pathlib import Path
import torch
from huggingface_hub import snapshot_download
import train_qwen_ascension_lora as trainer


def main():
    output = "checkpoints/qwen_recovery_smoke_20260831"
    if (trainer.ROOT / output).exists():
        raise FileExistsError("Refusing to overwrite an existing candidate")
    torch.set_num_threads(4)
    model = snapshot_download("Qwen/Qwen3-0.6B", revision="c1899de289a04d12100db370d81485cdf75e47ca",
                              local_files_only=True)
    original = trainer.training_arguments
    def bounded_arguments(**kwargs):
        kwargs.update(max_steps=10, save_strategy="steps", save_steps=2, save_total_limit=2,
                      logging_steps=1, use_cpu=True, bf16=False, fp16=False,
                      dataloader_num_workers=0)
        return original(**kwargs)
    trainer.training_arguments = bounded_arguments
    print("RECOVERY SMOKE ONLY: pinned official base, 10 steps, CPU, no promotion", flush=True)
    return trainer.main(["--model", model, "--curriculum", "evals/training/ascension_product_v1.jsonl",
                         "--output-dir", output, "--max-length", "256", "--epochs", "1",
                         "--learning-rate", "0.00001"])


if __name__ == "__main__":
    raise SystemExit(main())
