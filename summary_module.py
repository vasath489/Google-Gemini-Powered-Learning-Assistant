"""Summarization module (Gemini)."""
from gemini_client import generate

SYSTEM = (
    "You summarize educational text for quick revision. Keep the key facts, "
    "remove repetition, and do not add information that is not in the text."
)


def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the passage below in 4-6 short bullet points, then add a "
        "one-line 'Key takeaway'.\n\nPassage:\n" + text
    )
    return generate(prompt, system=SYSTEM)
