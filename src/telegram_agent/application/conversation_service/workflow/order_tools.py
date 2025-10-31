# tools/order_tools.py

import json
from pathlib import Path
from telegram_agent.config.settings import settings
from telegram_agent.infrastructure.utils.logger import logger
from telegram_agent.application.conversation_service.handlers.context_handler import ContextHandler

# כאן תניח שיש instance אחד, מאורגן בגלובלי/Singleton ב-agent הראשי
context = ContextHandler()

def order_status_tool(order_id=None, user_id=None) -> str:
    """
    Query the system for the given order's status.
    Uses context memory if order_id is not supplied.
    """
    try:
        # ניסיון להשתמש במספר הזמנה מהשאלה, ואם לא קיים – מהזיכרון!
        if not order_id and user_id and context.has(user_id, "last_order_id"):
            order_id = context.get(user_id, "last_order_id")

        if not order_id:
            return "אנא ספק מספר הזמנה כדי שאוכל לבדוק את הסטטוס שלך."

        # שמירת מספר הזמנה בזיכרון לשיחה
        context.save(user_id, "last_order_id", order_id)

        # ניקוי (לכל מקרה – כדי למנוע כפילויות)
        clean_order_id = order_id.replace("ORD-", "").replace("#", "").strip()
        
        # טעינת בסיס הידע
        kb_path = settings.KNOWLEDGE_BASE_PATH
        if Path(kb_path).exists():
            with open(kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # חיפוש במידע
            for item in data:
                if item.get("order_id") == clean_order_id:
                    logger.info(f"✅ Found order {clean_order_id} in knowledge base")
                    return item.get("content", f"מצאתי הזמנה {clean_order_id} אך אין פרטים זמינים.")

        logger.warning(f"⚠️ Order {clean_order_id} not found in knowledge base")
        return (
            f"❌ הזמנה מספר {clean_order_id} לא נמצאה במערכת.\n"
            "אנא ודא שהמספר נכון או פנה לשירות הלקוחות:\n"
            "📧 support@company.com\n"
            "📞 03-1234567"
        )
        
    except Exception as e:
        logger.error(f"Error in order_status_tool: {e}", exc_info=True)
        return (
            f"😔 מצטער, נתקלתי בבעיה בבדיקת ההזמנה {order_id}.\n"
            "אנא נסה שוב או פנה לשירות הלקוחות."
        )
