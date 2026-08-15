"""Create a GitHub release and upload the v16 GGUF artifact."""
from __future__ import annotations

import http.client
import json
import os
import ssl
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN = os.environ.get("GH_TOKEN", "").strip()
REPO = "acensionlifeos-dev/ascension-ai"
TAG = "v16-merged-70-30"
FILE = ROOT / "models" / "v16_merged_70_30.gguf"


def create_release() -> str:
    if not TOKEN:
        raise SystemExit("GH_TOKEN required")
    body = json.dumps({
        "tag_name": TAG,
        "name": "v16 merged 70/30 GGUF",
        "body": "Qwen3-1.7B full-model merge 70% proven_parent + 30% v6b converted to Q8_0 GGUF.",
    })
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request(
        "POST", f"/repos/{REPO}/releases", body=body.encode(),
        headers={
            "Authorization": f"token {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "ascension-ai",
        },
    )
    resp = conn.getresponse()
    data = json.loads(resp.read().decode("utf-8"))
    if resp.status not in (201, 422):
        raise SystemExit(f"Release creation failed: {resp.status} {data}")
    if resp.status == 422 and "already_exists" in str(data):
        # Fetch existing release
        conn.request(
            "GET", f"/repos/{REPO}/releases/tags/{TAG}",
            headers={"Authorization": f"token {TOKEN}", "User-Agent": "ascension-ai"},
        )
        resp = conn.getresponse()
        data = json.loads(resp.read().decode("utf-8"))
    return data["upload_url"].split("{")[0]


def upload_asset(upload_url: str) -> None:
    if not FILE.is_file():
        raise SystemExit(f"GGUF file not found: {FILE}")
    size = FILE.stat().st_size
    url = upload_url + "?name=v16_merged_70_30.gguf"
    parsed = url.split("/")[2]
    path = "/" + "/".join(url.split("/")[3:])
    conn = http.client.HTTPSConnection(parsed)
    conn.putrequest("POST", path)
    conn.putheader("Authorization", f"token {TOKEN}")
    conn.putheader("Content-Type", "application/octet-stream")
    conn.putheader("Content-Length", str(size))
    conn.putheader("User-Agent", "ascension-ai")
    conn.endheaders()
    with FILE.open("rb") as source:
        while True:
            chunk = source.read(1024 * 1024)
            if not chunk:
                break
            conn.send(chunk)
    resp = conn.getresponse()
    print(json.dumps({
        "status": resp.status,
        "reason": resp.reason,
        "headers": dict(resp.getheaders()),
    }))


def main() -> int:
    upload_url = create_release()
    print("upload_url:", upload_url)
    upload_asset(upload_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
