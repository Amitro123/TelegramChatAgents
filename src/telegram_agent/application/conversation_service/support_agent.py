# ========================================
# agents/support_agent.py
# Main support agent logic
# ========================================

import time
from typing import Dict, Any

from telegram_agent.config.settings import settings
from telegram_agent.application.rag_indexing_service.rag import RAGEngine
from telegram_agent.application.conversation_service.handlers.order_handler import OrderHandler
from telegram_agent.application.conversation_service.handlers.context_handler import ContextHandler
from telegram_agent.application.conversation_service.handlers.fallback_handler import FallbackHandler
from telegram_agent.infrastructure.utils.logger import logger
from telegram_agent.application.conversation_service.workflow.agent import agent as langchain_agent, run_agent_query

class SupportAgent:
    """Customer support agent"""
    
    def __init__(self):
        self.rag = RAGEngine()
        self.order_handler = OrderHandler()
        self.context_handler = ContextHandler()
        self.fallback_handler = FallbackHandler()
        self.langchain_agent = langchain_agent
        
        # Load knowledge base
        self.rag.load_knowledge_base()
        
        logger.info("✅ Support agent initialized")
    
    async def process_message(self, query: str, user_id: str, platform: str = "telegram") -> Dict[str, Any]:
        """Process user message with intelligent routing.
        
        Routes queries to:
        1. LangChain Agent (for orders, working hours, shipping, refunds, FAQ, contact)
        2. RAG Engine (for general knowledge base queries)
        """
        start_time = time.time()
        logger.log_query(user_id, query, platform)

        try:
            # Check if this is an agent-handled query (orders or info)
            if self._should_use_agent(query, user_id):
                logger.info(f"🤖 Routing to LangChain agent: {query[:50]}...")
                result = await self._handle_agent_query(query, user_id, start_time)
            else:
                # RAG query flow for general knowledge
                logger.info(f"📚 Routing to RAG engine: {query[:50]}...")
                self.order_handler.clear_waiting_state(user_id)
                result = await self._handle_rag_query(query, user_id, platform, start_time)

            return result

        except Exception as e:
            logger.log_error(user_id, e, "process_message")
            return {
                "answer": self.fallback_handler.get("technical_error"),
                "confidence": 0.0,
                "status": "error",
                "sources_used": 0
            }

    def _should_use_agent(self, query: str, user_id: str) -> bool:
        """Determine if query should be handled by LangChain agent.
        
        Agent handles:
        - Order status queries
        - Working hours
        - Shipping info
        - Refund policy
        - FAQ
        - Support contact
        """
        query_lower = query.lower()
        
        # Check for order queries
        if self.order_handler.is_order_query(query, user_id):
            return True
        
        # Check for info tool keywords
        info_keywords = [
            # Working hours
            "שעות", "פעילות", "פתוח", "סגור", "hours", "open", "close",
            # Shipping
            "משלוח", "delivery", "shipping", "הגעה", "זמן אספקה",
            # Refund
            "החזר", "זיכוי", "ביטול", "refund", "return", "cancel",
            # FAQ
            "שאלות", "נפוצות", "faq", "שאלה",
            # Contact
            "קשר", "תמיכה", "שירות", "contact", "support", "help"
        ]
        
        return any(keyword in query_lower for keyword in info_keywords)
    
    async def _handle_agent_query(self, query: str, user_id: str, start_time: float) -> Dict[str, Any]:
        """Handle queries using LangChain agent (orders + info tools)."""
        try:
            # Check if waiting for order number
            if self.order_handler.is_order_query(query, user_id):
                order_num = self.order_handler.extract_order_number(query)
                
                if not order_num:
                    # Ask for order number
                    order_result = self.order_handler.handle_order_query(query, user_id)
                    result = {
                        "answer": order_result["message"],
                        "confidence": 1.0,
                        "status": "order_waiting",
                        "sources_used": 0
                    }
                    
                    latency_ms = int((time.time() - start_time) * 1000)
                    logger.log_response(
                        user_id, result["confidence"], result["status"],
                        latency_ms, result["sources_used"]
                    )
                    return result
            
            # Use LangChain agent
            logger.info(f"🤖 Calling LangChain agent with: {query[:50]}...")
            agent_response = run_agent_query(query)
            
            if agent_response:
                # Clear order waiting state if successful
                self.order_handler.clear_waiting_state(user_id)
                
                result = {
                    "answer": agent_response,
                    "confidence": 1.0,
                    "status": "agent_handled",
                    "sources_used": 1
                }
            else:
                # Agent failed, use fallback
                logger.warning("⚠️ Agent returned None, using fallback")
                result = {
                    "answer": self.fallback_handler.get("technical_error"),
                    "confidence": 0.0,
                    "status": "agent_error",
                    "sources_used": 0
                }
            
            # Calculate latency
            latency_ms = int((time.time() - start_time) * 1000)
            logger.log_response(
                user_id, result["confidence"], result["status"],
                latency_ms, result["sources_used"]
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error in agent query handling: {e}", exc_info=True)
            
            # Fallback
            result = {
                "answer": self.fallback_handler.get("technical_error"),
                "confidence": 0.0,
                "status": "agent_exception",
                "sources_used": 0
            }
            
            latency_ms = int((time.time() - start_time) * 1000)
            logger.log_response(
                user_id, result["confidence"], result["status"],
                latency_ms, result["sources_used"]
            )
            
            return result

    async def _handle_rag_query(self, query: str, user_id: str, platform: str, start_time: float) -> Dict[str, Any]:
        """Handle RAG-based queries"""
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
