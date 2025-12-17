# embed.py
import numpy as np
import requests
import google.generativeai as genai
from rag_core.config import LLM_PROVIDER, GEMINI_API_KEY, OLLAMA_BASE_URL

# ---------- Gemini ----------
def embed_with_gemini(texts: list[str]) -> list[list[float]]:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")

    genai.configure(api_key=GEMINI_API_KEY)

    embeddings = []
    for text in texts:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document",
        )
        embeddings.append(result["embedding"])

    return embeddings


# ---------- Ollama ----------
def embed_with_ollama(texts: list[str]) -> list[list[float]]:
    embeddings = []

    for text in texts:
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": text,
            },
            timeout=30,
        )
        resp.raise_for_status()
        embeddings.append(resp.json()["embedding"])

    return embeddings


# ---------- Public API ----------
def generate_embeddings(texts: list[str]) -> np.ndarray:
    if LLM_PROVIDER == "gemini":
        vectors = embed_with_gemini(texts)
    elif LLM_PROVIDER == "ollama":
        vectors = embed_with_ollama(texts)
    else:
        raise RuntimeError("Unsupported provider")

    return np.array(vectors)
