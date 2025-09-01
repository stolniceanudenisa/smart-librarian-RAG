from typing import List
from openai import OpenAI
from backend.core.config import settings
from backend.repositories.chroma_repo import ChromaRepository
from backend.tools.book_tools import get_short_records_for_ingest

client = OpenAI(api_key=settings.openai_api_key)

def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Calls OpenAI embeddings API for a batch of texts.
    """
    resp = client.embeddings.create(model=settings.embed_model, input=texts)
    return [item.embedding for item in resp.data]

def ingest_all() -> dict:
    """
    Loads local book_summaries.json, embeds 'short' blurbs, and upserts to Chroma.
    """
    rows = get_short_records_for_ingest()  # [(id, short, metadata), ...]
    if not rows:
        return {"ingested": 0, "message": "No records found."}

    ids = [r[0] for r in rows]
    docs = [r[1] for r in rows]
    metas = [r[2] for r in rows]

    # Embeddings (batch in one go; for large sets, chunk this list)
    vectors = embed_batch(docs)

    repo = ChromaRepository()
    repo.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=vectors)

    return {"ingested": len(rows), "collection": settings.collection_name, "persist_dir": settings.chroma_db_dir}
