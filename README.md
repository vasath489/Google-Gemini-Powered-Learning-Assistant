# EduGenie: Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI learning assistant for students. It answers questions, explains concepts in simple words, generates quizzes, summarizes long passages and builds personalized learning paths. The backend is built with **FastAPI** and the AI features are powered by **Google Gemini**. The frontend is plain **HTML + CSS + JavaScript**.

## Features

| Tool | What it does | Endpoint |
| --- | --- | --- |
| Ask a question | Concise answers to academic and general questions | `POST /qa` |
| Explain a concept | Beginner-friendly explanation with an example | `POST /explain` |
| Generate a quiz | 3 multiple-choice questions with instant right/wrong feedback | `POST /quiz` |
| Summarize text | Key points from a long passage | `POST /summarize` |
| Learning path | Beginner to advanced plan with timelines and resources | `POST /learn/recommendations` |

## Tech stack

- Python 3.10+
- FastAPI + Uvicorn
- Jinja2 templates, HTML, CSS, JavaScript
- Google Gemini API (`google-genai` SDK)
- Optional: LaMini-Flan-T5-783M (local model) for concept explanations

## Project structure

```
EduGenie/
├── main.py                 # FastAPI app and API routes
├── gemini_client.py        # Shared Gemini helper (API key, model, errors)
├── explanation_module.py   # Concept explanation
├── qna.py                  # Question answering
├── quiz_module.py          # Quiz generation (JSON parsing and validation)
├── summary_module.py       # Summarization
├── learning_path.py        # Learning recommendations
├── templates/index.html    # Frontend page
├── static/style.css        # Styling
├── static/app.js           # Frontend logic
├── requirements.txt        # Python dependencies
├── requirements-local.txt  # Optional local-model dependencies
└── .env.example            # Environment variable template
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/gemini-learning-assistant.git
   cd gemini-learning-assistant
   ```
2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Add your Gemini API key**
   - Get a free key from [Google AI Studio](https://aistudio.google.com/apikey).
   - Copy `.env.example` to `.env` and set `GEMINI_API_KEY=your_key`.
5. **Run the app**
   ```bash
   uvicorn main:app --reload
   ```
6. Open http://127.0.0.1:8000

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `GEMINI_API_KEY` | none (required) | Your Gemini API key |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model name. Change it if Google retires a model. |
| `USE_LOCAL_MODEL` | `false` | Set to `true` to explain concepts with LaMini-Flan-T5 locally (run `pip install -r requirements-local.txt` first) |

## How it works

1. The user picks a tool and submits text from the web page.
2. The browser sends a JSON `POST` request to the matching FastAPI endpoint.
3. The endpoint calls its module, which sends a structured prompt to Gemini.
4. The response is returned to the page. Quiz responses are cleaned, validated and rendered as interactive questions.

## Security note

The API key is read from the `.env` file, which is listed in `.gitignore`. Never commit your real key.

## Future improvements

- Voice input and multilingual support
- Progress tracking and gamification (badges, streaks)
- PDF and image input for doubt solving
- Mobile app and LMS integration

## Author

Your Name, B.Sc. Computer Science, Vetri Thiran Payirchi Thittam (Skillwallet)
