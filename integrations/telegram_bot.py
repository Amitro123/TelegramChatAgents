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
from config.strings import strings
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
        await update.message.reply_text(strings.START_MESSAGE)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(strings.HELP_MESSAGE)

    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        self.agent.context_handler.clear_context(user_id)
        await update.message.reply_text(strings.RESET_MESSAGE)

    async def bye_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(strings.BYE_MESSAGE)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        has_context = self.agent.context_handler.has_context(user_id)

        # Get cache stats
        cache_stats = self.agent.rag.embedding_cache.get_stats()
        cache_hit_rate = (
            cache_stats['hits'] / (cache_stats['hits'] + cache_stats['misses']) * 100
            if cache_stats['hits'] + cache_stats['misses'] > 0 else 0
        )

        stats_text = strings.STATS_TEMPLATE.format(
            user_id=user_id,
            conversation_status=strings.CONVERSATION_ACTIVE if has_context else strings.CONVERSATION_NONE,
            model=settings.LLM_MODEL,
            hit_rate=cache_hit_rate,
            hits=cache_stats['hits'],
            misses=cache_stats['misses'],
            size=cache_stats['size'],
            max_size=cache_stats['max_size']
        )
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
                response += strings.CONFIDENCE_SUFFIX.format(confidence=confidence_pct)

            await update.message.reply_text(response, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Critical error in handle_message for user {user_id}: {e}", exc_info=True)
            try:
                error_message = strings.ERROR_TECHNICAL.format(
                    error_code=int(time.time())
                )
                await update.message.reply_text(error_message)
            except Exception as send_error:
                logger.error(f"Failed to send error message to user: {send_error}")
            pass

    async def cache_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)

        if user_id not in settings.ADMIN_IDS:
            await update.message.reply_text(strings.ADMIN_ONLY)
            return

        cache_stats = self.agent.rag.embedding_cache.get_stats()
        hit_rate = (
            cache_stats['hits'] / (cache_stats['hits'] + cache_stats['misses']) * 100
            if cache_stats['hits'] + cache_stats['misses'] > 0 else 0
        )
        
        cache_info = strings.CACHE_INFO_TEMPLATE.format(
            hits=cache_stats['hits'],
            misses=cache_stats['misses'],
            size=cache_stats['size'],
            max_size=cache_stats['max_size'],
            hit_rate=hit_rate,
            savings=cache_stats['hits'] * 0.0001
        )

        await update.message.reply_text(cache_info, parse_mode="Markdown")

    async def clearcache_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)

        if user_id not in settings.ADMIN_IDS:
            await update.message.reply_text(strings.ADMIN_ONLY)
            return

        self.agent.rag.embedding_cache.clear_cache()
        await update.message.reply_text(strings.CACHE_CLEARED)

    def run(self):
        logger.info("🚀 Starting Telegram bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
