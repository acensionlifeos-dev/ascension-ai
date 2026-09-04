"""Media execution for Aerynza AI. Currently DALL-E 3 image generation."""

from __future__ import annotations

import os


def _openai_api_key() -> str:
    """Read the OpenAI API key from the most common environment names."""
    for name in ("OPENAI_API_KEY", "OPENAI_KEY", "ASCENSION_OPENAI_API_KEY"):
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


def generate_image(prompt: str, size: str = "1024x1024", quality: str = "standard") -> dict:
    """Generate an image with DALL-E 3 if an OpenAI key is configured."""
    api_key = _openai_api_key()
    if not api_key:
        return {
            "status": "no_key",
            "message": "No OpenAI API key found (checked OPENAI_API_KEY, OPENAI_KEY, ASCENSION_OPENAI_API_KEY). Add one to the environment to enable DALL-E 3 image generation.",
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
