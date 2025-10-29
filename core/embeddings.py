from functools import lru_cache
from typing import List
import hashlib

from core.llm import LLMManager
from utils.logger import logger

class EmbeddingCache:
    """Simple caching for embeddings"""
    
    def __init__(self, llm_manager: LLMManager):
        self.llm_manager = llm_manager
        self.embeddings = llm_manager.get_embeddings()
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info("✅ Embedding cache initialized")
    
    @lru_cache(maxsize=1000)
    def _get_cached_embedding(self, text_hash: str, text: str) -> List[float]:
        """Cached embedding retrieval"""
        self.cache_misses += 1
        return self.embeddings.embed_query(text)
    
    def embed_query(self, text: str) -> List[float]:
        """Get embedding with caching"""
        # Create hash of text for cache key
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Try cache
        result = self._get_cached_embedding(text_hash, text)
        
        # Check if it was cache hit
        info = self._get_cached_embedding.cache_info()
        if info.hits > self.cache_hits:
            self.cache_hits = info.hits
            logger.debug(f"💾 Cache hit for query (total hits: {self.cache_hits})")
        
        return result

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for a list of documents with caching (synchronous)"""
        return [self.embed_query(text) for text in texts]

    async def aembed_documents(self, texts: list) -> list:
        """Get embeddings for a list of documents with caching (async)"""
        return [self.embed_query(text) for text in texts]

    def get_stats(self) -> dict:
        """Get cache statistics"""
        info = self._get_cached_embedding.cache_info()
        return {
            "hits": info.hits,
            "misses": info.misses,
            "size": info.currsize,
            "max_size": info.maxsize
        }
    
    def clear_cache(self):
        """Clear the cache"""
        self._get_cached_embedding.cache_clear()
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info("🗑️ Embedding cache cleared")

