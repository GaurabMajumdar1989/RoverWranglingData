from rag_core.agents.deterministic_agent import DeterministicDecisionAgent
from rag_core.agents.llm_agent import LLMDecisionAgent

USE_LLM_DECISION_AGENT = False  # 🔁 THE FLAG


def get_decision_agent():
    if USE_LLM_DECISION_AGENT:
        return LLMDecisionAgent()
    return DeterministicDecisionAgent()
