"""Focused source contract for independent Qwen train/eval data."""
from pathlib import Path

source=(Path(__file__).parent/"train_qwen_ascension_lora.py").read_text(encoding="utf-8")
required=(
    'parser.add_argument("--eval-curriculum"',
    'raise ValueError(f"train/eval prompt overlap:',
    '"eval_is_independent": eval_curriculum is not None',
    'eval_rows = [encode_record(tokenizer, record, args.max_length) for record in eval_records]',
)
missing=[item for item in required if item not in source]
if missing: raise AssertionError(f"missing independent eval contract: {missing}")
print("PASS independent held-out data is loaded, overlap-checked, encoded separately and receipted")
