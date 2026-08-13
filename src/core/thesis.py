"""Privacy-bounded Human, Home, and Family thesis contracts.

A thesis is an inspectable, correctable synthesis of permissioned evidence. It
is never a diagnosis, destiny claim, hidden profile, or permission to execute.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Literal


ThesisScope = Literal["human", "sprout", "home", "family", "product"]

HUMAN_SECTIONS = (
    "profile", "preferences", "identity", "goals", "aspirations", "schedule",
    "finance", "health", "relationships", "resources", "constraints",
    "strengths", "patterns", "corrections", "verified_evidence",
)
SPROUT_SECTIONS = (
    "child_profile", "child_voice", "interests", "strengths", "growth_goals",
    "learning", "development", "wellbeing", "routines", "relationships",
    "responsibilities", "chores", "allowance", "safety", "support",
    "corrections", "verified_evidence",
)
HOME_SECTIONS = {
    "household_identity", "members", "rhythms", "responsibilities", "agreements",
    "calendar", "resources", "needs", "goals", "support", "tensions", "risks",
}
FAMILY_SECTIONS = {
    "family_identity", "legacy", "members", "branches", "roles", "governance",
    "trust", "economy", "enterprises", "resources", "support", "education",
    "goals", "opportunities", "risks", "agreements",
}
PRODUCT_SECTIONS = {
    "adoption", "activation", "retention", "engagement", "outcomes", "reliability",
    "accessibility", "trust", "market", "partnerships", "funding", "research",
    "product_direction", "company_strategy", "risks", "opportunities",
}
PROHIBITED_PRODUCT_KEYS = {
    "user", "user_id", "member_id", "child_id", "name", "preferred_name", "email",
    "phone", "address", "location", "latitude", "longitude", "ip", "device_id",
    "conversation", "message", "journal", "human_thesis", "sprout_thesis", "memory",
    "account", "transaction", "health_record", "calendar_event",
}


def _bounded(value: Any) -> Any:
    if isinstance(value, str):
        return value[:1000]
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return [_bounded(item) for item in value[:20]]
    if isinstance(value, dict):
        return {str(key)[:80]: _bounded(item) for key, item in list(value.items())[:30]}
    return str(value)[:1000]


def _claim(*, section: str, key: str, value: Any, source: str, confidence: float, visibility: str, contributor_id: str | None = None) -> dict:
    bounded_value = _bounded(value)
    claim_fingerprint = json.dumps(
        {"section": section, "key": key, "value": bounded_value, "source": source, "contributor_id": contributor_id},
        sort_keys=True,
        default=str,
    )
    return {
        "claim_id": hashlib.sha256(claim_fingerprint.encode("utf-8")).hexdigest()[:20],
        "section": section,
        "key": key,
        "value": bounded_value,
        "source": source,
        "confidence": round(max(0.0, min(float(confidence), 1.0)), 3),
        "visibility": visibility,
        "contributor_id": contributor_id,
        "status": "evidence" if confidence >= 0.9 else "working_hypothesis",
    }


def _context_claims(context: dict, section: str, visibility: str) -> list[dict]:
    value = context.get(section)
    if value is None:
        return []
    if isinstance(value, dict):
        rows = list(value.items())
    elif isinstance(value, list):
        rows = [(str(index), item) for index, item in enumerate(value)]
    else:
        rows = [(section, value)]
    claims = []
    for key, item in rows[:30]:
        confidence = 0.95 if section in {"profile", "schedule", "verified_evidence", "corrections"} else 0.8
        if isinstance(item, dict) and "confidence" in item:
            confidence = float(item.get("confidence") or 0.0)
        claims.append(_claim(
            section=section,
            key=str(key),
            value=item,
            source=f"permission_scoped_context.{section}",
            confidence=confidence,
            visibility=visibility,
        ))
    return claims


def _shared_fact_claims(context: dict, key: str, allowed_sections: set[str], visibility: str) -> list[dict]:
    facts = context.get(key, [])
    if isinstance(facts, dict):
        facts = [facts]
    claims = []
    for index, fact in enumerate(facts[:100] if isinstance(facts, list) else []):
        if not isinstance(fact, dict):
            continue
        section = str(fact.get("section") or "agreements")
        if section not in allowed_sections:
            continue
        claims.append(_claim(
            section=section,
            key=str(fact.get("key") or f"shared_fact_{index}"),
            value=fact.get("value"),
            source=str(fact.get("source") or key),
            confidence=float(fact.get("confidence", 0.85)),
            visibility=visibility,
            contributor_id=str(fact.get("contributor_id")) if fact.get("contributor_id") else None,
        ))
    return claims


def _member_contributions(context: dict, required_scope: str, allowed_sections: set[str]) -> tuple[list[dict], list[str], list[dict]]:
    rows = context.get("member_thesis_contributions", [])
    if not isinstance(rows, list):
        return [], [], []
    claims, contributors, rejected = [], [], []
    for index, contribution in enumerate(rows[:200]):
        if not isinstance(contribution, dict):
            rejected.append({"index": index, "reason": "invalid_contribution"})
            continue
        member_id = str(contribution.get("member_id") or "").strip()
        scopes = contribution.get("consent_scopes", [])
        if isinstance(scopes, str):
            scopes = [scopes]
        if not member_id or required_scope not in scopes:
            rejected.append({"index": index, "member_id": member_id or None, "reason": "missing_scope_consent"})
            continue
        accepted_for_member = 0
        for claim_index, item in enumerate(contribution.get("claims", [])[:50]):
            if not isinstance(item, dict):
                continue
            section = str(item.get("section") or "")
            if section not in allowed_sections or item.get("share_scope") != required_scope:
                rejected.append({"index": index, "claim_index": claim_index, "member_id": member_id, "reason": "claim_scope_rejected"})
                continue
            claims.append(_claim(
                section=section,
                key=str(item.get("key") or f"member_claim_{claim_index}"),
                value=item.get("value"),
                source=str(item.get("source") or "member_ap_contribution"),
                confidence=float(item.get("confidence", 0.8)),
                visibility=required_scope,
                contributor_id=member_id,
            ))
            accepted_for_member += 1
        if accepted_for_member:
            contributors.append(member_id)
    return claims, list(dict.fromkeys(contributors)), rejected


def _contradictions(claims: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = {}
    for claim in claims:
        grouped.setdefault((claim["section"], claim["key"]), []).append(claim)
    conflicts = []
    for (section, key), rows in grouped.items():
        values = {json.dumps(row["value"], sort_keys=True, default=str) for row in rows}
        if len(values) > 1:
            conflicts.append({
                "section": section,
                "key": key,
                "status": "unresolved",
                "sources": [row["source"] for row in rows],
                "contributor_ids": [row["contributor_id"] for row in rows if row.get("contributor_id")],
            })
    return conflicts


def _finalize(scope: ThesisScope, subject_id: str, claims: list[dict], contributors: list[str], rejected: list[dict], expected_sections: set[str] | tuple[str, ...]) -> dict:
    section_names = sorted({claim["section"] for claim in claims})
    unknowns = sorted(set(expected_sections) - set(section_names))
    digest_source = json.dumps({"scope": scope, "subject_id": subject_id, "claims": claims}, sort_keys=True, default=str)
    return {
        "thesis_id": hashlib.sha256(digest_source.encode("utf-8")).hexdigest()[:24],
        "schema_version": "1.0",
        "scope": scope,
        "subject_id": subject_id,
        "claims": claims,
        "sections_present": section_names,
        "unknowns": unknowns,
        "contradictions": _contradictions(claims),
        "contributors": contributors,
        "rejected_contributions": rejected,
        "confidence": round(sum(claim["confidence"] for claim in claims) / len(claims), 3) if claims else 0.0,
        "status": "working_thesis",
        "persistence": "calling_shell_reviews_and_persists_after_user_visible_receipt",
        "correction_right": "authorized people can inspect, correct, revoke, or rescope contributed claims",
        "execution_authority": "none",
        "not_diagnosis_or_destiny": True,
    }


def _coverage(context: dict, contributors: list[str]) -> dict:
    expected = context.get("expected_member_ids", [])
    if not isinstance(expected, list):
        expected = []
    expected_ids = list(dict.fromkeys(str(item).strip() for item in expected if str(item).strip()))[:500]
    contributor_ids = list(dict.fromkeys(contributors))
    missing = [member_id for member_id in expected_ids if member_id not in contributor_ids]
    return {
        "expected_member_ids": expected_ids,
        "contributing_member_ids": contributor_ids,
        "missing_member_ids": missing,
        "contributing_members": len(contributor_ids),
        "expected_members": len(expected_ids),
        "complete": bool(expected_ids) and not missing,
        "status": "complete" if expected_ids and not missing else "partial",
    }


def build_human_thesis(subject_id: str, context: dict) -> dict:
    claims = []
    for section in HUMAN_SECTIONS:
        claims.extend(_context_claims(context, section, "private_ap"))
    thesis = _finalize("human", subject_id, claims, [subject_id], [], HUMAN_SECTIONS)
    thesis["owner"] = subject_id
    thesis["privacy_boundary"] = "private_to_the_user_and_their_authorized_AP_shell"
    return thesis


def build_sprout_thesis(subject_id: str, context: dict) -> dict:
    consent_receipt_id = str(context.get("guardian_consent_receipt_id") or "").strip()
    guardian_ids = context.get("guardian_ids", [])
    if isinstance(guardian_ids, str):
        guardian_ids = [guardian_ids]
    guardian_ids = list(dict.fromkeys(str(item).strip() for item in guardian_ids if str(item).strip()))[:20]
    if not consent_receipt_id or not guardian_ids:
        raise ValueError("Sprout thesis creation requires an authorized guardian and consent receipt")

    claims = []
    for section in SPROUT_SECTIONS:
        claims.extend(_context_claims(context, section, "sprout_private"))
    thesis = _finalize("sprout", subject_id, claims, [subject_id], [], SPROUT_SECTIONS)
    age = context.get("age")
    try:
        numeric_age = int(age) if age is not None else None
    except (TypeError, ValueError):
        numeric_age = None
    thesis.update({
        "owner": subject_id,
        "authorized_guardian_ids": guardian_ids,
        "guardian_consent_receipt_id": consent_receipt_id,
        "experience_mode": "teen" if numeric_age is not None and numeric_age >= 12 else "sprout",
        "continuity_rule": "the thesis continues across Sprout-to-Teen presentation changes without freezing the child's identity",
        "privacy_boundary": "child-centered Sprout evidence only; adult finance, dating, household, and FamilyOS theses are excluded",
        "child_voice_right": "the child can view and correct age-appropriate claims; the guardian shell validates persistence and safety boundaries",
        "development_boundary": "developmental support is not diagnosis, labeling, destiny, or a substitute for qualified care",
    })
    return thesis


def build_member_thesis_contribution(
    member_id: str,
    target_scope: Literal["nexus_home", "nexus_family"],
    human_thesis: dict,
    selections: list[dict],
    consent_receipt_id: str,
) -> dict:
    """Export exact user-selected Human Thesis claims to a Nexus scope.

    The contribution contains no raw Human Thesis packet. Destination sections
    are explicit because a private AP concept may have a different shared-home
    or family meaning.
    """
    allowed_sections = HOME_SECTIONS if target_scope == "nexus_home" else FAMILY_SECTIONS
    if human_thesis.get("scope") != "human" or human_thesis.get("owner") != member_id:
        raise ValueError("the Human Thesis must belong to the contributing member")
    if not str(consent_receipt_id).strip():
        raise ValueError("an explicit consent receipt is required")

    private_claims = {
        str(item.get("claim_id")): item
        for item in human_thesis.get("claims", [])
        if isinstance(item, dict) and item.get("claim_id")
    }
    exported, rejected = [], []
    for index, selection in enumerate(selections[:100] if isinstance(selections, list) else []):
        if not isinstance(selection, dict):
            rejected.append({"index": index, "reason": "invalid_selection"})
            continue
        claim_id = str(selection.get("claim_id") or "")
        destination = str(selection.get("destination_section") or "")
        source_claim = private_claims.get(claim_id)
        if source_claim is None:
            rejected.append({"index": index, "claim_id": claim_id or None, "reason": "claim_not_found"})
            continue
        if destination not in allowed_sections:
            rejected.append({"index": index, "claim_id": claim_id, "reason": "destination_not_allowed"})
            continue
        exported.append({
            "section": destination,
            "key": str(selection.get("shared_key") or source_claim.get("key") or claim_id),
            "value": _bounded(source_claim.get("value")),
            "confidence": float(source_claim.get("confidence", 0.0)),
            "share_scope": target_scope,
            "source": f"human_thesis:{human_thesis.get('thesis_id')}:{claim_id}",
        })
    return {
        "member_id": member_id,
        "consent_scopes": [target_scope],
        "consent_receipt_id": str(consent_receipt_id),
        "source_thesis_id": human_thesis.get("thesis_id"),
        "claims": exported,
        "rejected_selections": rejected,
        "revocable": True,
        "persistence": "calling_shell_persists_only_after_validating_the_consent_receipt",
    }


def build_home_thesis(subject_id: str, context: dict) -> dict:
    facts = _shared_fact_claims(context, "home_shared_facts", HOME_SECTIONS, "nexus_home")
    contributions, contributors, rejected = _member_contributions(context, "nexus_home", HOME_SECTIONS)
    thesis = _finalize("home", subject_id, facts + contributions, contributors, rejected, HOME_SECTIONS)
    thesis["owner"] = "authorized_household_members"
    thesis["privacy_boundary"] = "shared_household_claims_only; private AP and FamilyOS data are excluded"
    thesis["member_coverage"] = _coverage(context, contributors)
    return thesis


def build_family_thesis(subject_id: str, context: dict) -> dict:
    facts = _shared_fact_claims(context, "family_shared_facts", FAMILY_SECTIONS, "nexus_family")
    contributions, contributors, rejected = _member_contributions(context, "nexus_family", FAMILY_SECTIONS)
    thesis = _finalize("family", subject_id, facts + contributions, contributors, rejected, FAMILY_SECTIONS)
    thesis["owner"] = "authorized_family_governance"
    thesis["privacy_boundary"] = "consented AP contribution claims and FamilyOS shared facts only; private LifeOS and NexusHome data are excluded"
    thesis["comprehensiveness_rule"] = "expand breadth through consented member contributions, named historical branches, shared evidence, and explicit unknowns—not private-data inference"
    thesis["member_coverage"] = _coverage(context, contributors)
    thesis["comprehensive"] = (
        thesis["member_coverage"]["complete"]
        and not thesis["unknowns"]
        and not thesis["contradictions"]
    )
    return thesis


def _contains_prohibited_product_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).strip().lower()
            if normalized in PROHIBITED_PRODUCT_KEYS or any(token in normalized for token in ("email", "phone", "address", "user_id", "member_id", "child_id", "conversation", "message")):
                return True
            if _contains_prohibited_product_key(item):
                return True
    elif isinstance(value, list):
        return any(_contains_prohibited_product_key(item) for item in value)
    return False


def build_product_thesis(subject_id: str, context: dict) -> dict:
    """Build founder strategy from aggregates and public evidence only."""
    minimum_cohort = max(20, int(context.get("minimum_cohort_size", 20) or 20))
    claims, rejected = [], []
    metrics = context.get("aggregate_metrics", [])
    if not isinstance(metrics, list):
        metrics = []
    for index, metric in enumerate(metrics[:500]):
        if not isinstance(metric, dict) or _contains_prohibited_product_key(metric):
            rejected.append({"index": index, "source": "aggregate_metrics", "reason": "personal_or_row_level_field_rejected"})
            continue
        cohort_size = int(metric.get("cohort_size", 0) or 0)
        section = str(metric.get("section") or "product_direction")
        value = metric.get("value")
        if cohort_size < minimum_cohort:
            rejected.append({"index": index, "source": "aggregate_metrics", "reason": "cohort_below_privacy_threshold"})
            continue
        if section not in PRODUCT_SECTIONS or not isinstance(value, (int, float, bool)):
            rejected.append({"index": index, "source": "aggregate_metrics", "reason": "invalid_aggregate_metric"})
            continue
        claims.append(_claim(
            section=section,
            key=str(metric.get("key") or f"aggregate_{index}"),
            value={"value": value, "cohort_size": cohort_size, "period": _bounded(metric.get("period"))},
            source=str(metric.get("source") or "privacy_thresholded_product_analytics"),
            confidence=float(metric.get("confidence", 0.9)),
            visibility="founder_strategy",
        ))

    public_rows = context.get("public_evidence", [])
    if not isinstance(public_rows, list):
        public_rows = []
    for index, item in enumerate(public_rows[:200]):
        if not isinstance(item, dict) or _contains_prohibited_product_key(item):
            rejected.append({"index": index, "source": "public_evidence", "reason": "invalid_or_personal_field_rejected"})
            continue
        section = str(item.get("section") or "market")
        if section not in PRODUCT_SECTIONS or not item.get("source_url"):
            rejected.append({"index": index, "source": "public_evidence", "reason": "unverifiable_public_evidence"})
            continue
        claims.append(_claim(
            section=section,
            key=str(item.get("key") or item.get("title") or f"public_{index}"),
            value={"finding": _bounded(item.get("finding")), "source_url": _bounded(item.get("source_url")), "published_at": _bounded(item.get("published_at"))},
            source="public_evidence",
            confidence=float(item.get("confidence", 0.75)),
            visibility="founder_strategy",
        ))

    thesis = _finalize("product", subject_id, claims, [], rejected, PRODUCT_SECTIONS)
    thesis.update({
        "owner": "The B.E.I.N.G Group LLC authorized founder controls",
        "privacy_boundary": "privacy-thresholded aggregate analytics and cited public evidence only; no personal thesis, raw conversation, user row, or identifiable small cohort",
        "minimum_cohort_size": minimum_cohort,
        "silent_operation_rule": "may compute in the background only when aggregate analytics use is disclosed; material product or company decisions remain human-reviewed",
        "allowed_uses": ["product improvement", "partnership discovery", "market research", "funding strategy", "research priorities", "company planning"],
        "prohibited_uses": ["individual profiling", "vulnerability targeting", "reidentification", "personalized pricing", "silent policy changes", "automated consequential decisions"],
        "founder_review_required": True,
    })
    return thesis


def build_thesis(scope: ThesisScope, subject_id: str, context: dict) -> dict:
    if scope == "human":
        return build_human_thesis(subject_id, context)
    if scope == "sprout":
        return build_sprout_thesis(subject_id, context)
    if scope == "home":
        return build_home_thesis(subject_id, context)
    if scope == "family":
        return build_family_thesis(subject_id, context)
    if scope == "product":
        return build_product_thesis(subject_id, context)
    raise ValueError(f"unsupported thesis scope: {scope}")
