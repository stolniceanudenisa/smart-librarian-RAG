from fastapi import APIRouter, HTTPException
from backend.usecases.ingest_books import ingest_all

router = APIRouter()

@router.post("/")
def ingest_endpoint():
    try:
        result = ingest_all()
        return {"status": "ok", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
