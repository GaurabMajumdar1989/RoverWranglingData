from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RetrievalMetrics:
    mean_confidence: float
    confidence_spread: float
    top_k_coverage: float
    flags: List[str]


@dataclass
class Decision:
    tool: str
    reason: str
