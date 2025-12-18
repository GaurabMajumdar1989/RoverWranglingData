# generate.py
import requests
import google.generativeai as genai
from rag_core.config import LLM_PROVIDER, GEMINI_API_KEY, OLLAMA_BASE_URL
from rag_core.generation_utils import extract_cited_chunk_ids

INSUFFICIENT_EVIDENCE_MSG = "Insufficient evidence in retrieved context."


# ---------- Public API ----------
def generate_answer(ranked_chunks: list[dict], query: str) -> str:
    if not ranked_chunks:
        return INSUFFICIENT_EVIDENCE_MSG
    
    allowed_chunk_ids = {c['chunk_idx'] for c in ranked_chunks}

    context_chunks = [
        f"[chunk_id={c['chunk_idx']}, rank={c['rank']}]\n{c['chunk']}"
        for c in ranked_chunks
    ]
    
    print(f"Context Chunks for Generation:\n{context_chunks}")
    prompt = build_prompt(context_chunks, query)
    print(f"Prompt for LLM:\n{prompt}")
    
    if LLM_PROVIDER == "gemini":
        answer = generate_with_gemini(prompt)
    elif LLM_PROVIDER == "ollama":
        answer = generate_with_ollama(prompt)
    else:
        raise RuntimeError("Unsupported provider")
    
    cited_ids = extract_cited_chunk_ids(answer)
    print(f"Cited Chunk IDs in Answer: {cited_ids}")

    if cited_ids == allowed_chunk_ids:
        # Model likely cited everything blindly
        return INSUFFICIENT_EVIDENCE_MSG

    if not cited_ids:
        return INSUFFICIENT_EVIDENCE_MSG

    if not cited_ids.issubset(allowed_chunk_ids):
        return INSUFFICIENT_EVIDENCE_MSG
    
    return answer
    

def build_prompt(context_chunks: list[str], query: str) -> str:
    context = "\n\n".join(context_chunks)

    return f"""You MUST answer the question using ONLY the information in the context.
    If the answer is not fully supported by the context, say:
    "{INSUFFICIENT_EVIDENCE_MSG}"

    When answering, cite the chunk_id(s) you used.

    Context:
    {context}

    Question:
    {query}

    Answer (with chunk_id citations):
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
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )
    resp.raise_for_status()
    return resp.json()["response"]