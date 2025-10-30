"""
Setup file for telegram_agent package.
This allows the package to be installed in development mode.
"""

from setuptools import setup, find_packages

setup(
    name="telegram_agent",
    version="1.0.0",
    description="AI-powered Telegram support bot with RAG capabilities",
    author="Dana",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "python-telegram-bot>=20.0",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.5",
        "langchain-community>=0.0.20",
        "openai>=1.0.0",
        "chromadb>=0.4.0",
        "pydantic-settings>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
)

