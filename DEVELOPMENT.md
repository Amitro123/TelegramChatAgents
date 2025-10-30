# 🛠️ Development Guide

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Import Structure](#import-structure)
- [Adding New Tools](#adding-new-tools)
- [Query Routing Logic](#query-routing-logic)
- [Context & Memory](#context--memory)
- [Error Handling](#error-handling)
- [Debugging Tips](#debugging-tips)

## 🏗️ Architecture Overview

### Modular Structure

The project follows a clean architecture with clear separation of concerns:

```
telegram_agent/
├── config/              # Configuration (no dependencies)
├── domain/              # Domain models
├── infrastructure/      # External integrations (depends on config)
└── application/         # Business logic (depends on config + infrastructure)
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **config/** | Settings, strings, environment variables |
| **infrastructure/telegram/** | Telegram bot integration |
| **infrastructure/utils/** | Logging utilities |
| **infrastructure/clients/** | External API clients (OpenAI, Qdrant) |
| **application/conversation_service/** | Chat handling, agents, handlers |
| **application/rag_indexing_service/** | RAG engine, embeddings, LLM |
| **domain/** | Prompt templates, domain models |

## 📦 Import Structure

### Entry Point Pattern

```python
# main.py
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Now import from telegram_agent
from telegram_agent.infrastructure.telegram.telegram_bot import TelegramBot
from telegram_agent.config.settings import settings
```

### Within Package Pattern

```python
# Any file in src/telegram_agent/
from telegram_agent.config.settings import settings
from telegram_agent.infrastructure.utils.logger import logger
from telegram_agent.application.rag_indexing_service.rag import RAGEngine
```

### Import Rules

1. **Always use absolute imports** from `telegram_agent.*`
2. **Never use relative imports** across packages
3. **Avoid circular imports** - follow dependency hierarchy
4. **Import only what you need** - don't import entire modules

### Dependency Hierarchy

```
config (no dependencies)
   ↓
infrastructure (depends on config)
   ↓
application (depends on config + infrastructure)
   ↓
main.py (depends on everything)
```

## 🔧 Adding New Tools

### Step 1: Create Tool Function

Create a new file in `src/telegram_agent/application/conversation_service/workflow/`:

```python
# my_new_tool.py
from telegram_agent.config.strings import info_strings
from telegram_agent.infrastructure.utils.logger import logger

def my_new_tool(input: str = None) -> str:
    """Description of what this tool does."""
    try:
        logger.info(f"🔧 Running my_new_tool with input: {input}")
        
        # Your tool logic here
        result = "Tool response"
        
        return result
    except Exception as e:
        logger.error(f"Error in my_new_tool: {e}", exc_info=True)
        return "Error message for user"
```

### Step 2: Add Tool Description to Strings

Edit `src/telegram_agent/config/strings.py`:

```python
class InfoStrings:
    # ... existing strings ...
    
    MY_NEW_TOOL_DESC = (
        "Use this tool when the user asks about [specific topic]. "
        "Input should be the user's question."
    )
    
    MY_NEW_TOOL_ANSWER = "Your tool's response template"
```

### Step 3: Register Tool with Agent

Edit `src/telegram_agent/application/conversation_service/workflow/agent.py`:

```python
from telegram_agent.application.conversation_service.workflow.my_new_tool import my_new_tool

tools = [
    # ... existing tools ...
    Tool(
        name="My New Tool",
        func=my_new_tool,
        description=info_strings.MY_NEW_TOOL_DESC
    ),
]
```

### Step 4: Update Routing Logic

Edit `src/telegram_agent/application/conversation_service/support_agent.py`:

```python
def _should_use_agent(self, query: str, user_id: str) -> bool:
    info_keywords = [
        # ... existing keywords ...
        "new_keyword", "another_keyword",  # Add keywords for your tool
    ]
    return any(keyword in query_lower for keyword in info_keywords)
```

### Step 5: Test Your Tool

```python
# Test directly
from src.telegram_agent.application.conversation_service.workflow.my_new_tool import my_new_tool
print(my_new_tool("test input"))

# Test through agent
from src.telegram_agent.application.conversation_service.workflow.agent import run_agent_query
print(run_agent_query("query that should trigger your tool"))
```

## 🔄 Query Routing Logic

### Routing Decision Flow

```python
def process_message(query, user_id):
    if _should_use_agent(query, user_id):
        # Route to LangChain Agent
        return _handle_agent_query(query, user_id)
    else:
        # Route to RAG Engine
        return _handle_rag_query(query, user_id)
```

### Agent Routing Keywords

```python
info_keywords = [
    # Working hours
    "שעות", "פעילות", "פתוח", "סגור", "hours", "open", "close",
    
    # Shipping
    "משלוח", "delivery", "shipping", "הגעה", "זמן אספקה",
    
    # Refund
    "החזר", "זיכוי", "ביטול", "refund", "return", "cancel",
    
    # FAQ
    "שאלות", "נפוצות", "faq", "שאלה",
    
    # Contact
    "קשר", "תמיכה", "שירות", "contact", "support", "help"
]
```

### Order Query Detection

```python
ORDER_KEYWORDS = [
    "הזמנה", "מספר הזמנה", "הזמנה שלי",
    "מעקב", "tracking", "order", "משלוח שלי",
    "סטטוס", "סטאטוס", "איפה", "הגיע"
]

ORDER_PATTERNS = [
    r'ORD-\d{5,}',      # ORD-12345
    r'#\d{5,}',         # #12345
    r'\b\d{5,}\b'       # 12345 (5+ digits)
]
```

## 💾 Context & Memory

### Context Handler Features

The `ContextHandler` provides two types of storage:

#### 1. Conversation History

```python
# Add message to history
context_handler.add_message(user_id, query, response, confidence)

# Get conversation context
context = context_handler.get_context(user_id)

# Clear history
context_handler.clear_context(user_id)
```

#### 2. Operational Memory

```python
# Save data
context_handler.save(user_id, "last_order_id", "13354")

# Retrieve data
order_id = context_handler.get(user_id, "last_order_id")

# Check if exists
if context_handler.has(user_id, "last_order_id"):
    # Do something

# Clear memory
context_handler.clear_memory(user_id)
```

### Use Cases

**Conversation History**: For RAG context enhancement
```python
# Enhances queries with recent conversation
context = self.context_handler.get_context(user_id)
enhanced_query = f"{context}\n\n{query}" if context else query
```

**Operational Memory**: For stateful operations
```python
# Remember order ID across messages
if not order_id and context_handler.has(user_id, "last_order_id"):
    order_id = context_handler.get(user_id, "last_order_id")
```

## 🛡️ Error Handling

### Multi-Layer Error Handling

```
Tool Level → Agent Level → Support Agent Level → Telegram Bot Level
```

### Tool Level

```python
def my_tool(input: str) -> str:
    try:
        # Tool logic
        return result
    except Exception as e:
        logger.error(f"Error in my_tool: {e}", exc_info=True)
        return "User-friendly error message"
```

### Agent Level

```python
def run_agent_query(query: str) -> Optional[str]:
    try:
        response = agent.run(query)
        return response
    except Exception as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        return None  # Signals error to caller
```

### Support Agent Level

```python
async def _handle_agent_query(query, user_id, start_time):
    try:
        agent_response = run_agent_query(query)
        if agent_response:
            return {"answer": agent_response, "confidence": 1.0}
        else:
            # Fallback
            return {"answer": fallback_handler.get("technical_error"), "confidence": 0.0}
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return {"answer": fallback_handler.get("technical_error"), "confidence": 0.0}
```

### Fallback Responses

```python
# In fallback_handler.py
FALLBACKS = {
    "openai_error": "מצטער, נתקלתי בבעיה בחיבור לשרת החכם שלי 🤖",
    "api_timeout": "הבקשה לקחה יותר מדי זמן ⏱️",
    "no_context": "לא מצאתי מידע על זה במאגר הידע שלי 📚",
    "technical_error": "אופס! משהו השתבש מצידי 🔧",
}
```

## 🐛 Debugging Tips

### 1. Check Logs

```bash
# View latest log
tail -f logs/bot_$(date +%Y%m%d).log

# Search for errors
grep "ERROR" logs/bot_*.log

# Search for specific user
grep "user_123" logs/bot_*.log
```

### 2. Test Individual Components

```python
# Test tool directly
from src.telegram_agent.application.conversation_service.workflow.order_tools import order_status_tool
print(order_status_tool("13354"))

# Test agent
from src.telegram_agent.application.conversation_service.workflow.agent import run_agent_query
print(run_agent_query("מה שעות הפעילות?"))

# Test routing
from src.telegram_agent.application.conversation_service.support_agent import SupportAgent
agent = SupportAgent()
print(agent._should_use_agent("בדוק הזמנה", "user_123"))
```

### 3. Enable Verbose Logging

```python
# In settings.py
LOG_LEVEL = "DEBUG"  # Instead of "INFO"

# In agent.py
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # Shows agent reasoning
    handle_parsing_errors=True,
    max_iterations=3
)
```

### 4. Verify Imports

```bash
python verify_imports.py
```

### 5. Test Agent Integration

```bash
python test_agent_integration.py
```

### 6. Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Import path incorrect | Check folder names, verify `src/` in path |
| Agent not calling tool | Tool description unclear | Improve description in `info_strings` |
| Circular import | Two modules import each other | Restructure to follow dependency hierarchy |
| Tool not found | Not registered in agent | Add to `tools` list in `agent.py` |
| Query not routed | Keywords missing | Add keywords to `_should_use_agent()` |

### 7. Debug Agent Reasoning

When `verbose=True`, the agent shows its thinking:

```
> Entering new AgentExecutor chain...
I need to check the order status for order 13354.
Action: Order Status Checker
Action Input: 13354
Observation: Order 13354 is on its way...
Thought: I now know the order status
Final Answer: Your order 13354 is on its way...
```

### 8. Test Query Routing

```python
# Add debug logging
logger.info(f"Query: {query}")
logger.info(f"Should use agent: {self._should_use_agent(query, user_id)}")
logger.info(f"Is order query: {self.order_handler.is_order_query(query, user_id)}")
```

## 📊 Performance Monitoring

### Log Response Times

```python
start_time = time.time()
# ... process query ...
latency_ms = int((time.time() - start_time) * 1000)
logger.log_response(user_id, confidence, status, latency_ms, sources_used)
```

### Track Tool Usage

```python
logger.info(f"🤖 Using tool: {tool_name}")
logger.info(f"📊 Sources used: {sources_used}")
```

## 🔐 Security Best Practices

1. **Never commit `.env` file** - add to `.gitignore`
2. **Use environment variables** for all secrets
3. **Validate user input** before processing
4. **Sanitize order IDs** before database queries
5. **Log without exposing** sensitive data

## 🚀 Deployment

### Environment Variables Required

```env
TELEGRAM_BOT_TOKEN=required
OPENAI_API_KEY=required
LLM_MODEL=optional (default: gpt-4o-mini)
EMBEDDING_MODEL=optional (default: text-embedding-3-small)
QDRANT_URL=optional
QDRANT_API_KEY=optional
KNOWLEDGE_BASE_PATH=optional (default: ./data/knowledge_base.json)
LOG_FILE_PATH=optional (default: ./logs)
```

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Imports verified
- [ ] `.env` configured
- [ ] Knowledge base populated
- [ ] Logs directory created
- [ ] Error handling tested
- [ ] Fallback responses configured

---

**For questions or issues, refer to the main README.md or open a GitHub issue.**
