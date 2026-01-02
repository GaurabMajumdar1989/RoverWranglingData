import json
from rag_core.agents.contracts import RetrievalMetrics, Decision

# Whatever LLM wrapper you already use (ollama / openai / gemini)
from rag_core.llm.decision_llm import call_decision_llm


ALLOWED_TOOLS = {
    "condense_evidence",
    "rerank_top_k",
    "bounded_retry",
    "abort_with_explanation",
}


class LLMDecisionAgent:
  def decide(self, metrics: RetrievalMetrics) -> Decision:
    prompt = self._build_prompt(metrics)

    try:
        raw = call_decision_llm(prompt)

        parsed = json.loads(raw)
        tool = parsed.get("tool")
        reason = parsed.get("reason", "")

        if tool not in ALLOWED_TOOLS:
            return Decision(
                tool="abort_with_explanation",
                reason=f"Invalid tool selected by LLM: {tool}"
            )

        return Decision(tool=tool, reason=reason)

    except Exception as e:
        return Decision(
            tool="abort_with_explanation",
            reason=f"Decision LLM failure: {str(e)}"
        )

  def _build_prompt(self, metrics: RetrievalMetrics) -> str:
        return f"""
You are a Decision Agent in a governed RAG system.

You are NOT allowed to:
- Answer the user
- Add new information
- Modify content

Your task:
Select exactly ONE tool that improves answer reliability.

Available tools:
- condense_evidence
- rerank_top_k
- bounded_retry
- abort_with_explanation

Metrics:
mean_confidence: {metrics.mean_confidence}
confidence_spread: {metrics.confidence_spread}
top_k_coverage: {metrics.top_k_coverage}
failure_flags: {metrics.flags}

Decision rules:
- LOW_COVERAGE → condense_evidence
- High confidence_spread → rerank_top_k
- Retry only if explicitly allowed
- If unsafe or unclear → abort_with_explanation

Respond ONLY in valid JSON:
{{
  "tool": "<one tool name>",
  "reason": "<short metric-based justification>"
}}
"""
