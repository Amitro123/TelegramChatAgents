"""
PDF Document Indexing Service
Windows-compatible version using PyPDF2 and ChromaDB
"""

import PyPDF2
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from telegram_agent.config.settings import settings
from telegram_agent.infrastructure.utils.logger import logger


def load_pdf_with_pypdf2(pdf_path: str):
    """Load PDF using PyPDF2 (Windows-compatible)"""
    documents = []
    
    logger.info(f"📄 Loading: {pdf_path}")
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        
        logger.info(f"📊 Total pages: {num_pages}")
        
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            # Create a Document object for each page
            doc = Document(
                page_content=text,
                metadata={"source": pdf_path, "page": page_num + 1}
            )
            documents.append(doc)
            
            if (page_num + 1) % 5 == 0 or page_num + 1 == num_pages:
                logger.info(f"   Processed {page_num + 1}/{num_pages} pages...")
    
    logger.info(f"✅ Loaded {len(documents)} pages")
    return documents


def generate_split_documents():
    """Load and split PDF into chunks"""
    pdf_path = "./data/Return-Policy-and-Customer-Care.pdf"
    
    # Check if file exists
    if not Path(pdf_path).exists():
        logger.error(f"❌ PDF file not found: {pdf_path}")
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Load PDF
    docs = load_pdf_with_pypdf2(pdf_path)
    
    # Split into chunks
    logger.info("🔪 Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    logger.info(f"✅ Created {len(all_splits)} chunks")

    return all_splits


def index_documents():
    """Index PDF documents into ChromaDB"""
    # Generate document chunks
    all_splits = generate_split_documents()
    
    # Show sample chunk
    if all_splits:
        logger.info(f"📝 Sample chunk (first 200 chars):")
        logger.info(f"   {all_splits[0].page_content[:200]}...")
    
    # Create embeddings
    logger.info("🧠 Creating embeddings with OpenAI...")
    embeddings = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY
    )

    # Index into ChromaDB
    logger.info("📤 Indexing into ChromaDB...")
    logger.info("   Persist directory: ./chroma_db")
    
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="return_policy"
    )

    logger.info("✅ Documents indexed successfully!")
    
    # Test search
    logger.info("🔍 Testing search...")
    test_query = "What is the return policy?"
    results = vectorstore.similarity_search(test_query, k=2)
    logger.info(f"   Query: '{test_query}'")
    logger.info(f"   Found {len(results)} relevant chunks")
    if results:
        logger.info(f"   Top result (first 150 chars):")
        logger.info(f"   {results[0].page_content[:150]}...")


if __name__ == "__main__":
    try:
        logger.info("="*70)
        logger.info("🚀 Starting document indexing...")
        logger.info("="*70)
        
        index_documents()
        
        logger.info("="*70)
        logger.info("🎉 Indexing Complete!")
        logger.info("="*70)
        logger.info("📊 Summary:")
        logger.info(f"   • PDF: data/Return-Policy-and-Customer-Care.pdf")
        logger.info(f"   • Vector Store: ChromaDB (./chroma_db)")
        logger.info(f"   • Collection: return_policy")
        logger.info(f"   • Embedding Model: {settings.EMBEDDING_MODEL}")
        logger.info("✅ Your bot can now answer questions about the return policy!")
        logger.info("="*70)
        
    except Exception as e:
        logger.error(f"❌ Error during indexing: {e}")
        import traceback
        traceback.print_exc()