#!/usr/bin/env python3
"""
Wrapper script to run PDF indexing.
Handles Python path setup and runs the indexing service.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Now import and run the indexing
from telegram_agent.application.rag_indexing_service.index_documents import index_documents
from telegram_agent.infrastructure.utils.logger import logger

if __name__ == "__main__":
    try:
        logger.info("="*70)
        logger.info("🚀 Starting document indexing...")
        logger.info("="*70)
        
        index_documents()
        
        logger.info("="*70)
        logger.info("🎉 Indexing Complete!")
        logger.info("="*70)
        
    except Exception as e:
        logger.error(f"❌ Error during indexing: {e}", exc_info=True)
        sys.exit(1)
