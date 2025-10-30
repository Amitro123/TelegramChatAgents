#!/usr/bin/env python3
"""Test localization of info tools"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from telegram_agent.application.conversation_service.workflow.info_tools import (
    get_working_hours, get_shipping_info, get_refund_policy, get_faq, get_support_contact
)

print("🧪 Testing Localization\n")
print("="*70)

# Test Hebrew queries
print("\n📝 Hebrew Queries:")
print("-"*70)
print("Working Hours (HE):", get_working_hours("מה שעות הפעילות?"))
print("Shipping (HE):", get_shipping_info("כמה זמן לוקח משלוח?"))
print("Refund (HE):", get_refund_policy("מה מדיניות ההחזרות?"))
print("FAQ (HE):", get_faq("יש לי שאלה"))
print("Support (HE):", get_support_contact("איך ליצור קשר?"))

# Test English queries
print("\n📝 English Queries:")
print("-"*70)
print("Working Hours (EN):", get_working_hours("What are your hours?"))
print("Shipping (EN):", get_shipping_info("How long is delivery?"))
print("Refund (EN):", get_refund_policy("What is your refund policy?"))
print("FAQ (EN):", get_faq("I have a question"))
print("Support (EN):", get_support_contact("How to contact support?"))

print("\n" + "="*70)
print("✅ Localization test complete!")
