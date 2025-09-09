# Restaurant AI Assistant (FastAPI + Frontend)

A simple restaurant chatbot that can answer FAQs (hours, location, menu items),
check table availability mock data, and collect contact info for a reservation request.

## Tech
- Python 3.10+
- FastAPI, Uvicorn
- OpenAI Responses API (or compatible) via `OPENAI_API_KEY`
- Frontend: vanilla HTML + JS

## Run Locally
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # add your API key
uvicorn app.main:app --reload
# Open http://127.0.0.1:8000
```

## Environment
Create `.env` from `.env.example`:
```
OPENAI_API_KEY=sk-...
MODEL=gpt-4o-mini
```

## Deploy (optional quick ideas)
- Render, Railway, Fly.io, or Deta Space

## Portfolio Notes
- Problem statement: restaurants field repetitive questions; this bot answers FAQs and captures reservations.
- Impact: reduce phone interruptions, capture after-hours leads, consistent info.
- Next steps: integrate with real reservations API (SevenRooms/Resy), add RAG over actual menu PDF.
