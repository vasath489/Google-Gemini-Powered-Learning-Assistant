"""Question answering module (Gemini)."""
from gemini_client import generate

SYSTEM = (
    "You are EduGenie, a friendly tutor for students. Answer accurately and "
    "concisely in simple language. If the question is ambiguous, state the "
    "assumption you made. Use short paragraphs or bullet points."
)


def answer_question(question: str) -> str:
    return generate(f"Question: {question}", system=SYSTEM)
