from rag_core.guardrails.evaluator import evaluate_guardrails
from rag_core.agents.deterministic_agent import DeterministicDecisionAgent
from rag_core.agents.contracts import RetrievalMetrics


def test_phase6_low_coverage_flows_to_condense_evidence():
    ranked_chunks = [
        {"retrieval_confidence": 0.60},
        {"retrieval_confidence": 0.60},
        {"retrieval_confidence": 0.60},
        {"retrieval_confidence": 0.60},
        {"retrieval_confidence": 0.60},
    ]

    guardrail_result = evaluate_guardrails(
        ranked_chunks,
        query=None
    )

    metrics = RetrievalMetrics(
        mean_confidence=guardrail_result["metrics"]["mean_confidence"],
        confidence_spread=guardrail_result["metrics"]["confidence_spread"],
        top_k_coverage=guardrail_result["metrics"]["top_k_coverage"],
        flags=guardrail_result["failures"]
    )

    agent = DeterministicDecisionAgent()
    decision = agent.decide(metrics)

    assert decision.tool == "condense_evidence"
