# Pydantic request/response models
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    title: Optional[str]
    rationale: str
    full_summary: Optional[str]
