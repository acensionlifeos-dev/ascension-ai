"""Media execution for Aerynza AI. Currently DALL-E 3 image generation."""

from __future__ import annotations

import re

from src.core.provider_keys import provider_key


def _openai_api_key(context: dict | None = None) -> str:
    """Read the OpenAI API key from shell context first, then environment names."""
    return provider_key(
        context,
        provider="openai",
        key="api_key",
        env_names=["OPENAI_API_KEY", "OPENAI_KEY", "ASCENSION_OPENAI_API_KEY"],
    )


def parse_image_request(text: str) -> str | None:
    """Extract an image-generation prompt from natural chat.

    Catches things like 'a picture of a family in a meadow' and 'draw me a cat'.
    """
    value = str(text or "").strip()
    # Specific 'a picture/photo/drawing of ...' patterns first.
    m = re.search(
        r"\b(?:an?\s+)?(?:image|picture|photo|drawing|sketch|painting)\b"
        r"\s+(?:of|show|with|depict|display|featuring|containing)\s+(.+)",
        value,
        re.I,
    )
    if m:
        return m.group(1).strip()
    # Direct draw command: 'draw me ...'
    m = re.search(r"\b(?:draw|paint|sketch)\b(?:\s+me)?[\s:—-]+(.+)", value, re.I)
    if m:
        return m.group(1).strip()
    # Generic generation verbs followed by image/picture/etc.
    m = re.search(
        r"\b(?:generate|create|make|draw|paint|sketch|render|produce)\b"
        r".{0,30}\b(?:an?\s+)?(?:image|picture|photo|drawing|sketch|painting)\b"
        r"[\s:—-]*(.*)",
        value,
        re.I,
    )
    if m:
        prompt = m.group(1).strip()
        if prompt:
            return prompt
    return None


def generate_image(prompt: str, size: str = "1024x1024", quality: str = "standard", context: dict | None = None) -> dict:
    """Generate an image with DALL-E 3 if an OpenAI key is configured."""
    api_key = _openai_api_key(context)
    if not api_key:
        return {
            "status": "no_key",
            "message": "No OpenAI API key found. The shell can supply it in context['provider_keys']['openai']['api_key'], or set OPENAI_API_KEY / OPENAI_KEY / ASCENSION_OPENAI_API_KEY in the environment.",
        }
    try:
        import openai
    except ImportError as error:
        return {
            "status": "error",
            "message": f"OpenAI client is not installed: {error}",
        }

    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
            response_format="url",
        )
        url = response.data[0].url if response.data and response.data[0].url else None
        if not url:
            return {
                "status": "error",
                "message": "DALL-E 3 returned an empty image URL.",
            }
        return {
            "status": "image",
            "url": url,
            "message": f"DALL-E 3 generated an image for: {prompt}",
        }
    except openai.APIError as error:
        return {"status": "error", "message": f"OpenAI API error: {error}"}
    except Exception as error:
        return {"status": "error", "message": str(error)}
