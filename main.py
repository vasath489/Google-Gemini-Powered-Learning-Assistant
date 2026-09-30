"""EduGenie - Google Gemini powered learning assistant (FastAPI backend)."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from gemini_client import GeminiError
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

app = FastAPI(title="EduGenie", description="Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=6000)
    level: str = Field("beginner", max_length=30)  # used by /learn/recommendations


def _run(func, *args):
    """Call a module function and turn Gemini errors into clean HTTP errors."""
    try:
        return func(*args)
    except GeminiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/qa")
def qa(body: TextRequest):
    return {"result": _run(answer_question, body.text)}


@app.post("/explain")
def explain(body: TextRequest):
    return {"result": _run(explain_concept, body.text)}


@app.post("/quiz")
def quiz(body: TextRequest):
    return {"questions": _run(generate_quiz, body.text)}


@app.post("/summarize")
def summarize(body: TextRequest):
    return {"result": _run(summarize_text, body.text)}


@app.post("/learn/recommendations")
def learn(body: TextRequest):
    return {"result": _run(get_learning_recommendations, body.text, body.level)}
