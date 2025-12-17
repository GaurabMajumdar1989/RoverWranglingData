# retrieve.py
import numpy as np
from rag_core.store import FaissStore
from rag_core.embed import generate_embeddings

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def top_k_similar(
    query_vector: np.ndarray,
    doc_vectors: np.ndarray,
    k: int = 2,
):
    """
    Return indices of top-k most similar document vectors.
    """
    scores = []

    for idx, vec in enumerate(doc_vectors):
        score = cosine_similarity(query_vector, vec)
        scores.append((idx, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:k]

def retrieve_with_faiss(query: str, k: int = 10, threshold: float = 0.3):
    """
    Phase 2 retrieval using FAISS
    """

    # Step 1: embed query (only one embedding → cheap)
    query_embedding = generate_embeddings([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # Step 2: load FAISS index
    store = FaissStore(dim=query_embedding.shape[1])

    # Step 3: vector search
    results = store.search(query_embedding, k)

    # Step 4: similarity filtering
    filtered = [
        r for r in results
        if r["score"] >= threshold
    ]

    scored_chunks = []

    for r in filtered:
        chunk = r["metadata"]["text"]
        cosine_score = r["score"]

        keyword_score = keyword_overlap_score(query, chunk)
        score = final_score(cosine_score, keyword_score)

        scored_chunks.append({
            "chunk": chunk,
            "cosine": cosine_score,
            "keyword": keyword_score,
            "final_score": score
        })
    # -------- CONTEXT SELECTION --------

    ranked = sorted(
        scored_chunks,
        key=lambda x: x["final_score"],
        reverse=True
    )

    MIN_FINAL_SCORE = 0.4
    MAX_CONTEXT_CHUNKS = 4

    selected = [
        c for c in ranked
        if c["final_score"] >= MIN_FINAL_SCORE
    ][:MAX_CONTEXT_CHUNKS]

    if len(selected) == 0:
        return []

    return selected


def keyword_overlap_score(query: str, chunk: str) -> float:
    """
    Returns a score between 0 and 1
    based on overlapping meaningful words
    """

    def extract_keywords(text: str) -> set:
        # Convert to lowercase and find words
        # words = re.findall(r'\b\w+\b', text.lower()) import re (for regex) before that
        words = text.lower().split()
        # Define a simple list of stopwords
        stopwords = set([
            'the', 'is', 'in', 'and', 'to', 'a', 'of', 'that', 'it', 'on',
            'for', 'with', 'as', 'this', 'by', 'an', 'be', 'at', 'from',
            'or', 'are', 'was', 'but', 'not', 'have', 'has'
        ])
        # Filter out stopwords
        keywords = set(word for word in words if word not in stopwords)
        return keywords

    query_keywords = extract_keywords(query)
    chunk_keywords = extract_keywords(chunk)

    if not query_keywords or not chunk_keywords:
        return 0.0

    overlap = query_keywords.intersection(chunk_keywords)
    score = len(overlap) / len(query_keywords)

    return score

def final_score(cosine: float, keyword: float,
                w_cosine: float = 0.7,
                w_keyword: float = 0.3) -> float:
    return (w_cosine * cosine) + (w_keyword * keyword)

def select_context(
    scored_chunks,
    min_score: float = 0.4,
    max_chunks: int = 4
):
    """
    scored_chunks: list of dicts
    {
      "chunk": str,
      "final_score": float
    }
    """

    # sort by score descending
    ranked = sorted(
        scored_chunks,
        key=lambda x: x["final_score"],
        reverse=True
    )

    # filter by minimum confidence
    filtered = [
        c for c in ranked
        if c["final_score"] >= min_score
    ]

    # cap context size
    return filtered[:max_chunks]

def is_confident(selected_chunks, min_chunks: int = 1) -> bool:
    """
    Decide whether retrieval is good enough
    to proceed downstream.
    """
    return len(selected_chunks) >= min_chunks

