import faiss
import json
import os
import numpy as np
from rag_core.config import RAG_STORE_PATH

STORE_DIR = RAG_STORE_PATH
INDEX_PATH = os.path.join(STORE_DIR, "index.faiss")
META_PATH = os.path.join(STORE_DIR, "metadata.json")


class FaissStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = None
        self.metadata = []

        os.makedirs(STORE_DIR, exist_ok=True)

        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(META_PATH, "r") as f:
                self.metadata = json.load(f)
        else:
            # Inner Product index (cosine if embeddings normalized)
            self.index = faiss.IndexFlatIP(dim)

    def add(self, embeddings: np.ndarray, metadata: list[dict]):
        self.index.add(embeddings)
        self.metadata.extend(metadata)

    def search(self, query_vec: np.ndarray, k: int):
        scores, ids = self.index.search(query_vec, k)

        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx == -1:
                continue
            results.append({
                "score": float(score),
                "metadata": self.metadata[idx]
            })

        return results

    def persist(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "w") as f:
            json.dump(self.metadata, f, indent=2)
