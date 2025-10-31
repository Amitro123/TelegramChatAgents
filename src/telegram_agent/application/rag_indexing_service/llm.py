from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from telegram_agent.config.settings import settings
from telegram_agent.infrastructure.utils.logger import logger
from functools import lru_cache
import collections
import hashlib

class LLMManager:
    """Manage LLM interactions"""
    
    def __init__(self):
        self.chat_model = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        logger.info(f"✅ LLM initialized: {settings.LLM_MODEL}")


        self.answer_cache = collections.OrderedDict()
        self.max_cache_size = settings.LLM_CACHE_SIZE if hasattr(settings, "LLM_CACHE_SIZE") else 500

    async def generate(self, prompt: str) -> str:
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        if prompt_hash in self.answer_cache:
            self.answer_cache.move_to_end(prompt_hash)
            logger.debug(f"LLM answer cache hit for prompt: {prompt[:30]}")
            return self.answer_cache[prompt_hash]

        try:
            response = await self.chat_model.ainvoke(prompt)
            answer = response.content
            self.answer_cache[prompt_hash] = answer
            self.answer_cache.move_to_end(prompt_hash)
            if len(self.answer_cache) > self.max_cache_size:
                self.answer_cache.popitem(last=False)
            return answer
        except Exception as e:
            logger.error(f"LLM generation error: {e}", exc_info=True)
            raise

    def get_embeddings(self):
        """Get embeddings instance"""
        return self.embeddings
