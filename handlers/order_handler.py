import re
from typing import Optional, Dict
from utils.logger import logger

class OrderHandler:
    """Enhanced order handling with context awareness"""
    
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
    
    def __init__(self):
        self.pending_order_requests = {}  # user_id -> waiting for order number
        logger.info("✅ Order handler initialized")
    
    def is_order_query(self, text: str, user_id: str = None) -> bool:
        """
        Check if query is about an order
        Now considers:
        1. Keywords in text
        2. Number-only messages (if waiting for order number)
        3. Pattern match
        """
        text_lower = text.lower()
        
        # Check keywords
        has_keyword = any(kw in text_lower for kw in self.ORDER_KEYWORDS)
        
        # Check if this is a follow-up number
        is_waiting = user_id and self.pending_order_requests.get(user_id, False)
        
        # Check if it's a number that matches our pattern
        has_number = any(re.search(pattern, text) for pattern in self.ORDER_PATTERNS)
        
        result = has_keyword or (is_waiting and has_number) or has_number
        
        if result:
            logger.debug(f"Detected order query: {text[:50]} (keyword={has_keyword}, waiting={is_waiting}, number={has_number})")
        
        return result
    
    def extract_order_number(self, text: str) -> Optional[str]:
        """Extract order number from text"""
        for pattern in self.ORDER_PATTERNS:
            match = re.search(pattern, text)
            if match:
                order_num = match.group()
                logger.info(f"📦 Extracted order number: {order_num}")
                return order_num
        return None
    
    def handle_order_query(self, text: str, user_id: str) -> Dict[str, any]:
        """
        Generate order response
        Returns dict with 'message' and 'waiting_for_number' flag
        """
        order_num = self.extract_order_number(text)
        
        if order_num:
            # Clear waiting state
            self.pending_order_requests[user_id] = False
            
            return {
                "message": (
                    f"🔍 מאתר את ההזמנה **{order_num}**...\n\n"
                    f"*(בגרסת ייצור: חיבור אוטומטי למערכת ההזמנות)*\n\n"
                    f"💡 Demo Info:\n"
                    f"• מספר הזמנה: {order_num}\n"
                    f"• סטטוס: בדרך אליך 📦\n"
                    f"• משלוח משוער: 2-3 ימים\n"
                    f"• מספר מעקב: IL-{order_num}\n"
                    f"• עדכון אחרון: היום 14:30\n\n"
                    f"🔔 תקבל עדכון SMS כשההזמנה תגיע לנקודת החלוקה."
                ),
                "waiting_for_number": False
            }
        else:
            # Set waiting state
            self.pending_order_requests[user_id] = True
            
            return {
                "message": (
                    "📝 כדי לעזור לך עם ההזמנה, אני צריך את **מספר ההזמנה**.\n\n"
                    "איפה למצוא אותו?\n"
                    "✉️ במייל אישור ההזמנה\n"
                    "📱 באפליקציה שלנו בלשונית 'ההזמנות שלי'\n"
                    "🌐 באתר תחת 'איזור אישי'\n\n"
                    "💡 פורמט: ORD-12345 או #12345 או 12345\n\n"
                    "👉 **שלח לי את מספר ההזמנה עכשיו:**"
                ),
                "waiting_for_number": True
            }
    
    def clear_waiting_state(self, user_id: str):
        """Clear waiting state for user"""
        if user_id in self.pending_order_requests:
            self.pending_order_requests[user_id] = False
