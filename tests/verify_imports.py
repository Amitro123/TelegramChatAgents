#!/usr/bin/env python3
"""
Verification script to test all imports in the refactored codebase.
Run this from the project root to verify all imports work correctly.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

print("🔍 Verifying imports in refactored codebase...\n")

errors = []
successes = []

# Test 1: Config imports
print("1️⃣ Testing config imports...")
try:
    from telegram_agent.config.settings import settings
    from telegram_agent.config.strings import strings, info_strings
    successes.append("✅ Config imports")
    print("   ✅ settings, strings, info_strings")
except Exception as e:
    errors.append(f"❌ Config imports: {e}")
    print(f"   ❌ Error: {e}")

# Test 2: Infrastructure imports
print("\n2️⃣ Testing infrastructure imports...")
try:
    from telegram_agent.infrastructure.utils.logger import logger
    successes.append("✅ Infrastructure.utils imports")
    print("   ✅ logger")
except Exception as e:
    errors.append(f"❌ Infrastructure.utils imports: {e}")
    print(f"   ❌ Error: {e}")

try:
    from telegram_agent.infrastructure.telegram.telegram_bot import TelegramBot
    successes.append("✅ Infrastructure.telegram imports")
    print("   ✅ TelegramBot")
except Exception as e:
    errors.append(f"❌ Infrastructure.telegram imports: {e}")
    print(f"   ❌ Error: {e}")

# Test 3: RAG Service imports
print("\n3️⃣ Testing RAG service imports...")
try:
    from telegram_agent.application.rag_indexing_service.llm import LLMManager
    from telegram_agent.application.rag_indexing_service.embeddings import EmbeddingCache
    from telegram_agent.application.rag_indexing_service.rag import RAGEngine
    successes.append("✅ RAG service imports")
    print("   ✅ LLMManager, EmbeddingCache, RAGEngine")
except Exception as e:
    errors.append(f"❌ RAG service imports: {e}")
    print(f"   ❌ Error: {e}")

# Test 4: Conversation Service - Handlers
print("\n4️⃣ Testing conversation service handlers...")
try:
    from telegram_agent.application.conversation_service.handlers.context_handler import ContextHandler
    from telegram_agent.application.conversation_service.handlers.order_handler import OrderHandler
    from telegram_agent.application.conversation_service.handlers.fallback_handler import FallbackHandler
    successes.append("✅ Conversation handlers imports")
    print("   ✅ ContextHandler, OrderHandler, FallbackHandler")
except Exception as e:
    errors.append(f"❌ Conversation handlers imports: {e}")
    print(f"   ❌ Error: {e}")

# Test 5: Conversation Service - Workflow
print("\n5️⃣ Testing conversation service workflow...")
try:
    from telegram_agent.application.conversation_service.workflow.order_tools import order_status_tool
    from telegram_agent.application.conversation_service.workflow.info_tools import (
        get_working_hours, get_shipping_info, get_refund_policy, get_faq, get_support_contact
    )
    successes.append("✅ Workflow tools imports")
    print("   ✅ order_status_tool, info_tools functions")
except Exception as e:
    errors.append(f"❌ Workflow tools imports: {e}")
    print(f"   ❌ Error: {e}")

try:
    from telegram_agent.application.conversation_service.workflow.agent import agent
    successes.append("✅ LangChain agent import")
    print("   ✅ agent (LangChain)")
except Exception as e:
    errors.append(f"❌ LangChain agent import: {e}")
    print(f"   ❌ Error: {e}")

# Test 6: Support Agent
print("\n6️⃣ Testing support agent...")
try:
    from telegram_agent.application.conversation_service.support_agent import SupportAgent
    successes.append("✅ SupportAgent import")
    print("   ✅ SupportAgent")
except Exception as e:
    errors.append(f"❌ SupportAgent import: {e}")
    print(f"   ❌ Error: {e}")

# Summary
print("\n" + "="*60)
print("📊 VERIFICATION SUMMARY")
print("="*60)
print(f"\n✅ Successful imports: {len(successes)}/{len(successes) + len(errors)}")
for success in successes:
    print(f"   {success}")

if errors:
    print(f"\n❌ Failed imports: {len(errors)}")
    for error in errors:
        print(f"   {error}")
    print("\n⚠️  Some imports failed. Please check the errors above.")
    sys.exit(1)
else:
    print("\n🎉 All imports verified successfully!")
    print("✅ Your refactored codebase is ready to use!")
    print("\n💡 Next step: Run 'python main.py' to start the bot")
    sys.exit(0)
