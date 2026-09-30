"""Learning recommendation module (Gemini)."""
from gemini_client import generate

SYSTEM = (
    "You are a learning coach. Build practical, realistic study plans. "
    "Recommend only well-known resource types (official docs, free courses, "
    "books, video channels) and never invent specific URLs."
)


def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    prompt = f"""Create a structured learning path for: {topic}
The learner's current level is: {level}.

Format the answer in Markdown with these sections:
## Overview
## Beginner
## Intermediate
## Advanced
For each stage list the topics to learn, an estimated time, and one practice
task. Finish with "## Recommended resources" (videos, articles, books)."""
    return generate(prompt, system=SYSTEM)
