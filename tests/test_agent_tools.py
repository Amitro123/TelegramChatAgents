import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from telegram_agent.application.conversation_service.workflow.agent import agent

def test_order_status_tool():
    print("Running agent order status tests...\n")

    queries = [
        "בדוק מה קורה עם הזמנה 13354",
        "אני צריך לדעת מה הסטטוס של ORD-13354",
        "מה עם הזמנה מספר #13354?",
        "בדוק סטטוס הזמנה 99999",
        "יש עיכוב בהזמנה שלי 13354?",
        "תן לי לדעת מה מספר ההזמנה שלי"
    ]

    for q in queries:
        print("="*30)
        print(f"USER: {q}")
        try:
            response = agent.run(q)
            print(f"AGENT RESPONSE: {response}\n")
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_order_status_tool()
