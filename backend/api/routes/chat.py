from fastapi import APIRouter
from backend.usecases.chat_rag import run_chat_rag
from backend.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    """
    Main RAG chat endpoint.
    Takes a user query, retrieves candidates, 
    lets GPT pick one, and appends the deterministic full summary.
    """
    result = run_chat_rag(payload.query)
    return ChatResponse(**result)
