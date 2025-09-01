from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from backend.core.config import settings

class ChromaRepository:
    def __init__(self, persist_dir: Optional[str] = None, collection: Optional[str] = None):
        self.persist_dir = persist_dir or settings.chroma_db_dir
        self.collection_name = collection or settings.collection_name
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=ChromaSettings(allow_reset=False)
        )
        self.collection = self.client.get_or_create_collection(self.collection_name)

    def upsert(
        self,
        ids: List[str],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        embeddings: List[List[float]],
    ):
        """
        Upsert into Chroma: documents + metadatas + embeddings.
        """
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(self, query_text: str, top_k: int = None):
        """
        Embed the user query and retrieve top-k matches from Chroma.
        """
        client = OpenAI(api_key=settings.openai_api_key)
        emb = client.embeddings.create(model=settings.embed_model, input=query_text)
        query_vec = emb.data[0].embedding

        k = top_k or settings.top_k
        res = self.collection.query(
            query_embeddings=[query_vec],
            n_results=k,
            include=["metadatas", "documents", "distances"]
        )

        results = []
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            results.append({
                "title": meta.get("title"),
                "tags": meta.get("tags"),
                "short": doc,
                "distance": dist
            })
        return results
