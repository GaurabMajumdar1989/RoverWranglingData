from rag_core.guardrails.evaluator import evaluate_guardrails


def test_high_evidence_entropy_guardrail_triggers():
    ranked_chunks = [
        {"retrieval_confidence": 0.70},
        {"retrieval_confidence": 0.70},
        {"retrieval_confidence": 0.70},
        {"retrieval_confidence": 0.70},
        {"retrieval_confidence": 0.70},
    ]

    result = evaluate_guardrails(ranked_chunks, query="who is rover wrangler")

    assert result["pass"] is False
    assert "HIGH_EVIDENCE_ENTROPY" in result["failures"]
