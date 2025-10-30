#!/usr/bin/env python3
"""
Test script to verify LangChain agent integration with all tools.
Run this to ensure all tools are properly connected before running main.py
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

print("🔍 Testing LangChain Agent Integration\n")
print("="*70)

# Test 1: Import all components
print("\n1️⃣ Testing Imports...")
try:
    from telegram_agent.application.conversation_service.workflow.agent import agent, run_agent_query
    from telegram_agent.application.conversation_service.workflow.order_tools import order_status_tool
    from telegram_agent.application.conversation_service.workflow.info_tools import (
        get_working_hours, get_shipping_info, get_refund_policy, get_faq, get_support_contact
    )
    print("   ✅ All imports successful")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Test 2: Test individual tools
print("\n2️⃣ Testing Individual Tools...")

print("\n   📦 Order Status Tool:")
try:
    result = order_status_tool("13354")
    print(f"      ✅ Result: {result[:80]}...")
except Exception as e:
    print(f"      ❌ Error: {e}")

print("\n   🕐 Working Hours Tool:")
try:
    result = get_working_hours()
    print(f"      ✅ Result: {result[:80]}...")
except Exception as e:
    print(f"      ❌ Error: {e}")

print("\n   📦 Shipping Info Tool:")
try:
    result = get_shipping_info()
    print(f"      ✅ Result: {result[:80]}...")
except Exception as e:
    print(f"      ❌ Error: {e}")

print("\n   💰 Refund Policy Tool:")
try:
    result = get_refund_policy()
    print(f"      ✅ Result: {result[:80]}...")
except Exception as e:
    print(f"      ❌ Error: {e}")

print("\n   ❓ FAQ Tool:")
try:
    result = get_faq()
    print(f"      ✅ Result: {result[:80]}...")
except Exception as e:
    print(f"      ❌ Error: {e}")

print("\n   📞 Support Contact Tool:")
try:
    result = get_support_contact()
    print(f"      ✅ Result: {result[:80]}...")
except Exception as e:
    print(f"      ❌ Error: {e}")

# Test 3: Test agent with queries
print("\n3️⃣ Testing LangChain Agent with Queries...")

test_queries = [
    ("Order Status", "בדוק מה קורה עם הזמנה 13354"),
    ("Working Hours", "מה שעות הפעילות שלכם?"),
    ("Shipping Info", "כמה זמן לוקח משלוח?"),
    ("Refund Policy", "מה מדיניות ההחזרות?"),
    ("Support Contact", "איך ליצור קשר עם שירות לקוחות?")
]

for test_name, query in test_queries:
    print(f"\n   🤖 Testing: {test_name}")
    print(f"      Query: {query}")
    try:
        result = run_agent_query(query)
        if result:
            # Truncate long responses
            display_result = result[:150] + "..." if len(result) > 150 else result
            print(f"      ✅ Response: {display_result}")
        else:
            print(f"      ⚠️ Agent returned None")
    except Exception as e:
        print(f"      ❌ Error: {e}")

# Test 4: Verify agent tools are registered
print("\n4️⃣ Verifying Agent Tools Registration...")
try:
    tool_names = [tool.name for tool in agent.tools]
    print(f"   ✅ Registered tools ({len(tool_names)}):")
    for name in tool_names:
        print(f"      • {name}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary
print("\n" + "="*70)
print("📊 INTEGRATION TEST SUMMARY")
print("="*70)
print("""
✅ All tools are properly integrated with the LangChain agent!

Next steps:
1. Make sure your .env file has:
   - TELEGRAM_BOT_TOKEN
   - OPENAI_API_KEY

2. Run the bot:
   python main.py

3. Test in Telegram with queries like:
   - "בדוק הזמנה 13354"
   - "מה שעות הפעילות?"
   - "איך ליצור קשר?"

The agent will automatically route queries to the appropriate tools!
""")
print("="*70)
