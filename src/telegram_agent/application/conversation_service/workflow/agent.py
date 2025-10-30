"""LangChain Agent with integrated tools for order status and info queries."""

from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from typing import Optional

from telegram_agent.application.conversation_service.workflow.order_tools import order_status_tool
from telegram_agent.application.conversation_service.workflow.info_tools import (
    get_working_hours, get_shipping_info, get_refund_policy, get_faq, get_support_contact
)
from telegram_agent.config.strings import info_strings
from telegram_agent.config.settings import settings
from telegram_agent.infrastructure.utils.logger import logger

tools = [
    Tool(
        name="Order Status Checker",
        func=order_status_tool,
        description=info_strings.ORDER_STATUS_DESC
    ),
    Tool(
        name="Working Hours Info",
        func=get_working_hours,
        description=info_strings.WORKING_HOURS_DESC
    ),
    Tool(
        name="Shipping Info",
        func=get_shipping_info,
        description=info_strings.SHIPPING_DESC
    ),
    Tool(
        name="Refund Policy",
        func=get_refund_policy,
        description=info_strings.REFUND_DESC
    ),
    Tool(
        name="FAQ Helper",
        func=get_faq,
        description=info_strings.FAQ_DESC
    ),
    Tool(
        name="Support Contact",
        func=get_support_contact,
        description=info_strings.SUPPORT_DESC
    )
]

llm = ChatOpenAI(
    model=settings.LLM_MODEL,
    temperature=0,
    openai_api_key=settings.OPENAI_API_KEY
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

def run_agent_query(query: str) -> Optional[str]:
    """Run a query through the LangChain agent with error handling.
    
    Args:
        query: User query in Hebrew or English
        
    Returns:
        Agent response string or None if error
    """
    try:
        logger.info(f"🤖 Running agent query: {query[:50]}...")
        response = agent.run(query)
        logger.info(f"✅ Agent response received (length: {len(response)})")
        return response
    except Exception as e:
        logger.error(f"❌ Agent error: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    # Test queries
    print("\n" + "="*60)
    print("Testing LangChain Agent with Tools")
    print("="*60 + "\n")
    
    test_queries = [
        "בדוק מה קורה עם הזמנה 13354",
        "מה שעות הפעילות שלכם?",
        "מה מדיניות ההחזרות?",
        "איך ליצור קשר עם שירות לקוחות?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        result = run_agent_query(query)
        if result:
            print(f"Response: {result}")
        else:
            print("❌ Failed to get response")
        print()
