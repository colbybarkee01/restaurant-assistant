import os, json, datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o-mini")

app = FastAPI(title="Restaurant AI Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

with open("app/data/faq.json", "r") as f:
    DATA = json.load(f)

SYSTEM_PROMPT = (
    "You are an AI assistant for a neighborhood restaurant. "
    "Use the provided FAQs and simple table availability JSON to answer. "
    "If unsure, say you don't know and offer to collect contact info. "
    "Keep answers concise and friendly."
)
def find_faq_answer(user_msg: str) -> str | None:
    """Very simple keyword-based FAQ lookup to avoid LLM for common Qs."""
    msg = user_msg.lower()
    # try exact-ish match first
    for item in DATA.get("faqs", []):
        q = item.get("q", "").lower()
        if q and (q in msg or msg in q):
            return item.get("a")

    # fallback: keyword buckets
    if any(k in msg for k in ["hour", "open", "close", "closing", "time"]):
        for item in DATA.get("faqs", []):
            if "hour" in item.get("q", "").lower():
                return item.get("a")
    if any(k in msg for k in ["where", "address", "located", "location"]):
        for item in DATA.get("faqs", []):
            q = item.get("q", "").lower()
            if "where" in q or "located" in q or "address" in q or "location" in q:
                return item.get("a")
    if any(k in msg for k in ["vegan", "gluten", "vegetarian", "allergy"]):
        for item in DATA.get("faqs", []):
            if any(word in item.get("q", "").lower() for word in ["vegan", "gluten", "vegetarian", "allergy"]):
                return item.get("a")
    if "menu" in msg:
        for item in DATA.get("faqs", []):
            if "menu" in item.get("q", "").lower():
                return item.get("a")
    return None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    name: str | None = None
    party_size: int | None = None
    time_iso: str | None = None
    phone: str | None = None
    email: str | None = None

def check_availability(party_size: int | None, time_iso: str | None) -> str:
    if not party_size or not time_iso:
        return "If you'd like, share party size and a preferred time to check availability."
    try:
        desired = datetime.datetime.fromisoformat(time_iso)
    except ValueError:
        return "Time format should be ISO 8601 (e.g., 2025-09-05T18:00:00)."
    for t in DATA["tables"]:
        if t["available"] and t["size"] >= party_size:
            slot = datetime.datetime.fromisoformat(t["time"])
            if abs((slot - desired).total_seconds()) <= 3600:
                return f"Looks like we can fit a party of {party_size} around {slot.strftime('%-I:%M %p')}. Want me to collect your name and phone to request a reservation?"
    return "I don't see a perfect match in the next hour of your time—want me to take a request and we'll text you back?"

async def call_openai(user_prompt: str) -> str:
    if not OPENAI_API_KEY:
        return "[Missing OPENAI_API_KEY]"
    payload = {
        "model": MODEL,
        "input": f"{SYSTEM_PROMPT}\n\nFAQs and data: {json.dumps(DATA)}\n\nUser: {user_prompt}",
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    # Using embeddings/ responses surrogate: many providers accept 'responses' or 'chat.completions'.
    # We'll call chat.completions for broad compatibility.
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"FAQs/data: {json.dumps(DATA)}\n\nQuestion: {user_prompt}"}
        ]
    }
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            j = r.json()
            return j["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[LLM error: {e}]"

@app.post("/chat")
async def chat(req: ChatRequest):
    user_msg = req.messages[-1].content if req.messages else ""
    lower = user_msg.lower()

    # 1) Reservation/availability (local)
    if any(k in lower for k in ["table", "reservation", "book", "reserve"]):
        availability = check_availability(req.party_size, req.time_iso)
        return {"reply": availability}

    # 2) FAQ (local)
    faq = find_faq_answer(user_msg)
    if faq:
        return {"reply": faq}

    # 3) Otherwise fall back to LLM
    reply = await call_openai(user_msg)
    return {"reply": reply}


@app.get("/health")
async def health():
    return {"ok": True}
