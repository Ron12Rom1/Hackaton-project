from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class AIType(str, Enum):
    GENERAL = "general"
    PSYCHOLOGICAL = "psychological"
    MEDICAL = "medical"
    LOGISTIC = "logistic"

class AIResponse(BaseModel):
    content: str
    confidence: float
    sources: Optional[List[str]] = None
    suggested_actions: Optional[List[str]] = None

class AIRequest(BaseModel):
    user_id: str
    chat_id: str
    message: str
    context: Optional[dict] = None
    ai_type: AIType = AIType.GENERAL 