# 🤖 Telegram Customer Support Agent

AI-powered customer support bot with RAG (Retrieval-Augmented Generation), LangChain tools, and intelligent query routing.

## ✨ Features

- **🤖 LangChain Agent** with 6 specialized tools
- **📚 RAG Engine** for knowledge base queries
- **🧠 Intelligent Routing** between agent tools and RAG
- **📦 Order Status Tracking** with context memory
- **💬 Conversation Context** management per user
- **🌐 Automatic Localization** - Detects language and responds in Hebrew or English
- **📊 Confidence Scoring** with fallback handling
- **🔍 Structured Logging** for debugging

## 🏗️ Architecture

```
TelegramBot
    ↓
SupportAgent (Intelligent Router)
    ↓
    ├─→ LangChain Agent (Orders + Info)
    │   ├─→ Order Status Checker
    │   ├─→ Working Hours Info
    │   ├─→ Shipping Info
    │   ├─→ Refund Policy
    │   ├─→ FAQ Helper
    │   └─→ Support Contact
    │
    └─→ RAG Engine (General Knowledge)
        └─→ Vector Search + LLM Generation
```

## 📁 Project Structure

```
TelegramChatBot/
├── main.py                          # Entry point
├── src/
│   └── telegram_agent/              # Main package
│       ├── config/                  # Settings & strings
│       ├── application/             # Business logic
│       │   ├── conversation_service/    # Chat handling
│       │   │   ├── support_agent.py     # Main agent
│       │   │   ├── handlers/            # Context, orders, fallback
│       │   │   └── workflow/            # LangChain agent & tools
│       │   └── rag_indexing_service/    # RAG & embeddings
│       ├── infrastructure/           # External integrations
│       │   ├── telegram/            # Telegram bot
│       │   ├── clients/             # API clients
│       │   └── utils/               # Logger
│       └── domain/                  # Domain models
├── data/                            # Knowledge base
├── tests/                           # Test files
└── requirements.txt                 # Dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# OpenAI
OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Qdrant (optional)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_key

# Paths
KNOWLEDGE_BASE_PATH=./data/knowledge_base.json
LOG_FILE_PATH=./logs
```

### 3. Run the Bot

```bash
python main.py
```

### 4. Test in Telegram

Send messages to your bot:

- **Order queries**: "בדוק הזמנה 13354"
- **Info queries**: "מה שעות הפעילות?"
- **General queries**: "ספר לי על המוצר"

## 🛠️ Available Tools

| Tool | Function | Handles |
|------|----------|----------|
| **Order Status Checker** | `order_status_tool()` | Order tracking with order numbers |
| **Working Hours Info** | `get_working_hours()` | Business hours questions |
| **Shipping Info** | `get_shipping_info()` | Delivery time questions |
| **Refund Policy** | `get_refund_policy()` | Return/refund questions |
| **FAQ Helper** | `get_faq()` | General FAQ questions |
| **Support Contact** | `get_support_contact()` | Contact info requests |

## 🔄 Query Routing

The `SupportAgent` intelligently routes queries:

### Routes to LangChain Agent:
- Order queries (הזמנה, order, tracking)
- Working hours (שעות, פעילות, hours)
- Shipping (משלוח, delivery)
- Refunds (החזר, זיכוי, refund)
- FAQ (שאלות נפוצות)
- Contact (קשר, תמיכה, support)

### Routes to RAG Engine:
- General knowledge base queries
- Product information
- Company details

## 🧪 Testing

### Verify Imports
```bash
python verify_imports.py
```

### Test Agent Integration
```bash
python test_agent_integration.py
```

### Run Tests
```bash
python tests/test_agent_tools.py
```

## 📝 Configuration

### Knowledge Base

Edit `data/knowledge_base.json` to add/update content:

```json
[
  {
    "order_id": "13354",
    "content": "Order status information..."
  },
  {
    "topic": "products",
    "content": "Product information..."
  }
]
```

### Strings & Responses

Edit `src/telegram_agent/config/strings.py` to customize:
- Tool descriptions
- Response templates
- Info content (hours, shipping, refunds, etc.)

### Settings

Edit `src/telegram_agent/config/settings.py` to adjust:
- Model selection
- Confidence thresholds
- Context limits
- Paths

## 🔍 Logging

Logs are saved to `./logs/bot_YYYYMMDD.log`

Log levels:
- `INFO`: General operations
- `DEBUG`: Detailed debugging
- `WARNING`: Potential issues
- `ERROR`: Errors with stack traces

## 🌟 Key Features

### 1. Intelligent Routing
Automatically detects query type and routes to the appropriate handler.

### 2. Context Memory
Maintains conversation history and operational memory per user.

### 3. Order Tracking
Stateful order handling with waiting states for order numbers.

### 4. Error Handling
Graceful degradation with fallback responses at every level.

### 5. Bilingual Support
Handles both Hebrew and English queries seamlessly.

## 📚 Development

See `DEVELOPMENT.md` for:
- Detailed architecture documentation
- Import structure
- Adding new tools
- Debugging tips

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Built with**: Python, LangChain, OpenAI, python-telegram-bot, Qdrant