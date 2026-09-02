"""Safety guard for the native Python endpoint.

Mirrors the TypeScript safety-guard.ts and adds content scanning for PII,
crisis, high-risk requests, and boundary violations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List


CRISIS_PATTERNS = {
    "self_harm": re.compile(
        r"\b(?:hurt myself|self[-. ]?harm|cut myself|end it all|end my life|"
        r"kill myself|suicidal|suicide|no reason to live)\b",
        re.IGNORECASE,
    ),
    "harm_to_others": re.compile(
        r"\b(?:kill them|hurt them|plan to attack|going to shoot|bomb|stab someone|murder)\b",
        re.IGNORECASE,
    ),
    "abuse": re.compile(
        r"\b(?:hitting me|hitting the kids|being abused|domestic violence|"
        r"he hurts me|she hurts me|afraid of my partner)\b",
        re.IGNORECASE,
    ),
}

PII_PATTERNS = {
    "ssn_usa": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "phone_usa": re.compile(r"\b\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
    "api_key_like": re.compile(
        r"\b(?:api[_-]?key|token|secret)\s*[:=]\s*['\"]?[a-zA-Z0-9]{16,}['\"]?",
        re.IGNORECASE,
    ),
}

SENSITIVE_TOPIC_PATTERNS = {
    "health_diagnosis_request": re.compile(
        r"\b(?:diagnose|tell me if I have|do I have (?:cancer|bipolar|ADHD|diabetes|"
        r"depression|anxiety|herpes|HIV)|am I pregnant|is this (?:herpes|bipolar|ADHD|cancer|diabetes))\b",
        re.IGNORECASE,
    ),
    "legal_advice_request": re.compile(
        r"\b(?:should I sue|can I get custody|will I go to jail|am I liable|"
        r"is this legal for me to)\b",
        re.IGNORECASE,
    ),
    "financial_guarantee_request": re.compile(
        r"\b(?:guarantee returns|guaranteed profit|risk-free investment|"
        r"make me rich fast|double my money)\b",
        re.IGNORECASE,
    ),
    "password_or_secret_request": re.compile(
        r"\b(?:give me your password|what is the admin password|send me the key|"
        r"what is the secret)\b",
        re.IGNORECASE,
    ),
    "personal_info_request": re.compile(
        r"\b(?:what is their ssn|what is their password|give me their bank|"
        r"show me their messages)\b",
        re.IGNORECASE,
    ),
}

THIRD_PARTY_PATTERN = re.compile(
    r"\b(?:my (?:wife|husband|kid|child|partner|employee|boss|business partner)).*"
    r"\b(?:password|account|ssn|bank|messages|location|search history|private)\b",
    re.IGNORECASE,
)

# This deliberately requires present-tense, personal emergency language. It must
# not intercept educational questions such as "what are the signs of a stroke?".
MEDICAL_EMERGENCY_PATTERNS = {
    "cardiac_or_breathing": re.compile(
        r"\b(?:i(?:'m| am)?|my child(?:'s)?|my baby(?:'s)?|someone here(?:'s)?)\b.{0,80}"
        r"(?:severe|crushing|sudden|new|bad)?\s*(?:chest pain|chest pressure|"
        r"can(?:not|'t) breathe|trouble breathing|short(?:ness)? of breath|having (?:a )?heart attack)\b|"
        r"\b(?:i think i(?:'m| am) having|i(?:'m| am) having) (?:a )?heart attack\b",
        re.IGNORECASE,
    ),
    "stroke": re.compile(
        r"\b(?:i think i(?:'m| am) having|i(?:'m| am) having|my .* (?:is|has)) (?:a )?stroke\b|"
        r"\b(?:my|their) face (?:is )?droop(?:ing|ed)?\b.{0,100}\b(?:arm|leg) (?:is )?(?:weak|numb)\b|"
        r"\b(?:my|their) speech (?:is )?(?:slurred|strange)\b.{0,100}\b(?:weak|numb|droop)",
        re.IGNORECASE,
    ),
    "anaphylaxis": re.compile(
        r"\b(?:my|their) (?:throat|tongue|lips?) (?:is|are)?\s*(?:swelling|swollen)\b.{0,100}"
        r"\b(?:can(?:not|'t) breathe|trouble breathing|wheez(?:e|ing))\b",
        re.IGNORECASE,
    ),
    "overdose": re.compile(
        r"\b(?:i|they|he|she) (?:overdosed|took too (?:many|much)|may have overdosed)\b",
        re.IGNORECASE,
    ),
    "severe_bleeding": re.compile(
        r"\b(?:i(?:'m| am)?|they(?:'re| are)?|he(?:'s| is)?|she(?:'s| is)?)\b.{0,60}"
        r"(?:bleeding (?:heavily|a lot|uncontrollably)|bleeding (?:that )?won(?:not|'t) stop|uncontrolled bleeding)\b",
        re.IGNORECASE,
    ),
    "pregnancy_emergency": re.compile(
        r"\b(?:i(?:'m| am) pregnant|pregnan(?:t|cy))\b.{0,120}"
        r"(?:heavy bleeding|severe (?:belly|abdominal|pelvic) pain|seizure|fainted|passed out|"
        r"can(?:not|'t) breathe|chest pain)\b",
        re.IGNORECASE,
    ),
}


def medical_emergency_response(content: str) -> str | None:
    """Return immediate, non-diagnostic escalation for current emergencies."""
    text = str(content or "").strip()
    category = next((name for name, pattern in MEDICAL_EMERGENCY_PATTERNS.items() if pattern.search(text)), None)
    if not category:
        return None
    if category == "stroke":
        return (
            "These can be signs of a stroke. Call emergency services now (911 in the U.S. and Canada) and note when the symptoms started. "
            "Do not drive yourself and do not wait to see if it improves. If you can, unlock the door and keep the phone with you."
        )
    if category == "overdose":
        return (
            "This may be an overdose emergency. Call emergency services now (911 in the U.S. and Canada). "
            "If opioid overdose is possible and naloxone is available, use it as directed. Do not leave the person alone; follow the dispatcher’s instructions."
        )
    return (
        "This could be a medical emergency. Call emergency services now (911 in the U.S. and Canada) or have someone nearby call. "
        "Do not drive yourself and do not wait for an online reply. If you can, unlock the door, keep your phone with you, and follow the dispatcher’s instructions."
    )


@dataclass
class SafetyResult:
    safe: bool = True
    level: str = "none"
    flags: List[str] = field(default_factory=list)
    action: str = "allow"
    message: str = "No safety issues detected."
    pii_detected: List[str] = field(default_factory=list)
    crisis_detected: List[str] = field(default_factory=list)
    sensitive_topics: List[str] = field(default_factory=list)


def scan_safety(content: str) -> SafetyResult:
    flags: List[str] = []
    pii: List[str] = []
    crisis: List[str] = []
    sensitive: List[str] = []

    for name, pattern in PII_PATTERNS.items():
        if pattern.search(content):
            flags.append(f"pii:{name}")
            pii.append(name)

    for category, pattern in CRISIS_PATTERNS.items():
        if pattern.search(content):
            flags.append(f"crisis:{category}")
            crisis.append(category)

    for name, pattern in SENSITIVE_TOPIC_PATTERNS.items():
        if pattern.search(content):
            flags.append(f"sensitive:{name}")
            sensitive.append(name)

    if THIRD_PARTY_PATTERN.search(content):
        flags.append("boundary:third_party_private_info")

    if crisis:
        return SafetyResult(
            safe=False,
            level="critical",
            flags=flags,
            action="escalate",
            message=(
                "This message contains signs of possible crisis or harm. I am not a crisis counselor. "
                "If you or someone else is in danger, please contact emergency services or a crisis line "
                "(988 in the US). You are not alone."
            ),
            pii_detected=pii,
            crisis_detected=crisis,
            sensitive_topics=sensitive,
        )

    high_risk = {
        "health_diagnosis_request",
        "legal_advice_request",
        "financial_guarantee_request",
        "password_or_secret_request",
    }
    if high_risk.intersection(sensitive):
        return SafetyResult(
            safe=True,
            level="high",
            flags=flags,
            action="warn",
            message=(
                "This request may involve diagnosis, legal liability, guaranteed returns, or access to secrets. "
                "I cannot provide that kind of certainty or access. I can help you prepare to talk to the right "
                "professional or protect what is yours."
            ),
            pii_detected=pii,
            crisis_detected=crisis,
            sensitive_topics=sensitive,
        )

    if pii:
        return SafetyResult(
            safe=True,
            level="medium",
            flags=flags,
            action="warn",
            message=(
                "This message appears to contain personal or sensitive information. I will not save or send "
                "anything without your permission. Please be cautious about sharing full SSNs, card numbers, or passwords."
            ),
            pii_detected=pii,
            crisis_detected=crisis,
            sensitive_topics=sensitive,
        )

    if sensitive:
        return SafetyResult(
            safe=True,
            level="low",
            flags=flags,
            action="warn",
            message=(
                "This topic is sensitive. I can offer general information and help you think through next steps, "
                "but I will not replace a qualified professional."
            ),
            pii_detected=pii,
            crisis_detected=crisis,
            sensitive_topics=sensitive,
        )

    return SafetyResult(
        safe=True,
        level="none",
        flags=flags,
        action="allow",
        message="No safety issues detected.",
        pii_detected=pii,
        crisis_detected=crisis,
        sensitive_topics=sensitive,
    )
