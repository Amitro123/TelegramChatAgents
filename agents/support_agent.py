# ========================================
# agents/support_agent.py
# Main support agent logic
# ========================================

import time
from typing import Dict, Any

from config.settings import settings
from core.rag import RAGEngine
from handlers.order_handler import OrderHandler
from handlers.context_handler import ContextHandler
from handlers.fallback_handler import FallbackHandler
from utils.logger import logger

class SupportAgent:
    """Customer support agent"""
    
    def __init__(self):
        self.rag = RAGEngine()
        self.order_handler = OrderHandler()
        self.context_handler = ContextHandler()
        self.fallback_handler = FallbackHandler()
        
        # Load knowledge base
        self.rag.load_knowledge_base()
        
        logger.info("✅ Support agent initialized")
    
async def process_message(self, query: str, user_id: str,
                         platform: str = "telegram") -> Dict[str, Any]:
    """Process user message with enhanced order handling"""
    start_time = time.time()
    
    logger.log_query(user_id, query, platform)
    
    try:
        # Check if order-related (now with user_id for context)
        if self.order_handler.is_order_query(query, user_id):
            order_result = self.order_handler.handle_order_query(query, user_id)
            
            result = {
                "answer": order_result["message"],
                "confidence": 1.0,
                "status": "order_handled",
                "sources_used": 0
            }
            
            # Calculate latency
            latency_ms = int((time.time() - start_time) * 1000)
            logger.log_response(
                user_id, result["confidence"], result["status"],
                latency_ms, result["sources_used"]
            )
            
            return result
        
        # If user was waiting for order number but sent something else,
        # clear the waiting state
        self.order_handler.clear_waiting_state(user_id)
        
        # Add conversation context
        context = self.context_handler.get_context(user_id)
        enhanced_query = f"{context}\n\n{query}" if context else query
        
        # RAG flow
        search_results = await self.rag.search(enhanced_query)
        
        if not search_results:
            result = {
                "answer": self.fallback_handler.get("no_context"),
                "confidence": 0.0,
                "status": "no_context",
                "sources_used": 0
            }
        else:
            result = await self.rag.generate_answer(query, search_results)
        
        # Save to context
        self.context_handler.add_message(
            user_id, query, result["answer"], result["confidence"]
        )
        
        # Log response
        latency_ms = int((time.time() - start_time) * 1000)
        logger.log_response(
            user_id, result["confidence"], result["status"],
            latency_ms, result["sources_used"]
        )
        
        # Check if approval needed
        if result["confidence"] < settings.CONFIDENCE_MEDIUM:
            logger.log_approval_needed(user_id, query, result["confidence"])
        
        return result
        
    except Exception as e:
        logger.log_error(user_id, e, "process_message")
        return {
            "answer": self.fallback_handler.get("technical_error"),
            "confidence": 0.0,
            "status": "error",
            "sources_used": 0
        }
