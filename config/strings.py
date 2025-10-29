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
