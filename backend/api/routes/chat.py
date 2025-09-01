from fastapi import APIRouter
from backend.usecases.chat_rag import run_chat_rag
from backend.schemas.chat import ChatRequest, ChatResponse

from fastapi import APIRouter, HTTPException
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.core.guards import enforce_profanity_guard
from backend.usecases.chat_rag import run_chat_rag


router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    is_blocked, msg = enforce_profanity_guard(payload.query)
    if is_blocked:
        # 400 Bad Request is fine; 422 Unprocessable also ok stylistically
        raise HTTPException(status_code=400, detail=msg)

    result = run_chat_rag(payload.query)
    return ChatResponse(**result)