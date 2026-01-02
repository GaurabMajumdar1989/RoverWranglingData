from rag_core.agents.deterministic_agent import DeterministicDecisionAgent
from rag_core.agents.contracts import RetrievalMetrics


def test_low_coverage_triggers_condense_evidence():
    agent = DeterministicDecisionAgent()

    metrics = RetrievalMetrics(
        mean_confidence=0.65,
        confidence_spread=0.10,
        top_k_coverage=0.60,
        flags=["LOW_COVERAGE"]
    )

    decision = agent.decide(metrics)

    assert decision.tool == "condense_evidence"

from rag_core.agents.config import MAX_CONFIDENCE_SPREAD


def test_high_confidence_spread_triggers_rerank():
    agent = DeterministicDecisionAgent()

    metrics = RetrievalMetrics(
        mean_confidence=0.75,
        confidence_spread=MAX_CONFIDENCE_SPREAD + 0.01,
        top_k_coverage=0.90,
        flags=[]
    )

    decision = agent.decide(metrics)

    assert decision.tool == "rerank_top_k"
