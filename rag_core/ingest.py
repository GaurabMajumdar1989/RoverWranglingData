import hashlib
from pathlib import Path
import json
import numpy as np
from rag_core.store import FaissStore
from rag_core.embed import generate_embeddings   # use your existing embed logic
from rag_core.config import RAG_STORE_PATH

MANIFEST_PATH = (RAG_STORE_PATH / "manifest.json").resolve()

def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_manifest(manifest: dict):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

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


def load_document(source: str  | Path) -> str:
  with open(source, 'r', encoding="utf-8") as file:
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
    print(f"CHUNKS=============>inside chunk_test() in ingest{chunks}")
    return chunks  

def ingest_with_faiss(doc_id: str, chunks: list[str]):
    """
    Phase 2 ingestion:
    - checks manifest
    - embeds chunks once
    - stores embeddings in FAISS
    """
    print(f"DOC ID recieved in ingest_with_faiss()=====>{doc_id}")
    full_text = "".join(chunks)

    if not should_ingest(doc_id, full_text):
        print(f"[INGEST] Skipped unchanged doc: {doc_id}")
        return

    print(f"[INGEST] Embedding and storing: {doc_id}")

    embeddings = generate_embeddings(chunks)
    print(f"embeddings generated from LLM OhhLLAMA====>\n{embeddings}")

    embeddings = np.array(embeddings).astype("float32")
    print(f"embeddings generated for FAISS after changing the dimension np.array(embeddings).astype===>\n{embeddings}")

    print(f"embeddings dimension change before supplying to store embeddings.shape[1]===>\n{embeddings.shape[1]}")
    #print(f"[INGEST] {doc_id}: {len(chunks)} chunks, dim={embeddings.shape[1]}")
    store = FaissStore(dim=embeddings.shape[1])

    metadata = [
        {
            "doc_id": doc_id,
            "chunk_index": i,
            "text": chunk
        }
        for i, chunk in enumerate(chunks)
    ]
    print(f"Before adding to store metadata ========{metadata}")
    store.add(embeddings, metadata)
    store.persist()

    print(f"[INGEST] Stored {len(chunks)} chunks in FAISS")