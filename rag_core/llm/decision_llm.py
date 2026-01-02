# rag_core/llm/decision_llm.py

import requests
from rag_core.config import OLLAMA_BASE_URL


def call_decision_llm(prompt: str) -> str:
    """
    Calls an LLM ONLY for decision-making.
    - Input: governance prompt
    - Output: raw text (expected JSON)
    - No embeddings
    - No context injection
    """

    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )

    resp.raise_for_status()
    return resp.json()["response"]
