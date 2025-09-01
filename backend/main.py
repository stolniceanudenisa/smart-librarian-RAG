from fastapi import FastAPI
from backend.api.routes import chat, debug, ingest, media

app = FastAPI(title="Smart Librarian (RAG + Tool)", version="0.1.0")
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(media.router, prefix="/media", tags=["media"])
app.include_router(debug.router, prefix="/debug", tags=["debug"])


@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}
