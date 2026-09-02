"""Controlled v8: v6 data trained and evaluated under the same strict contract."""
import torch
from huggingface_hub import snapshot_download
import train_qwen_ascension_lora as trainer
import evaluate_qwen_ascension_lora as evaluator

def main():
    output="checkpoints/qwen_state_contract_v8_20260901"
    if (trainer.ROOT/output).exists(): raise FileExistsError("Preserve previous candidate")
    torch.set_num_threads(4)
    base=snapshot_download("Qwen/Qwen3-0.6B",revision="c1899de289a04d12100db370d81485cdf75e47ca",local_files_only=True)
    original=trainer.training_arguments
    def bounded(**kwargs):
        kwargs.update(max_steps=60,save_strategy="steps",save_steps=10,save_total_limit=2,
                      logging_steps=1,use_cpu=True,bf16=False,fp16=False,dataloader_num_workers=0)
        return original(**kwargs)
    trainer.training_arguments=bounded
    trainer.main(["--model",base,
                  "--curriculum","evals/training/aerynza_state_precision_train_v6.jsonl",
                  "--eval-curriculum","evals/training/aerynza_state_precision_heldout_v6.jsonl",
                  "--output-dir",output,"--max-length","256","--learning-rate","0.00001"])
    return evaluator.main(["--model",base,"--adapter",output,"--tokens","128",
                           "--output","evals/results/qwen_state_contract_v8_20260901_gate.json"])
if __name__=="__main__": raise SystemExit(main())
