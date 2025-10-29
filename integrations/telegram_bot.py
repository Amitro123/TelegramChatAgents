# ========================================
# integrations/telegram_bot.py
# Telegram integration
# ========================================

from telegram import Update
from telegram.ext import (
    Application, CommandHandler,
    MessageHandler, filters, ContextTypes
)
import signal
import sys
import time

from agents.support_agent import SupportAgent
from config.settings import settings
from utils.logger import logger

class TelegramBot:
    """Telegram bot integration"""

    def __init__(self):
        self.agent = SupportAgent()
        self.app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        self._setup_handlers()
        self._setup_shutdown_handlers()
        logger.info("✅ Telegram bot initialized")

    def _setup_shutdown_handlers(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, sig, frame):
        logger.info("⚠️ Shutdown signal received...")
        logger.info("🛑 Bot shutting down gracefully...")
        sys.exit(0)

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("reset", self.reset_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        self.app.add_handler(CommandHandler("cache", self.cache_command))  # NEW
        self.app.add_handler(CommandHandler("clearcache", self.clearcache_command))  # NEW
        self.app.add_handler(CommandHandler("bye", self.bye_command))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "👋 שלום! אני בוט שירות לקוחות חכם.\n\n"
            "אני כאן כדי לענות על שאלות שלך.\n"
            "פשוט שלח לי שאלה! 💬\n\n"
            "Commands:\n"
            "/help - עזרה\n"
            "/reset - אפס שיחה\n"
            "/stats - סטטיסטיקות"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 איך אני עובד?\n\n"
            "1️⃣ אתה שולח שאלה\n"
            "2️⃣ אני מחפש במאגר הידע\n"
            "3️⃣ אני מייצר תשובה מדויקת\n\n"
            "✅ = ביטחון גבוה\n"
            "⚠️ = ביטחון בינוני\n"
            "❓ = ביטחון נמוך"
        )

    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        self.agent.context_handler.clear_context(user_id)
        await update.message.reply_text("🔄 השיחה אופסה!")

    async def bye_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🛑 הבוט עומד להיסגר. תודה שהשתמשת בשירות! האם יש משהו נוסף שאוכל לעזור לפני הסיום?"
        )

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        has_context = self.agent.context_handler.has_context(user_id)

        # Get cache stats
        cache_stats = self.agent.rag.embedding_cache.get_stats()
        cache_hit_rate = (
            cache_stats['hits'] / (cache_stats['hits'] + cache_stats['misses']) * 100
            if cache_stats['hits'] + cache_stats['misses'] > 0 else 0
        )

        stats_text = f"""📊 *סטטיסטיקות*

            👤 User ID: `{user_id}`
            💬 Conversation: {'✅ Active' if has_context else '❌ None'}
            🤖 Model: {settings.LLM_MODEL}

            💾 Cache Stats:
            • Hit Rate: {cache_hit_rate:.1f}%
            • Hits: {cache_stats['hits']}
            • Misses: {cache_stats['misses']}
            • Size: {cache_stats['size']}/{cache_stats['max_size']}

            _Cache helps reduce API costs!_
            """
        await update.message.reply_text(stats_text, parse_mode="Markdown")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced message handler with better error handling"""

        if not update or not update.message:
            logger.error("Received update without message")
            return

        user_message = update.message.text
        user_id = str(update.effective_user.id)

        try:
            await update.message.chat.send_action("typing")
        except Exception as e:
            logger.error(f"Failed to send typing action: {e}")

        try:
            result = await self.agent.process_message(
                query=user_message,
                user_id=user_id,
                platform="telegram"
            )

            response = result["answer"]
            if result["status"] != "order_handled":
                confidence_pct = int(result["confidence"] * 100)
                response += f"\n\n_Confidence: {confidence_pct}%_"

            await update.message.reply_text(response, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Critical error in handle_message for user {user_id}: {e}", exc_info=True)
            try:
                await update.message.reply_text(
                    "😔 מצטער, נתקלתי בבעיה טכנית.\n"
                    "הצוות קיבל התראה ועובד על פתרון.\n\n"
                    "בינתיים:\n"
                    "📧 support@company.com\n"
                    "📞 03-1234567\n\n"
                    f"קוד שגיאה: ERR-{int(time.time())}"
                )
            except Exception as send_error:
                logger.error(f"Failed to send error message to user: {send_error}")
            pass

    async def cache_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)

        ADMIN_IDS = ["YOUR_TELEGRAM_ID"]  # Add your ID here

        if user_id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only command")
            return

        cache_stats = self.agent.rag.embedding_cache.get_stats()

        cache_info = f"""💾 *Cache Management*

    Current Stats:
    • Total Hits: {cache_stats['hits']}
    • Total Misses: {cache_stats['misses']}
    • Cache Size: {cache_stats['size']}/{cache_stats['max_size']}
    • Hit Rate: {cache_stats['hits'] / (cache_stats['hits'] + cache_stats['misses']) * 100:.1f}%

    Cost Savings:
    • API Calls Saved: {cache_stats['hits']}
    • Estimated Savings: ${cache_stats['hits'] * 0.0001:.2f}

    Use /clearcache to clear cache
    """

        await update.message.reply_text(cache_info, parse_mode="Markdown")

    async def clearcache_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        ADMIN_IDS = ["YOUR_TELEGRAM_ID"]

        if user_id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Admin only command")
            return

        self.agent.rag.embedding_cache.clear_cache()
        await update.message.reply_text("🗑️ Cache cleared successfully!")

    def run(self):
        logger.info("🚀 Starting Telegram bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
