from pydantic import BaseModel
from typing import Any, List

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    data: List[Any] = []
    insight: str = ""
    confidence: str = "medium"