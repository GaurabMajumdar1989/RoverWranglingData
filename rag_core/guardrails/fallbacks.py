# rag_core/guardrails/fallbacks.py

def select_fallback(failures):
    if "INSUFFICIENT_EVIDENCE" in failures:
        return "NO_ANSWER"

    if "LOW_MEAN_CONFIDENCE" in failures:
        return "EVIDENCE_ONLY"

    if "HIGH_CONFIDENCE_SPREAD" in failures:
        return "PARTIAL_ANSWER"

    if "LOW_COVERAGE" in failures:
        return "CLARIFICATION_REQUIRED"

    return "NO_ANSWER"
