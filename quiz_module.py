"""Quiz generation module (Gemini).

Asks Gemini for 3 multiple-choice questions as JSON, cleans any Markdown
code fences, validates the structure and returns a Python list.
"""
import json
import re

from gemini_client import GeminiError, generate

SYSTEM = (
    "You write fair multiple-choice questions for students. "
    "Respond with valid JSON only, no commentary."
)


def clean_json_block(text: str) -> str:
    """Remove ```json ... ``` fences if the model added them."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _normalize(item: dict) -> dict:
    options = item.get("options", [])
    if len(options) != 4:
        raise ValueError("each question needs exactly 4 options")
    answer = item.get("answer")
    if isinstance(answer, int) and 0 <= answer < 4:
        idx = answer
    elif isinstance(answer, str) and answer.strip().upper() in "ABCD" and len(answer.strip()) == 1:
        idx = "ABCD".index(answer.strip().upper())
    elif answer in options:
        idx = options.index(answer)
    else:
        raise ValueError("answer must match one of the options")
    return {
        "question": str(item["question"]).strip(),
        "options": [str(o).strip() for o in options],
        "answer_index": idx,
    }


def generate_quiz(passage: str) -> list[dict]:
    prompt = f"""Create 3 multiple-choice questions from the topic or text below.
Return a JSON array. Each element must look like:
{{"question": "...", "options": ["...", "...", "...", "..."], "answer": "<the exact text of the correct option>"}}
Rules: exactly 4 options, exactly one correct, plausible wrong options.

Topic or text:
{passage}"""
    raw = generate(prompt, system=SYSTEM, json_mode=True)
    try:
        data = json.loads(clean_json_block(raw))
        if isinstance(data, dict):
            data = data.get("questions", [])
        return [_normalize(item) for item in data][:3]
    except (ValueError, KeyError, TypeError) as exc:
        raise GeminiError(f"Could not read the quiz from the model ({exc}). Please try again.") from exc
