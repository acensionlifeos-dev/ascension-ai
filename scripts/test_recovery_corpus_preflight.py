import json
import tempfile
from pathlib import Path
from recovery_corpus_preflight import validate


def main():
    with tempfile.TemporaryDirectory() as directory:
        train, heldout = Path(directory) / "train.jsonl", Path(directory) / "heldout.jsonl"
        def write(path, prefix):
            path.write_text("\n".join(json.dumps({"user": f"{prefix} question {i}", "assistant": "A useful answer."}) for i in range(20)), encoding="utf-8")
        write(train, "train")
        write(heldout, "heldout")
        assert validate(train, heldout)["human_review_required"]
        for bad in (heldout.read_text(), "# internal documentation", json.dumps({"user": "test", "assistant": ""})):
            train.write_text(bad, encoding="utf-8")
            try:
                validate(train, heldout)
            except (ValueError, json.JSONDecodeError):
                pass
            else:
                raise AssertionError("Bad corpus accepted")
    print("PASS valid format, overlap, documentation, and incomplete corpus checks")


if __name__ == "__main__":
    main()
