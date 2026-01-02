from rag_core.guardrails.evaluator import evaluate_guardrails


def test_low_coverage_guardrail_triggers():
    ranked_chunks = [
        {"retrieval_confidence": 0.60},
        {"retrieval_confidence": 0.60},
        {"retrieval_confidence": 0.60},
        {"retrieval_confidence": 0.60},
        {"retrieval_confidence": 0.60},
    ]

    result = evaluate_guardrails(ranked_chunks, query="who is rover wrangler")

    assert result["pass"] is False
    assert "LOW_COVERAGE" in result["failures"]
    assert "top_k_coverage" in result["metrics"]
