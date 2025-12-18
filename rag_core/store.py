import faiss
import json
import numpy as np
from rag_core.config import RAG_STORE_PATH


INDEX_PATH = (RAG_STORE_PATH / "index.faiss").resolve()
META_PATH = (RAG_STORE_PATH / "metadata.json").resolve()



class FaissStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = None
        self.metadata = []

        if INDEX_PATH.exists() and META_PATH.exists():
            self.index = faiss.read_index(str(INDEX_PATH))
            with open(META_PATH, "r", encoding="utf-8") as f:
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
        faiss.write_index(self.index, str(INDEX_PATH))
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
