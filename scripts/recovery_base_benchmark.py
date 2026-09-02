"""Bounded CPU baseline only: download public weights, never train or promote."""
import json
import time
from pathlib import Path


def main():
    import torch
    from huggingface_hub import HfApi
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from evaluate_native_checkpoint import DEFAULT_PROMPTS, evaluate_response
    output = Path(__file__).resolve().parents[1] / "evals/results/qwen_recovery_baseline_20260831.json"
    if output.exists():
        raise FileExistsError("Preserve existing baseline; choose a new run explicitly")
    model_id = "Qwen/Qwen3-0.6B"
    revision = HfApi().model_info(model_id).sha
    print(f"Loading {model_id} pinned at {revision}", flush=True)
    torch.set_num_threads(4)
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(model_id, revision=revision, trust_remote_code=False, torch_dtype=torch.float32)
    model.eval()
    results = []
    for prompt in DEFAULT_PROMPTS:
        inputs = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], enable_thinking=False,
                    add_generation_prompt=True, return_tensors="pt", return_dict=True)
        start = time.monotonic()
        torch.manual_seed(3407)
        with torch.inference_mode():
            generated = model.generate(**inputs, max_new_tokens=96, do_sample=True, temperature=0.7, top_p=0.8, top_k=20,
                                       pad_token_id=tokenizer.eos_token_id)
        answer = tokenizer.decode(generated[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
        results.append({**evaluate_response(prompt, answer), "seconds": round(time.monotonic()-start, 2)})
        print(f"Completed {len(results)}/{len(DEFAULT_PROMPTS)}", flush=True)
    output.write_text(json.dumps({"base_model": model_id, "revision": revision, "samples": results,
        "human_review_required": True, "production_replacement_ready": False, "training_started": False}, indent=2), encoding="utf-8")
    print(str(output), flush=True)


if __name__ == "__main__":
    main()
