# rag_core/main_phase4.py

from rag_core.agents.contracts import RetrievalMetrics
from rag_core.retrieve import retrieve_with_faiss

from rag_core.guardrails.evaluator import evaluate_guardrails
from rag_core.guardrails.fallbacks import select_fallback
from rag_core.guardrails.render import render_response

from rag_core.agents.factory import get_decision_agent
from rag_core.tools.condense import condense_evidence
from rag_core.tools.rerank import rerank_top_k
from rag_core.tools.retry import bounded_retry
import logging
from rag_core.generate import generate_answer

def run_phase4():
    logging.basicConfig(level=logging.INFO)

    print("=== RWD Phase 4: Governed RAG Runner ===")

    query = "Who is Rover Wrangler and what struggles does he face in Aethelgard?"
    print(f"\nQuery: {query}\n")

    agent = get_decision_agent()

    # Phase 2: Retrieval (frozen, ranked evidence)
    ranked_chunks = retrieve_with_faiss(query)

    print("\nRetrieved Evidence:")
    for c in ranked_chunks:
        print(
            f"  - chunk_id={c['chunk_idx']}, "
            f"rank={c['rank']}, "
            f"confidence={c['retrieval_confidence']}"
        )

    # Phase 4: Governed Generation
    guardrail_result = evaluate_guardrails(ranked_chunks, query)
    print("Guardrail Evaluation Result:\n", guardrail_result)

    if not guardrail_result["pass"]:
        metrics = guardrail_result["metrics"]

        decision = agent.decide(RetrievalMetrics(
            mean_confidence=metrics["mean_confidence"],
            confidence_spread=metrics["confidence_spread"],
            top_k_coverage=metrics["top_k_coverage"],
            flags=guardrail_result["failures"]
            )
        )

        logging.info({
            "phase": "Phase 6",
            "agent": "DecisionAgent",
            "tool": decision.tool,
            "reason": decision.reason,
            "metrics": guardrail_result["metrics"]
        })

        # Phase 6 tool execution
        if decision.tool == "condense_evidence":
            ranked_chunks = condense_evidence(ranked_chunks)

        elif decision.tool == "rerank_top_k":
            ranked_chunks = rerank_top_k(ranked_chunks)

        elif decision.tool == "bounded_retry":
            return bounded_retry(query)

        elif decision.tool == "abort_with_explanation":
            strategy = select_fallback(guardrail_result["failures"])
            return render_response(strategy, ranked_chunks)


    # Only here generation is allowed
    answer = generate_answer(ranked_chunks, query)
    print("\nGenerated Answer:")
    print(answer)
    return {
        "answer": answer,
        "evidence": ranked_chunks,
        "metrics": guardrail_result["metrics"],
        "confidence": "medium"  # max allowed in Phase 4
    }
   


if __name__ == "__main__":
    run_phase4()
