import os

ROOT = "TelegramChatBot"
FILES = {
    "main.py":
        "# Main chatbot logic (see previous example)\n# TODO: העתיקו לתוך קובץ זה את הקוד שלך מהפוסט הקודם!\n",
    "knowledge_base.json":
        """[
  {"content": "שעות הפעילות שלנו: ראשון-חמישי 9:00-18:00, יום שישי 9:00-13:00. אנחנו סגורים בשבת וחגים.", "metadata": {"category": "general_info", "topic": "hours"}},
  {"content": "ניתן ליצור איתנו קשר בטלפון: 03-1234567, במייל: support@company.com, או בצ'אט באתר.", "metadata": {"category": "contact", "topic": "support"}},
  {"content": "מדיניות ההחזרות שלנו: החזרה מלאה תוך 30 יום ללא שאלות. המוצר חייב להיות במצב חדש ובאריזה מקורית.", "metadata": {"category": "policy", "topic": "returns"}},
  {"content": "משלוח חינם על הזמנות מעל 200 ש״ח. משלוח רגיל עולה 20 ש״ח ומגיע תוך 3-5 ימי עסקים.", "metadata": {"category": "shipping", "topic": "delivery"}},
  {"content": "אנחנו מקבלים תשלום בכרטיסי אשראי (ויזה, מאסטרקארד), PayPal, ו-Bit. ניתן גם לשלם במזומן במשרד.", "metadata": {"category": "payment", "topic": "methods"}}
]
""",
    "requirements.txt":
        "python-telegram-bot==20.7\nlangchain==0.1.0\nlangchain-openai==0.0.2\nchromadb==0.4.22\nopenai==1.3.0\npython-dotenv==1.0.0\n",
    ".env":
        "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here\nOPENAI_API_KEY=your_openai_api_key_here\n",
    ".gitignore":
        "demo_db/\n.env\n*.pyc\n__pycache__/\n.DS_Store\n",
    "README.md":
        """
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
""",
    "spec.yml":
        """
version: '1'
pipeline:
  install:
    - pip install -r requirements.txt
  env:
    - .env
  run:
    - python main.py
  artifacts:
    - logs/
    - demo_db/
  ports:
    - "8443:8443"
description: Minimal Telegram Customer Support AI bot with RAG
"""
}

os.makedirs(ROOT, exist_ok=True)
for fname, content in FILES.items():
    with open(os.path.join(ROOT, fname), "w", encoding='utf-8') as f:
        f.write(content)

print(f"✅ Project scaffold created in: ./{ROOT}\nFiles:")
for k in FILES.keys():
    print(f" - {k}")

