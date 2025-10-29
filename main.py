from integrations.telegram_bot import TelegramBot
from utils.logger import logger
from config.settings import settings
import sys

def main():
    """Enhanced main with error handling"""
    try:
        logger.info("="* 50)
        logger.info("🤖 AI Support Agent Starting...")
        logger.info(f"Model: {settings.LLM_MODEL}")
        logger.info(f"Confidence Thresholds: High={settings.CONFIDENCE_HIGH}, Medium={settings.CONFIDENCE_MEDIUM}")
        logger.info("="* 50)
        
        # Check environment
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
            sys.exit(1)
        
        if not settings.OPENAI_API_KEY:
            logger.error("❌ OPENAI_API_KEY not set!")
            sys.exit(1)
        
        # Initialize and run bot
        bot = TelegramBot()
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Keyboard interrupt received")
        logger.info("🛑 Bot shutting down gracefully...")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        logger.error("🛑 Bot crashed. Check logs above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
