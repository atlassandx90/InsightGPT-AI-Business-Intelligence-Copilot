from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CopilotResponse:
    answer: str
    sql: Optional[str] = None
    result: Any = None
    insight: Optional[str] = None
    recommendation: Optional[str] = None
    chart_metadata: Optional[dict] = None