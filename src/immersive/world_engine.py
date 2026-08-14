"""Ascension-native spatial world planning and render-receipt contracts.

The intelligence core compiles a permission-scoped request into a portable scene
manifest. A real engine adapter owns mesh generation, simulation, rendering,
device permissions, and receipts. No hosted model is required or implied.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any


SCHEMA_VERSION = "ascension.spatial.world.v1"
ENGINE_TARGETS = {
    "webxr_threejs": {"formats": ["glb", "gltf"], "modes": ["web_ar", "web_vr", "3d"]},
    "openxr": {"formats": ["glb", "gltf", "usd"], "modes": ["vr", "mixed_reality"]},
    "arkit_realitykit": {"formats": ["usdz", "reality"], "modes": ["ar", "mixed_reality"]},
    "arcore_sceneview": {"formats": ["glb", "gltf"], "modes": ["ar", "mixed_reality"]},
}

_OBJECT_RULES = (
    (r"\b(?:home|house|room|bedroom|kitchen)\b", "architecture", "room_shell"),
    (r"\b(?:car|vehicle)\b", "vehicle", "aspiration_vehicle"),
    (r"\b(?:watch|jewelry|display)\b", "display", "aspiration_display"),
    (r"\b(?:desk|chair|sofa|bed|table)\b", "furniture", "furniture"),
    (r"\b(?:coach|companion|avatar|person)\b", "character", "assistant_avatar"),
)


def _stable_id(prefix: str, value: str) -> str:
    return f"{prefix}_{hashlib.sha256(value.encode('utf-8')).hexdigest()[:12]}"


def _entities(prompt: str) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    for pattern, category, role in _OBJECT_RULES:
        match = re.search(pattern, prompt, re.I)
        if not match:
            continue
        label = match.group(0).lower()
        entities.append({
            "id": _stable_id("entity", f"{role}:{label}"),
            "label": label,
            "category": category,
            "role": role,
            "transform": {"position_m": [0.0, 0.0, -2.0 - len(entities)], "rotation_deg": [0, 0, 0], "scale": [1, 1, 1]},
            "asset": {"state": "required", "asset_id": None, "source": None, "license": None, "checksum": None},
            "interaction": {"selectable": True, "grabbable": category not in {"architecture"}, "collision": True},
        })
    if not entities:
        entities.append({
            "id": _stable_id("entity", "environment_shell"),
            "label": "environment",
            "category": "environment",
            "role": "world_shell",
            "transform": {"position_m": [0, 0, 0], "rotation_deg": [0, 0, 0], "scale": [1, 1, 1]},
            "asset": {"state": "required", "asset_id": None, "source": None, "license": None, "checksum": None},
            "interaction": {"selectable": False, "grabbable": False, "collision": True},
        })
    return entities


def compile_world(
    prompt: str,
    *,
    mode: str = "3d",
    target: str = "webxr_threejs",
    user_assets: list[dict[str, Any]] | None = None,
    permissions: list[str] | None = None,
) -> dict[str, Any]:
    """Compile an engine-neutral world manifest without claiming it was rendered."""
    prompt = str(prompt or "").strip()
    if not prompt:
        raise ValueError("A world description is required")
    if target not in ENGINE_TARGETS:
        raise ValueError(f"Unsupported engine target: {target}")
    if mode not in ENGINE_TARGETS[target]["modes"]:
        raise ValueError(f"Mode {mode!r} is not supported by {target}")

    granted = set(permissions or [])
    required_permissions = []
    if mode in {"ar", "web_ar", "mixed_reality"}:
        required_permissions.extend(["camera.read_session", "spatial_map.local"])
    permission_gaps = sorted(set(required_permissions) - granted)
    entities = _entities(prompt)
    supplied_assets = {str(a.get("role")): a for a in (user_assets or []) if isinstance(a, dict)}
    for entity in entities:
        asset = supplied_assets.get(entity["role"])
        if asset:
            entity["asset"] = {
                "state": "supplied_unverified",
                "asset_id": asset.get("asset_id"),
                "source": asset.get("source"),
                "license": asset.get("license"),
                "checksum": asset.get("checksum"),
            }

    world_id = _stable_id("world", json.dumps([prompt, mode, target], separators=(",", ":")))
    manifest: dict[str, Any] = {
        "schema": SCHEMA_VERSION,
        "world_id": world_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "mode": mode,
        "target": target,
        "coordinate_system": {"handedness": "right", "up_axis": "y", "unit": "meter"},
        "entities": entities,
        "environment": {"sky": "procedural", "lighting": "physically_based", "gravity_m_s2": -9.81},
        "spatial": {"anchors": [], "plane_detection": mode in {"ar", "web_ar", "mixed_reality"}, "occlusion": True},
        "performance_budget": {"minimum_fps": 60 if mode in {"ar", "web_ar"} else 72, "max_draw_calls": 250, "max_visible_triangles": 1_000_000, "lod_required": True},
        "accessibility": {"seated_mode": True, "reduced_motion": True, "captions": True, "high_contrast_ui": True, "locomotion": ["teleport", "smooth"]},
        "safety": {"comfort_vignette": True, "guardian_boundary_required": False, "bystander_identification": False, "physical_boundary_required": mode != "3d"},
        "permissions": {"required": required_permissions, "granted": sorted(granted), "missing": permission_gaps, "camera_retention": "none_by_default"},
        "render_contract": {
            "state": "prepared_not_rendered",
            "engine_target": target,
            "accepted_asset_formats": ENGINE_TARGETS[target]["formats"],
            "required_receipt_fields": ["world_id", "engine", "build_id", "artifact_uri", "rendered_at", "manifest_sha256", "validation_passed"],
        },
    }
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    manifest["manifest_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    manifest["ready_for_engine"] = not permission_gaps and all(e["asset"]["state"] != "required" for e in entities)
    return manifest


def compile_hub_compound(
    *,
    family_id: str,
    members: list[dict[str, Any]],
    households: list[dict[str, Any]] | None = None,
    neighborhood_id: str | None = None,
    shared_assets: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compile a privacy-partitioned Hub compound without copying LifeOS profiles.

    Inputs must already be permission scoped by FamilyOS. Named family-tree nodes
    may exist without an OS account, but never gain a private profile or presence.
    """
    if not str(family_id or "").strip():
        raise ValueError("family_id is required")
    member_nodes = []
    for raw in members:
        if not isinstance(raw, dict) or not raw.get("display_name"):
            continue
        account_id = raw.get("account_id")
        member_nodes.append({
            "member_ref": _stable_id("member", f"{family_id}:{raw['display_name']}:{account_id or 'historical'}"),
            "display_name": str(raw["display_name"])[:80],
            "role": raw.get("family_role", "member"),
            "presence": "eligible" if account_id and raw.get("compound_presence_allowed") is True else "not_present",
            "profile_link": account_id if account_id and raw.get("profile_link_allowed") is True else None,
            "private_lifeos_context": "not_included",
            "historical_tree_node": account_id is None,
        })

    household_nodes = []
    for index, raw in enumerate(households or []):
        if not isinstance(raw, dict):
            continue
        household_nodes.append({
            "household_ref": _stable_id("home", f"{family_id}:{raw.get('household_id', index)}"),
            "label": str(raw.get("label") or f"Household {index + 1}")[:80],
            "parcel": index,
            "nexus_authority": "nexus_home",
            "family_visibility": raw.get("family_visibility", "presence_only"),
            "private_home_context": "not_included",
            "coparenting_spaces": list(raw.get("coparenting_spaces") or [])[:8],
        })

    compound_id = _stable_id("compound", family_id)
    manifest = {
        "schema": "ascension.spatial.compound.v1",
        "compound_id": compound_id,
        "family_id": family_id,
        "neighborhood_id": neighborhood_id,
        "zones": [
            {"id": "family_commons", "authority": "nexus_family", "visibility": "family_members", "features": ["family_chat", "calendar", "family_tree", "shared_resources"]},
            {"id": "enterprise_hall", "authority": "nexus_family", "visibility": "role_scoped", "features": ["funding_requests", "business_ideas", "family_economy"]},
            {"id": "legacy_gallery", "authority": "nexus_family", "visibility": "family_members", "features": ["historical_tree", "permissioned_stories"]},
        ],
        "members": member_nodes,
        "households": household_nodes,
        "shared_assets": [
            {
                "asset_id": item.get("asset_id"),
                "source": item.get("source"),
                "license": item.get("license"),
                "checksum": item.get("checksum"),
                "share_receipt": item.get("share_receipt"),
                "usable": bool(item.get("checksum") and item.get("license") and item.get("share_receipt")),
            }
            for item in (shared_assets or []) if isinstance(item, dict)
        ],
        "privacy": {
            "individual_authority": "ap",
            "household_authority": "nexus_home",
            "family_authority": "nexus_family",
            "cross_family_authority": "none",
            "lifeos_profiles_copied": False,
            "private_household_context_copied": False,
            "shared_fields_require_purpose_audience_duration_and_receipt": True,
        },
        "neighborhood_contract": {
            "state": "unlinked" if not neighborhood_id else "prepared_not_joined",
            "public_facade_allowed": True,
            "compound_interior_visible_to_neighbors": False,
            "shared_event_requires_family_approval": True,
            "required_join_receipt": ["compound_id", "neighborhood_id", "approved_by", "joined_at", "scope"],
        },
        "render_contract": {
            "state": "prepared_not_rendered",
            "engine_target": "webxr_threejs",
            "required_receipt_fields": ["compound_id", "engine", "build_id", "artifact_uri", "rendered_at", "manifest_sha256", "validation_passed"],
        },
    }
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    manifest["manifest_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    manifest["ready_for_engine"] = all(asset["usable"] for asset in manifest["shared_assets"])
    return manifest


def validate_render_receipt(manifest: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    """Verify that a real engine receipt belongs to this exact manifest."""
    required = set(manifest.get("render_contract", {}).get("required_receipt_fields", []))
    missing = sorted(field for field in required if receipt.get(field) in {None, ""})
    failures = []
    if missing:
        failures.append(f"missing receipt fields: {', '.join(missing)}")
    manifest_object_id = manifest.get("world_id") or manifest.get("compound_id")
    receipt_object_id = receipt.get("world_id") or receipt.get("compound_id")
    if receipt_object_id != manifest_object_id:
        failures.append("world or compound id mismatch")
    if receipt.get("manifest_sha256") != manifest.get("manifest_sha256"):
        failures.append("manifest checksum mismatch")
    if receipt.get("engine") != manifest.get("target"):
        failures.append("engine target mismatch")
    if receipt.get("validation_passed") is not True:
        failures.append("engine validation did not pass")
    return {"rendered": not failures, "failures": failures, "receipt": receipt if not failures else None}
