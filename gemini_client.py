"""Shared helper for talking to Google Gemini.

All modules (Q&A, quiz, summary, learning path, explanation fallback)
call `generate()` so the API key, model name and error handling live in
one place.
"""
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Change the model in .env (GEMINI_MODEL) if Google retires this one.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

_client = None


class GeminiError(Exception):
    """Raised when the Gemini call cannot be completed."""


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise GeminiError(
                "GEMINI_API_KEY is missing. Copy .env.example to .env and add your key."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def generate(prompt: str, system: str | None = None, json_mode: bool = False) -> str:
    """Send a prompt to Gemini and return the response text."""
    config = types.GenerateContentConfig(
        system_instruction=system,
        response_mime_type="application/json" if json_mode else None,
    )
    try:
        response = _get_client().models.generate_content(
            model=MODEL_NAME, contents=prompt, config=config
        )
    except GeminiError:
        raise
    except Exception as exc:  # network errors, quota, invalid key, etc.
        raise GeminiError(f"Gemini request failed: {exc}") from exc

    text = (response.text or "").strip()
    if not text:
        raise GeminiError("Gemini returned an empty response. Try rephrasing your input.")
    return text
