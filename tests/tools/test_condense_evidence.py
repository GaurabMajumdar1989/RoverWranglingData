from rag_core.tools.condense import condense_evidence


def test_condense_evidence_removes_duplicates():
    chunks = [
        {
            "chunk_idx": 1,
            "rank": 1,
            "retrieval_confidence": 0.8,
            "chunk": "This is the same chunk text repeated many times."
        },
        {
            "chunk_idx": 2,
            "rank": 2,
            "retrieval_confidence": 0.75,
            "chunk": "This is the same chunk text repeated many times."
        },
    ]

    condensed = condense_evidence(chunks)

    assert len(condensed) == 1
    assert condensed[0]["chunk_idx"] == 1

def test_condense_evidence_keeps_unique_chunks():
    chunks = [
        {
            "chunk_idx": 1,
            "rank": 1,
            "retrieval_confidence": 0.8,
            "chunk": "First unique chunk."
        },
        {
            "chunk_idx": 2,
            "rank": 2,
            "retrieval_confidence": 0.75,
            "chunk": "Second unique chunk."
        },
    ]

    condensed = condense_evidence(chunks)

    assert len(condensed) == 2

