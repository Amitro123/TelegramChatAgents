
# Demo Telegram Customer Support Agent (RAG + LangChain + OpenAI)

**Minimal MVP to show RAG, confidence scoring and multi-source KB search with a Telegram bot.**

## 📦 Project Structure

demo/
├── main.py
├── knowledge_base.json
├── requirements.txt
├── .env
├── README.md
├── .gitignore
└── spec.yml

## 🚀 Quick Start

1. Clone repo: `git clone ...`
2. Install: `pip install -r requirements.txt`
3. Add secrets to `.env`
4. Launch with: `python main.py`

## Features

- Telegram bot responding in Hebrew
- RAG search over chunked knowledge base (JSON)
- Confidence scoring (high/med/low)
- Source citation and explainability
- Easy to edit knowledge base, add more sources
- Ready to expand: add WhatsApp, multi-language, admin approval, etc.

**This is MVP - code ready for Windsor spec onboarding.**

## windsor_ai.spec (for CI/CD, Docker or any pipeline)

See `spec.yml` for Windsor/CI config example.
