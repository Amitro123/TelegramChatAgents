# LangChain Agent Integration Guide

## Overview

The Telegram bot now uses a **LangChain Agent** to intelligently handle order status queries. The agent can use tools to check order information from the knowledge base.

## Architecture

```
User Query → SupportAgent.process_message()
    ↓
    Is Order Query? → Yes → _handle_order_query()
    ↓                           ↓
    Extract Order Number → Use LangChain Agent
    ↓                           ↓
    LangChain Agent → OrderStatusChecker Tool
    ↓                           ↓
    order_status_tool() → Check Knowledge Base
    ↓                           ↓
    Return Status to User
```

## Components

### 1. **tools/order_tools.py**
- `order_status_tool()`: Queries the knowledge base for order information
- Cleans order IDs (removes prefixes like "ORD-", "#")
- Returns user-friendly Hebrew responses
- Handles errors gracefully

### 2. **tools/agent.py**
- Initializes LangChain agent with GPT model
- Configures the `OrderStatusChecker` tool
- Uses `ZERO_SHOT_REACT_DESCRIPTION` agent type
- Handles parsing errors and limits iterations

### 3. **agents/support_agent.py**
- `_handle_order_query()`: Main method for order queries
- Uses LangChain agent when order number is found
- Falls back to basic order handler if needed
- Comprehensive error handling

## How It Works

### Example Flow:

**User:** "בדוק הזמנה 13354"

1. **SupportAgent** detects it's an order query
2. Extracts order number: `13354`
3. Calls **LangChain Agent** with the query
4. Agent decides to use **OrderStatusChecker** tool
5. Tool searches knowledge base for order `13354`
6. Returns: "סטטוס הזמנה מס׳ 13354: נשלחה ב-27/10/2025..."
7. Response sent to user

### Agent Reasoning (REACT Pattern):

```
Thought: I need to check the status of order 13354
Action: OrderStatusChecker
Action Input: "13354"
Observation: הזמנה מספר 13354 בדרך אליך...
Thought: I now know the order status
Final Answer: [Returns the order status to user]
```

## Benefits

✅ **Intelligent Routing**: Agent decides when to use tools  
✅ **Natural Language**: Handles various query formats  
✅ **Extensible**: Easy to add more tools (shipping, returns, etc.)  
✅ **Fallback**: Graceful degradation if agent fails  
✅ **Logging**: Full visibility into agent decisions  

## Configuration

In `config/settings.py`:
```python
LLM_MODEL: str = "gpt-3.5-turbo"  # Model for agent
KNOWLEDGE_BASE_PATH: str = "./data/knowledge_base.json"
```

## Adding New Tools

To add a new tool (e.g., shipping tracker):

1. **Create tool function** in `tools/`:
```python
def shipping_tracker_tool(tracking_number: str) -> str:
    # Your logic here
    return "Shipping status..."
```

2. **Add to agent** in `tools/agent.py`:
```python
shipping_tool = Tool(
    name="ShippingTracker",
    func=shipping_tracker_tool,
    description="Track shipment by tracking number"
)

tools = [order_status, shipping_tool]
```

3. **Agent automatically uses it** when relevant!

## Testing

Test the agent directly:
```bash
python tools/agent.py
```

Or through the bot:
- "בדוק הזמנה 13354"
- "מה קורה עם ההזמנה שלי? מספר 13354"
- "איפה ההזמנה #13354?"

## Monitoring

Check logs for agent activity:
- `🤖 Using LangChain agent for order {order_num}`
- `✅ Found order {order_id} in knowledge base`
- `⚠️ Order {order_id} not found in knowledge base`

## Status Codes

- `order_handled_agent`: Successfully handled by LangChain agent
- `order_handled`: Handled by basic order handler
- `order_handled_fallback`: Agent failed, used fallback

## Future Enhancements

- [ ] Add more tools (returns, exchanges, cancellations)
- [ ] Integrate with real order management system API
- [ ] Add memory for multi-turn order conversations
- [ ] Use async agent for better performance
- [ ] Add tool for updating order information

## Troubleshooting

**Agent not working?**
- Check `OPENAI_API_KEY` in `.env`
- Verify `LLM_MODEL` is set correctly
- Check logs for agent errors

**Order not found?**
- Verify order exists in `knowledge_base.json`
- Check order_id format matches exactly
- Ensure knowledge base is loaded

**Slow responses?**
- Agent makes multiple LLM calls (thinking + tool use)
- Consider caching common queries
- Use faster model for agent (gpt-3.5-turbo)

---

**Note**: This is a demo implementation. In production, connect to real order management APIs instead of knowledge base JSON.
