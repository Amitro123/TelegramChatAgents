from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict, Any
import json
from pathlib import Path
from core.embeddings import EmbeddingCache

from core.llm import LLMManager
from config.settings import settings
from utils.logger import logger

class RAGEngine:
    """RAG (Retrieval Augmented Generation) engine"""
    
    def __init__(self):
        self.llm_manager = LLMManager()
        self.embedding_cache = EmbeddingCache(self.llm_manager)
        self.embeddings = self.embedding_cache
        self.vector_store = None

        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

        self.knowledge_base = []
        self.load_knowledge_base()
        
        logger.info("✅ RAG engine initialized")
    
    def load_knowledge_base(self, file_path: str = None) -> bool:
        """Load knowledge base from JSON"""
        kb_path = file_path or settings.KNOWLEDGE_BASE_PATH
        
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.knowledge_base = data
            
            # Convert to documents
            documents = [
                Document(
                    page_content=item['content'],
                    metadata=item.get('metadata', {})
                )
                for item in data
            ]
            
            # Split and create vector store
            chunks = self.text_splitter.split_documents(documents)
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=settings.VECTOR_DB_PATH
            )
            
            logger.info(f"✅ Loaded {len(documents)} documents, {len(chunks)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}", exc_info=True)
            return False
    
    async def search(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """Search in knowledge base"""
        if not self.vector_store:
            logger.warning("Vector store not initialized")
            return []
        
        k = k or settings.MAX_RETRIEVAL_RESULTS
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                }
                for doc, score in results
            ]
        except Exception as e:
            logger.error(f"Search error: {e}", exc_info=True)
            return []
    
    async def generate_answer(self, query: str, context: List[Dict]) -> Dict[str, Any]:
        """Generate answer from context"""
        if not context:
            return {
                "answer": "מצטער, אין לי מידע על זה במאגר הידע שלי. 🤷‍♂️",
                "confidence": 0.0,
                "status": "no_context",
                "sources_used": 0
            }
        
        # Build context
        context_text = "\n\n".join([
            f"מקור {i+1}:\n{doc['content']}"
            for i, doc in enumerate(context)
        ])
        
        # Calculate confidence
        avg_score = sum(doc['score'] for doc in context) / len(context)
        confidence = max(0, min(1, 1 - (avg_score / 2)))
        
        # Generate answer
        prompt = f"""אתה עוזר שירות לקוחות. ענה על שאלת הלקוח בהתבסס **רק** על ההקשר הבא.
אם התשובה לא נמצאת בהקשר, אמור שאין לך את המידע הזה.

הקשר:
{context_text}

שאלת לקוח: {query}

תשובה (בעברית, ידידותית):"""
        
        try:
            answer = await self.llm_manager.generate(prompt)
            
            # Determine status
            if confidence >= settings.CONFIDENCE_HIGH:
                status = "high_confidence"
                emoji = "✅"
            elif confidence >= settings.CONFIDENCE_MEDIUM:
                status = "medium_confidence"
                emoji = "⚠️"
            else:
                status = "low_confidence"
                emoji = "❓"
            
            return {
                "answer": f"{emoji} {answer}",
                "confidence": confidence,
                "status": status,
                "sources_used": len(context)
            }
            
        except Exception as e:
            logger.error(f"Answer generation error: {e}", exc_info=True)
            return {
                "answer": "מצטער, הייתה בעיה בעיבוד השאלה. נסה שוב.",
                "confidence": 0.0,
                "status": "error",
                "sources_used": 0
            }
