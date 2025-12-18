# rag_core/guardrails/evaluator.py

from .config import *
import statistics


def evaluate_guardrails(ranked_chunks):
    failures = []

    if not ranked_chunks or len(ranked_chunks) < MIN_CHUNKS:
        return {
            "pass": False,
            "failures": ["INSUFFICIENT_EVIDENCE"],
            "metrics": {}
        }

    confidences = [c["retrieval_confidence"] for c in ranked_chunks]

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

    return {
        "pass": len(failures) == 0,
        "failures": failures,
        "metrics": {
            "mean_confidence": round(mean_conf, 4),
            "confidence_spread": round(spread, 4),
            "top_k_coverage": round(coverage, 4),
        }
    }
