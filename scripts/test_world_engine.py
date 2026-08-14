"""Contract tests for Ascension-native spatial world compilation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.immersive.world_engine import compile_hub_compound, compile_world, validate_render_receipt


def test_ar_world_fails_closed_without_permissions_and_assets() -> None:
    world = compile_world("Place my dream car in the driveway of my dream home", mode="web_ar")
    assert world["render_contract"]["state"] == "prepared_not_rendered"
    assert world["ready_for_engine"] is False
    assert world["permissions"]["missing"] == ["camera.read_session", "spatial_map.local"]
    assert {item["role"] for item in world["entities"]} == {"room_shell", "aspiration_vehicle"}
    assert all(item["asset"]["state"] == "required" for item in world["entities"])


def test_supplied_assets_keep_provenance_and_do_not_become_verified() -> None:
    world = compile_world(
        "Show my car beside my home",
        mode="web_ar",
        permissions=["camera.read_session", "spatial_map.local"],
        user_assets=[
            {"role": "room_shell", "asset_id": "home-1", "source": "user_vault", "license": "user_owned", "checksum": "abc"},
            {"role": "aspiration_vehicle", "asset_id": "car-1", "source": "user_vault", "license": "user_owned", "checksum": "def"},
        ],
    )
    assert world["ready_for_engine"] is True
    assert all(item["asset"]["state"] == "supplied_unverified" for item in world["entities"])


def test_render_claim_requires_exact_engine_receipt() -> None:
    world = compile_world("A calm meditation room")
    bad = validate_render_receipt(world, {"world_id": world["world_id"]})
    assert bad["rendered"] is False
    receipt = {
        "world_id": world["world_id"],
        "engine": world["target"],
        "build_id": "build-1",
        "artifact_uri": "local://artifact/world.glb",
        "rendered_at": "2026-08-14T01:00:00Z",
        "manifest_sha256": world["manifest_sha256"],
        "validation_passed": True,
    }
    assert validate_render_receipt(world, receipt)["rendered"] is True


def test_family_compound_keeps_lifeos_and_household_context_private() -> None:
    compound = compile_hub_compound(
        family_id="family-1",
        neighborhood_id="neighborhood-1",
        members=[
            {"display_name": "Avery", "account_id": "user-1", "compound_presence_allowed": True, "profile_link_allowed": False},
            {"display_name": "Ancestor Without Account"},
        ],
        households=[{"household_id": "home-1", "label": "North House"}],
    )
    assert compound["privacy"]["lifeos_profiles_copied"] is False
    assert compound["privacy"]["private_household_context_copied"] is False
    assert compound["members"][0]["presence"] == "eligible"
    assert compound["members"][0]["profile_link"] is None
    assert compound["members"][1]["historical_tree_node"] is True
    assert compound["members"][1]["presence"] == "not_present"
    assert compound["neighborhood_contract"]["state"] == "prepared_not_joined"
    assert compound["neighborhood_contract"]["compound_interior_visible_to_neighbors"] is False


def test_compound_assets_require_rights_and_share_receipts() -> None:
    compound = compile_hub_compound(
        family_id="family-2",
        members=[],
        shared_assets=[{"asset_id": "home-model", "checksum": "abc", "license": "family_owned"}],
    )
    assert compound["ready_for_engine"] is False
    assert compound["shared_assets"][0]["usable"] is False


def main() -> None:
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("All spatial world-engine contracts passed.")


if __name__ == "__main__":
    main()
