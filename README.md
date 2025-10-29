Telegram Customer Support Agent
(RAG + LangChain + OpenAI, MVP demo)

Minimal MVP to demonstrate RAG retrieval, confidence scoring, and multi-source KB search via Telegram bot.
Designed for code review & onboarding (Windsor spec compliant).

📦 Project Structure
text
demo/
├── main.py
├── integrations/
│   └── telegram_bot.py
├── agents/
│   └── support_agent.py
├── handlers/
│   └── order_handler.py
├── knowledge_base.json
├── requirements.txt
├── .env
├── README.md
├── .gitignore
└── spec.yml
🚀 Quick Start
Clone repo:
git clone <REPO_URL>

Install dependencies:
pip install -r requirements.txt

Add secrets to .env (Telegram token, OpenAI key, etc)

Run the agent:
python main.py

Features
Telegram bot (Hebrew customer support)

RAG retrieval on chunked knowledge base (JSON)

Per-user context and enhanced order handling (Claude-style, with state)

Confidence scoring (high/medium/low) with auto/manual reply routing

Source citation and explainability

Easy to edit knowledge base and expand with new sources

Extensible system: ready for WhatsApp, Instagram, multi-language, admin approval, etc.

Code Review
PR is for review only — please leave comments, suggestions, or improvement ideas.
No direct changes in the codebase at this stage.
Focus on architecture, error handling, extensibility.

Spec / Windsor CI
See spec.yml for Windsor/CI/CD and deployment pipeline config.

Contact / Issues
Open GitHub Issues or PR comments for review feedback and questions.

Ready for production code review & onboarding.