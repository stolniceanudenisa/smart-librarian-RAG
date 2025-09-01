# backend/api/routes/debug.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.repositories.chroma_repo import ChromaRepository

router = APIRouter()

class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/retrieve")
def retrieve_endpoint(payload: RetrieveRequest):
    repo = ChromaRepository()
    results = repo.query(payload.query, top_k=payload.top_k)
    return results
