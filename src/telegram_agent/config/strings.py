# ========================================
# config/strings.py
# User-facing strings for Telegram bot
# ========================================

"""
Centralized strings for easy maintenance and i18n support
"""

class BotStrings:
    """All user-facing strings for the Telegram bot"""
    
    # Command responses
    START_MESSAGE = (
        "👋 שלום! אני בוט שירות לקוחות חכם.\n\n"
        "אני כאן כדי לענות על שאלות שלך.\n"
        "פשוט שלח לי שאלה! 💬\n\n"
        "Commands:\n"
        "/help - עזרה\n"
        "/reset - אפס שיחה\n"
        "/stats - סטטיסטיקות"
    )
    
    HELP_MESSAGE = (
        "🤖 איך אני עובד?\n\n"
        "1️⃣ אתה שולח שאלה\n"
        "2️⃣ אני מחפש במאגר הידע\n"
        "3️⃣ אני מייצר תשובה מדויקת\n\n"
        "✅ = ביטחון גבוה\n"
        "⚠️ = ביטחון בינוני\n"
        "❓ = ביטחון נמוך"
    )
    
    RESET_MESSAGE = "🔄 השיחה אופסה!"
    
    BYE_MESSAGE = (
        "🛑 הבוט עומד להיסגר. תודה שהשתמשת בשירות! "
        "האם יש משהו נוסף שאוכל לעזור לפני הסיום?"
    )
    
    # Stats command
    STATS_TEMPLATE = """📊 *סטטיסטיקות*

👤 User ID: `{user_id}`
💬 Conversation: {conversation_status}
🤖 Model: {model}

💾 Cache Stats:
• Hit Rate: {hit_rate:.1f}%
• Hits: {hits}
• Misses: {misses}
• Size: {size}/{max_size}

_Cache helps reduce API costs!_
"""
    
    CONVERSATION_ACTIVE = "✅ Active"
    CONVERSATION_NONE = "❌ None"
    
    # Error messages
    ERROR_TECHNICAL = (
        "😔 מצטער, נתקלתי בבעיה טכנית.\n"
        "הצוות קיבל התראה ועובד על פתרון.\n\n"
        "בינתיים:\n"
        "📧 support@company.com\n"
        "📞 03-1234567\n\n"
        "קוד שגיאה: ERR-{error_code}"
    )
    
    # Admin commands
    ADMIN_ONLY = "⛔ Admin only command"
    
    CACHE_INFO_TEMPLATE = """💾 *Cache Management*

Current Stats:
• Total Hits: {hits}
• Total Misses: {misses}
• Cache Size: {size}/{max_size}
• Hit Rate: {hit_rate:.1f}%

Cost Savings:
• API Calls Saved: {hits}
• Estimated Savings: ${savings:.2f}

Use /clearcache to clear cache
"""
    
    CACHE_CLEARED = "🗑️ Cache cleared successfully!"
    
    # Confidence suffix
    CONFIDENCE_SUFFIX = "\n\n_Confidence: {confidence}%_"
    
    # RAG Engine strings
    RAG_NO_CONTEXT = "מצטער, אין לי מידע על זה במאגר הידע שלי. 🤷‍♂️"
    
    RAG_ERROR = "מצטער, הייתה בעיה בעיבוד השאלה. נסה שוב."
    
    RAG_PROMPT_TEMPLATE = """אתה עוזר שירות לקוחות. ענה על שאלת הלקוח בהתבסס **רק** על ההקשר הבא.
אם התשובה לא נמצאת בהקשר, אמור שאין לך את המידע הזה.

הקשר:
{context_text}

שאלת לקוח: {query}

תשובה (בעברית, ידידותית):"""
    
    # Context source template
    CONTEXT_SOURCE = "מקור {index}:\n{content}"
    
    # Confidence emojis
    EMOJI_HIGH_CONFIDENCE = "✅"
    EMOJI_MEDIUM_CONFIDENCE = "⚠️"
    EMOJI_LOW_CONFIDENCE = "❓"


# Singleton instance
strings = BotStrings()


class InfoToolsStrings:
    """Strings for info tools and agent descriptions"""

    ORDER_STATUS_DESC = (
        "בדיקת סטטוס הזמנה לפי מספר. Answers order status queries in Hebrew and English.\n"
        "Use this tool to check the status of an order. "
        "Input should be an order number (e.g., '13354', 'ORD-12345'). "
        "Returns the current status and tracking information for the order."
    )

    WORKING_HOURS_DESC = "הצגת שעות הפעילות של השירות. Provides business hours information."
    WORKING_HOURS_ANSWER_HE = "שעות הפעילות שלנו: א'-ה' 09:00-18:00. יום ו' וערבי חג: 09:00-13:00."
    WORKING_HOURS_ANSWER_EN = "Opening hours: Sunday-Thursday 09:00-18:00, Friday & holidays: 09:00-13:00."

    SHIPPING_DESC = "מידע על משלוחים וזמני הגעה. Provides shipping policy and delivery times."
    SHIPPING_ANSWER_HE = "משלוחים לכל הארץ תוך 2-5 ימי עסקים. סטטוס עדכני לא ניתן בשאלה זו."
    SHIPPING_ANSWER_EN = "Delivery in Israel within 2-5 business days."

    REFUND_DESC = "מדיניות זיכויים, החזרות, ביטולים. Answers refund/return policy questions."
    REFUND_ANSWER_HE = "מדיניות זיכויים: ניתן לבטל הזמנה עד 24 שעות לפני מועד המשלוח."
    REFUND_ANSWER_EN = "Refunds: You may cancel an order up to 24 hours before delivery."

    FAQ_DESC = "מענה לשאלות נפוצות בהרבה נושאים. Answers frequently asked questions."
    FAQ_ANSWER_HE = "נשמח לעזור! שאלות נפוצות: ביטול, החזרות, משלוח, תשלום."
    FAQ_ANSWER_EN = "FAQ: Cancellation, returns, shipping, payment."

    SUPPORT_DESC = "פרטי יצירת קשר עם שירות לקוחות. Provides customer support contact details."
    SUPPORT_ANSWER_HE = "צור קשר עם שירות לקוחות: 📞 03-1234567 | 📧 support@example.com"
    SUPPORT_ANSWER_EN = "Customer support: 📞 03-1234567 | 📧 support@example.com"


info_strings = InfoToolsStrings()
