import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

if LLM_PROVIDER not in ["gemini", "ollama"]:
    raise ValueError(f"Invalid LLM_PROVIDER {LLM_PROVIDER}. Must be 'gemini' or 'ollama'.")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAG_STORE_PATH = os.path.join(PROJECT_ROOT, "rag_store")

USE_FAISS_INGESTION = True
USE_FAISS_RETRIEVAL = True

def get_active_provider():
    return LLM_PROVIDER