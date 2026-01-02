from rag_core.tools.config import CONDENSE_PREFIX_CHARS

def condense_evidence(chunks: list[dict]) -> list[dict]:
    seen = set()
    condensed = []
    print(f"`Condensing {len(chunks)} chunks to remove duplicates...\nChunks before condensing: {chunks}\n")
    for chunk in chunks:
        key = chunk["chunk"][:CONDENSE_PREFIX_CHARS]
        if key in seen:
            continue

        seen.add(key)
        condensed.append({
            "chunk_idx": chunk["chunk_idx"],
            "rank": chunk["rank"],
            "retrieval_confidence": chunk["retrieval_confidence"],
            "chunk": chunk["chunk"],
        })
    print(f"Chunks after condensing:  {condensed}\n")
    return condensed
