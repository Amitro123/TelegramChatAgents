from typing import Dict, List
from datetime import datetime
from telegram_agent.config.settings import settings
from telegram_agent.infrastructure.utils.logger import logger

class ContextHandler:
    """Manage conversation context and operational memory per user"""
    
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}
        self.max_history = settings.MAX_CONVERSATION_HISTORY
        logger.info(f"✅ Context handler initialized (max history: {self.max_history})")
        self.memory: Dict[str, Dict] = {}   # לכל משתמש, מילון של נתונים
    
    # ====== פונקציות MEMORY ======
    def save(self, user_id, key, value):
        if user_id not in self.memory:
            self.memory[user_id] = {}
        self.memory[user_id][key] = value
        logger.debug(f"Saved to memory for user {user_id}: {key}={value}")

    def get(self, user_id, key):
        return self.memory.get(user_id, {}).get(key)

    def has(self, user_id, key):
        return key in self.memory.get(user_id, {})

    def clear_memory(self, user_id):
        if user_id in self.memory:
            self.memory[user_id] = {}
    
    # ====== HISTORY ======
    def add_message(self, user_id: str, query: str, response: str, confidence: float):
        """Add message to history"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            "query": query,
            "response": response,
            "confidence": confidence,
            "timestamp": datetime.now()
        })
        
        # Keep only last N messages
        self.conversations[user_id] = self.conversations[user_id][-self.max_history:]
        logger.debug(f"Added message to context for user {user_id}")

    def get_context(self, user_id: str) -> str:
        """Get conversation context"""
        history = self.conversations.get(user_id, [])
        
        if not history:
            return ""
        
        # Format last 2 interactions
        context_parts = []
        for msg in history[-2:]:
            context_parts.append(
                f"Previous:\nUser: {msg['query']}\nBot: {msg['response'][:100]}"
            )
        
        return "\n\n".join(context_parts)
    
    def clear_context(self, user_id: str):
        """Clear conversation context"""
        if user_id in self.conversations:
            del self.conversations[user_id]
            logger.info(f"🔄 Cleared context for user {user_id}")

    def has_context(self, user_id: str) -> bool:
        """Check if user has context"""
        return user_id in self.conversations and len(self.conversations[user_id]) > 0
