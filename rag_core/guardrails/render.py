# rag_core/guardrails/render.py

def render_response(strategy, ranked_chunks):
    if strategy == "NO_ANSWER":
        return {
            "answer": None,
            "message": "Unable to answer reliably with available information.",
            "confidence": "low"
        }

    if strategy == "EVIDENCE_ONLY":
        return {
            "answer": None,
            "evidence": ranked_chunks,
            "note": "Evidence retrieved but confidence insufficient for synthesis."
        }

    if strategy == "PARTIAL_ANSWER":
        return {
            "answer": "Partial answer derived from highest-confidence evidence.",
            "evidence": ranked_chunks[:2],
            "confidence": "medium" # highest confidence level allowed after retrieval process
        }

    if strategy == "CLARIFICATION_REQUIRED":
        return {
            "answer": None,
            "message": "Please refine or narrow the query.",
            "confidence": "unknown"
        }

    return {
        "answer": None,
        "message": "Unhandled guardrail state."
    }
