import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.train_qwen_ascension_lora import balanced_group_weights


def main() -> None:
    groups = ["shell:ap"] * 100 + ["shell:sprout"] * 10 + ["conversation:ap"] * 5
    weights = balanced_group_weights(groups)
    mass = defaultdict(float)
    for group, weight in zip(groups, weights):
        mass[group] += weight
    assert set(round(value, 8) for value in mass.values()) == {1.0}
    print("v20 package+shell sampler test passed")


if __name__ == "__main__":
    main()
