import hashlib
import json
import os
import numpy as np
from rag_core.store import FaissStore
from rag_core.embed import generate_embeddings   # use your existing embed logic
from rag_core.config import RAG_STORE_PATH

MANIFEST_PATH = os.path.join(RAG_STORE_PATH, "manifest.json")

def load_manifest() -> dict:
    if not os.path.exists(MANIFEST_PATH):
        return {}
    with open(MANIFEST_PATH, "r") as f:
        return json.load(f)

def save_manifest(manifest: dict):
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

def should_ingest(doc_id: str, full_text: str) -> bool:
    manifest = load_manifest()
    content_hash = compute_content_hash(full_text)

    if doc_id in manifest:
        if manifest[doc_id]["hash"] == content_hash:
            return False  # unchanged

    manifest[doc_id] = {
        "hash": content_hash
    }
    save_manifest(manifest)
    return True        

def compute_content_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def load_document(source: str) -> str:
  with open(source, 'r') as file:
      return file.read()
  
def chunk_text(text: str, chunk_size: int = 200, overlap: int = 40):
    """
    Simple character-based chunking with overlap.
    Interview-safe starting point.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap

    return chunks  

def ingest_with_faiss(doc_id: str, chunks: list[str]):
    """
    Phase 2 ingestion:
    - checks manifest
    - embeds chunks once
    - stores embeddings in FAISS
    """

    full_text = "".join(chunks)

    if not should_ingest(doc_id, full_text):
        print(f"[INGEST] Skipped unchanged doc: {doc_id}")
        return

    print(f"[INGEST] Embedding and storing: {doc_id}")

    embeddings = generate_embeddings(chunks)
    embeddings = np.array(embeddings).astype("float32")

    store = FaissStore(dim=embeddings.shape[1])

    metadata = [
        {
            "doc_id": doc_id,
            "chunk_index": i,
            "text": chunk
        }
        for i, chunk in enumerate(chunks)
    ]

    store.add(embeddings, metadata)
    store.persist()

    print(f"[INGEST] Stored {len(chunks)} chunks in FAISS")