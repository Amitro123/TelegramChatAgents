from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    
    # LLM Settings
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.3
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # RAG Settings
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    MAX_RETRIEVAL_RESULTS: int = 3
    LLM_CACHE_SIZE: int = 500
    
    # Confidence Thresholds
    CONFIDENCE_HIGH: float = 0.8
    CONFIDENCE_MEDIUM: float = 0.5
    
    # Context Settings
    MAX_CONVERSATION_HISTORY: int = 5
    
    # Database
    VECTOR_DB_PATH: str = "./data/demo_db"
    KNOWLEDGE_BASE_PATH: str = "./data/knowledge_base.json"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "./logs"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()
