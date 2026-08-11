"""Download and verify the pinned local model selected for this deployment."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from huggingface_hub import hf_hub_download


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "config" / "model_profiles.json"
MODELS_DIR = ROOT / "models"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    profiles = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    name = os.getenv("ASCENSION_MODEL_PROFILE", "starter").strip().lower()
    if name not in profiles:
        raise SystemExit(f"Unknown ASCENSION_MODEL_PROFILE: {name}")
    profile = profiles[name]
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = Path(hf_hub_download(
        repo_id=profile["repo_id"],
        filename=profile["filename"],
        revision=profile["revision"],
        local_dir=MODELS_DIR,
    ))
    actual = sha256(downloaded)
    if actual != profile["sha256"]:
        downloaded.unlink(missing_ok=True)
        raise SystemExit("Downloaded model checksum did not match the pinned manifest.")
    print(json.dumps({
        "status": "verified",
        "profile": name,
        "model": profile["label"],
        "path": str(downloaded.relative_to(ROOT)),
        "size_bytes": downloaded.stat().st_size,
    }))


if __name__ == "__main__":
    main()
