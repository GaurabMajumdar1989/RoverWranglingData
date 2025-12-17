# generate.py
import requests
import google.generativeai as genai
from rag_core.config import LLM_PROVIDER, GEMINI_API_KEY, OLLAMA_BASE_URL


def build_prompt(context_chunks: list[str], query: str) -> str:
    context = "\n\n".join(context_chunks)

    return f"""
You are an assistant answering questions strictly based on the provided context.

Context:
{context}

Question:
{query}

Answer:
""".strip()


# ---------- Gemini ----------
def generate_with_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")

    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return response.text


# ---------- Ollama ----------
def generate_with_ollama(prompt: str) -> str:
    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["response"]


# ---------- Public API ----------
def generate_answer(context_chunks: list[str], query: str) -> str:
    prompt = build_prompt(context_chunks, query)

    if LLM_PROVIDER == "gemini":
        return generate_with_gemini(prompt)
    elif LLM_PROVIDER == "ollama":
        return generate_with_ollama(prompt)
    else:
        raise RuntimeError("Unsupported provider")
