# ========================================
# handlers/fallback_handler.py
# Error fallback responses
# ========================================

class FallbackHandler:
    """Enhanced fallback responses for all error scenarios"""
    
    FALLBACKS = {
        # API Errors
        "openai_error": (
            "מצטער, נתקלתי בבעיה בחיבור לשרת החכם שלי 🤖\n"
            "אנסה שוב בעוד רגע או צור קשר עם נציג."
        ),
        
        "api_timeout": (
            "הבקשה לקחה יותר מדי זמן ⏱️\n"
            "אנסה שוב או שלח שאלה אחרת."
        ),
        
        # Content Errors
        "no_context": (
            "לא מצאתי מידע על זה במאגר הידע שלי 📚\n"
            "האם תוכל לנסח את השאלה אחרת?\n"
            "או צור קשר עם נציג: support@company.com"
        ),
        
        "low_confidence": (
            "אני לא בטוח מספיק בתשובה שלי 🤔\n"
            "שלחתי את השאלה לנציג אנושי שיחזור אליך בהקדם.\n"
            "זמן תגובה משוער: 5-10 דקות"
        ),
        
        # Technical Errors
        "technical_error": (
            "אופס! משהו השתבש מצידי 🔧\n"
            "הצוות הטכני קיבל התראה.\n\n"
            "בינתיים, נסה:\n"
            "📧 Email: support@company.com\n"
            "📞 Phone: 03-1234567"
        ),
        
        "database_error": (
            "נתקלתי בבעיה בגישה למאגר המידע 💾\n"
            "הצוות הטכני עובד על זה.\n"
            "נסה שוב בעוד דקה."
        ),
        
        # Rate Limiting
        "rate_limit": (
            "קיבלתי יותר מדי בקשות ברגע זה 🚦\n"
            "המתן 10 שניות ונסה שוב."
        ),
        
        # Default
        "unknown_error": (
            "משהו לא צפוי קרה 🤷\n"
            "נסה שוב או צור קשר: support@company.com"
        )
    }
    
    @staticmethod
    def get(error_type: str) -> str:
        """Get fallback response"""
        return FallbackHandler.FALLBACKS.get(
            error_type,
            FallbackHandler.FALLBACKS["unknown_error"]
        )
    
    @staticmethod
    def get_all_types() -> list:
        """Get all available fallback types"""
        return list(FallbackHandler.FALLBACKS.keys())