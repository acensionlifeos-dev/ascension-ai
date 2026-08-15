"""Build a public JSON report of per-capability and execution gate results."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    gates = json.loads((ROOT / "evals" / "per_capability_gates.json").read_text("utf-8"))
    per_cap = json.loads((ROOT / "evals" / "results" / "grow161_all_v6b_a_per_capability_gate.json").read_text("utf-8"))
    exec_probe = json.loads((ROOT / "evals" / "results" / "grow161_all_v6b_a_execution_probe.json").read_text("utf-8"))

    per_cap_by_id = {r["case_id"]: r for r in per_cap["results"]}
    exec_by_id = {r["case_id"]: r for r in exec_probe["results"]}

    capabilities = []
    for case in gates["cases"]:
        cap_id = case["id"]
        capabilities.append({
            "id": cap_id,
            "name": case["name"],
            "category": case["category"],
            "shell": case["shell"],
            "per_capability_passed": per_cap_by_id.get(cap_id, {}).get("passed", False),
            "execution_passed": exec_by_id.get(cap_id, {}).get("passed", False),
            "execution_score": exec_by_id.get(cap_id, {}).get("score", 0.0),
        })

    report = {
        "total": len(capabilities),
        "per_capability_ready": per_cap["passed"],
        "per_capability_rate": per_cap["pass_rate"],
        "execution_ready": exec_probe["passed"],
        "execution_rate": exec_probe["pass_rate"],
        "generated_at": json.loads(json.dumps(None, default=str)),
        "capabilities": capabilities,
    }

    (ROOT / "public" / "static" / "capability_report.json").parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "public" / "capability_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(capabilities)} capability statuses to public/capability_report.json")
    print(f"Per-capability: {report['per_capability_ready']}/{report['total']} = {report['per_capability_rate']*100:.1f}%")
    print(f"Execution: {report['execution_ready']}/{report['total']} = {report['execution_rate']*100:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
