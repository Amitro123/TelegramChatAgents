import asyncio
from agents.support_agent import SupportAgent

async def test_order_detection():
    agent = SupportAgent()
    
    test_cases = [
        ("אפשר לבדוק סטטוס הזמנה?", True),
        ("13354", True),  # After asking about order
        ("מה שעות הפעילות?", False),
        ("ORD-12345", True),
        ("#54321", True),
    ]
    
    for query, expected_is_order in test_cases:
        is_order = agent.order_handler.is_order_query(query, "test_user")
        status = "✅" if is_order == expected_is_order else "❌"
        print(f"{status} '{query}' -> is_order={is_order} (expected={expected_is_order})")

if __name__ == "__main__":
    asyncio.run(test_order_detection())
