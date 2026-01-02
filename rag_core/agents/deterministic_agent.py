from rag_core.agents.contracts import RetrievalMetrics, Decision
from rag_core.agents.config import MAX_CONFIDENCE_SPREAD


class DeterministicDecisionAgent:
    def decide(self, metrics: RetrievalMetrics) -> Decision:
        flags = metrics.flags or set()

        # 1 Hard safety vetoes
        if "HALLUCINATION_RISK" in flags:
            return Decision(
                tool="abort_with_explanation",
                reason="Hallucination risk detected"
            )

        # 2 Weak or diffuse evidence → attempt consolidation
        if "LOW_COVERAGE" in flags or "HIGH_EVIDENCE_ENTROPY" in flags:
            return Decision(
                tool="condense_evidence",
                reason="Evidence insufficient or too diffuse"
            )

        # 3 Ranking instability → rerank
        if metrics.confidence_spread > MAX_CONFIDENCE_SPREAD:
            return Decision(
                tool="rerank_top_k",
                reason="High confidence spread"
            )

        # 4 No safe corrective action left
        return Decision(
            tool="abort_with_explanation",
            reason="No safe corrective action available"
        )
