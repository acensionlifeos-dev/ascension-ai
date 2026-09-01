import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_v20_curriculum import PACKAGES, current_branding, deepen_capability_answer, normalize, package_for


def main() -> None:
    assert normalize("  Work   10 PM ") == "work 10 pm"
    assert current_branding("Ascension LifeOS and AP") == "AerynzaLife and Aerynza"
    old = "I can help with Aerynza Tutor. One-on-one tutoring. I won't take any action without your permission and a provider receipt. Tell me what you'd like to do first."
    assert "I can help" not in deepen_capability_answer("Help me with Aerynza Tutor.", old)
    assert package_for({"user": "I work Wed-Sun", "assistant": "Let's map the schedule."}, "x") == "l2_time_schedule"
    assert package_for({"user": "Publish the post", "assistant": "I need approval and a receipt."}, "x") == "l5_memory_receipts"
    assert package_for({"user": "Help design a game", "assistant": "Let's shape it."}, "x") == "l7_creation_multimodal"
    assert len(PACKAGES) == 8
    print("v20 curriculum builder tests passed")


if __name__ == "__main__":
    main()
