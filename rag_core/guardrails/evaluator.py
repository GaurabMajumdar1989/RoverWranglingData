# rag_core/guardrails/evaluator.py

from .config import *
import statistics
import math


def evaluate_guardrails(ranked_chunks, query):
    failures = []

    if not ranked_chunks or len(ranked_chunks) < MIN_CHUNKS:
        return {
            "pass": False,
            "failures": ["INSUFFICIENT_EVIDENCE"],
            "metrics": {}
        }

    confidences = [c["retrieval_confidence"] for c in ranked_chunks]

    total_conf = sum(confidences)
    mean_conf = statistics.mean(confidences)
    spread = max(confidences) - min(confidences)

    top_k = ranked_chunks[:TOP_K]
    coverage = sum(c["retrieval_confidence"] for c in top_k) / sum(confidences)

    if mean_conf < MIN_MEAN_CONFIDENCE:
        failures.append("LOW_MEAN_CONFIDENCE")

    if spread > MAX_CONFIDENCE_SPREAD:
        failures.append("HIGH_CONFIDENCE_SPREAD")

    if coverage < MIN_TOP_K_COVERAGE:
        failures.append("LOW_COVERAGE")

      # -----------------------------
    # New guardrail: HIGH_EVIDENCE_ENTROPY
    # -----------------------------
    probs = [c / total_conf for c in confidences if c > 0]

    if len(probs) > 1:
        entropy = -sum(p * math.log(p) for p in probs)
        max_entropy = math.log(len(probs))
        normalized_entropy = entropy / max_entropy

        if normalized_entropy > MAX_CONFIDENCE_ENTROPY:
            failures.append("HIGH_EVIDENCE_ENTROPY")
    else:
        normalized_entropy = 0.0

    # -----------------------------
    # New guardrail: HALLUCINATION_RISK
    # -----------------------------
    normalized_texts = [c.get("chunk", "").lower() for c in top_k]

    if query is not None and coverage < MIN_TOP_K_COVERAGE:
        query_tokens = set(query.lower().split())
        chunk_tokens = set(" ".join(normalized_texts).split())

        if len(query_tokens & chunk_tokens) == 0:
            failures.append("HALLUCINATION_RISK")

    return {
        "pass": len(failures) == 0,
        "failures": failures,
        "metrics": {
            "mean_confidence": round(mean_conf, 4),
            "confidence_spread": round(spread, 4),
            "top_k_coverage": round(coverage, 4),
        }
    }
