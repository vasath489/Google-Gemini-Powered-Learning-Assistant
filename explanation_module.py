"""Concept explanation module.

Uses the local LaMini-Flan-T5-783M model (as in the project design) when
USE_LOCAL_MODEL=true and `transformers` + `torch` are installed. Otherwise
it falls back to Gemini so the app works with a light install.
"""
import os

from gemini_client import generate

LOCAL_MODEL_ID = "MBZUAI/LaMini-Flan-T5-783M"
_pipeline = None

SYSTEM = (
    "You explain concepts to beginners. Use plain words, one everyday "
    "analogy, and a tiny example. Keep it under 150 words."
)


def _local_pipeline():
    global _pipeline
    if _pipeline is None:
        from transformers import pipeline  # imported lazily: heavy dependency

        _pipeline = pipeline("text2text-generation", model=LOCAL_MODEL_ID)
    return _pipeline


def explain_concept(topic: str) -> str:
    if os.getenv("USE_LOCAL_MODEL", "false").lower() == "true":
        try:
            prompt = f"Explain the following concept in simple words for a beginner: {topic}"
            result = _local_pipeline()(prompt, max_length=300, do_sample=False)
            return result[0]["generated_text"].strip()
        except ImportError:
            pass  # transformers/torch not installed -> use Gemini
    return generate(f"Explain this concept simply: {topic}", system=SYSTEM)
