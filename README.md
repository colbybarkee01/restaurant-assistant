# Restaurant AI Assistant (FastAPI + Frontend)

🍽️ Restaurant AI Assistant

An AI-powered assistant for restaurants, built with FastAPI.
- ✅ Answers common questions (hours, location, vegan options, menu items) directly from structured FAQ data.
- ✅ Handles simple reservation requests using mock availability.
- ✅ Falls back to an LLM (OpenAI API) when a question isn’t covered by FAQs.
- ✅ Includes a lightweight web chat UI for testing and demos.
This project demonstrates how local business data can be combined with AI to provide practical, real-world solutions.

🚀 Features
- FastAPI backend with /chat and /health endpoints.
- Local FAQ lookup (no API usage for common Qs).
- Reservation logic (mock table availability via JSON).
- LLM fallback for open-ended questions.
- Web interface (static/index.html) for chatting with the bot.

📂 Project Structure

restaurant-assistant/

├── app/

│      ├── main.py          # FastAPI app + routing logic

│      └── data/faq.json    # FAQ + table availability

├── static/

│      └── index.html       # Chatbot web UI

├── .env.example         # Example environment variables

├── .gitignore

├── requirements.txt     # Python dependencies

├── run.sh               # Startup script (optional)

└── README.md

🛠️ Setup
1. Clone repo
git clone https://github.com/<your-username>/restaurant-assistant.git
cd restaurant-assistant

2. Virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

3. Install dependencies
- pip install --upgrade pip
- pip install -r requirements.txt

4. Configure environment
- Copy .env.example → .env:
- cp .env.example .env

Edit .env with your OpenAI API key:
- OPENAI_API_KEY=sk-xxxxxxx
- MODEL=gpt-4o-mini

5. Run server
- uvicorn app.main:app --reload


Server runs at: http://127.0.0.1:8000

Open the chat UI:
http://127.0.0.1:8000/static/index.html


💻 Example Usage
- “What are your hours?” → FAQ response
- “Where are you located?” → FAQ response
- “Do you have vegan options?” → FAQ response
- “Can I book a table?” (with party size + time filled) → reservation logic

Other Qs → AI fallback via OpenAI


📈 Portfolio Notes

This project is part of my AI consulting portfolio.

It demonstrates:
- Building a domain-specific AI assistant.
- Integrating structured data (FAQs, availability) with an LLM.
- Delivering a clean, demo-ready web app that businesses can immediately understand.

🔒 Security

- .env (with your real API key) is excluded via .gitignore.
- .env.example is included to help others run the project safely.


📜 License

MIT License.


docs: polished README with setup instructions and portfolio notes
