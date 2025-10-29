import logging
from datetime import datetime
from pathlib import Path
from config.settings import settings

class BotLogger:
    """Structured logging for the bot"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize logger"""
        # Create logs directory
        Path(settings.LOG_FILE_PATH).mkdir(exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger("SupportBot")
        self.logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        
        # File handler
        log_file = Path(settings.LOG_FILE_PATH) / f"bot_{datetime.now().strftime('%Y%m%d')}.log"
        fh = logging.FileHandler(log_file, encoding='utf-8')
        
        # Console handler
        ch = logging.StreamHandler()
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def log_query(self, user_id: str, query: str, platform: str = "telegram"):
        """Log incoming query"""
        self.logger.info(
            f"📨 Query | User: {user_id} | Platform: {platform} | "
            f"Query: {query[:50]}{'...' if len(query) > 50 else ''}"
        )

    def log_response(self, user_id: str, confidence: float,
            status: str, latency_ms: int, sources: int):
        """Log response with metrics"""
        emoji = "✅" if confidence >= 0.8 else "⚠️" if confidence >= 0.5 else "❓"
        self.logger.info(
            f"{emoji} Response | User: {user_id} | "
            f"Confidence: {confidence:.0%} | Status: {status} | "
            f"Sources: {sources} | Latency: {latency_ms}ms"
        )

    def log_error(self, user_id: str, error: Exception, context: str = ""):
        """Log error with context"""
        self.logger.error(
            f"❌ Error | User: {user_id} | Context: {context} | "
            f"Error: {str(error)}", 
            exc_info=True
        ) 
        
    def log_approval_needed(self, user_id: str, query: str, confidence: float):
        """Log when manual approval is needed"""
        self.logger.warning(
            f"⏳ Approval Needed | User: {user_id} | "
            f"Confidence: {confidence:.0%} | Query: {query[:50]}"
        )
      

    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        self.logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str):
        self.logger.debug(message)

# Global logger instance
logger = BotLogger()
