# rag_core/main_phase4.py

from rag_core.retrieve import retrieve_with_faiss

from rag_core.guardrails.evaluator import evaluate_guardrails
from rag_core.guardrails.fallbacks import select_fallback
from rag_core.guardrails.render import render_response

from rag_core.generate import generate_answer

def run_phase4():
    print("=== RWD Phase 4: Governed RAG Runner ===")

    query = "What lies dormant in Obsidian canyon?"
    print(f"\nQuery: {query}\n")

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
    guardrail_result = evaluate_guardrails(ranked_chunks)
    print("Guardrail Evaluation Result:\n", guardrail_result)

    if not guardrail_result["pass"]:
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
