import os

# Define the exact structure
PROJECT_STRUCTURE = {
    "backend": {
        "api": {
            "routes": {
                "__init__.py": "",
                "chat.py": "# /chat endpoint\n",
                "ingest.py": "# /ingest endpoint\n",
                "media.py": "# /tts, /stt, /image endpoints (grouped logically)\n",
            }
        },
        "core": {
            "__init__.py": "",
            "config.py": "# Pydantic settings, env management\n",
            "guards.py": "# profanity filter, rate limiting\n",
            "logging.py": "# logging + middleware\n",
        },
        "domain": {
            "__init__.py": "",
            "book.py": "# Book entity (title, tags, short, full)\n",
            "recommendation.py": "# Recommendation entity (title + rationale)\n",
        },
        "schemas": {
            "__init__.py": "",
            "chat.py": "# Pydantic request/response models\n",
        },
        "repositories": {
            "__init__.py": "",
            "chroma_repo.py": "# Persistence/retrieval for ChromaDB\n",
            "json_repo.py": "# Local JSON datastore for full summaries\n",
        },
        "usecases": {
            "__init__.py": "",
            "chat_rag.py": "# Main RAG flow orchestration (embed → retrieve → LLM → tool)\n",
            "ingest_books.py": "# Ingestion of book_summaries into Chroma\n",
            "generate_tts.py": "# Optional text-to-speech logic\n",
            "generate_stt.py": "# Optional speech-to-text logic\n",
            "generate_image.py": "# Optional image generation logic\n",
        },
        "tools": {
            "__init__.py": "",
            "book_tools.py": "# get_summary_by_title, condense_summary\n",
        },
        "main.py": "# FastAPI app, include_routers\n",
    },
    "data": {
        "book_summaries.json": '[\n  {\n    "title": "Example Book",\n    "tags": ["demo"],\n    "short": "A short blurb...",\n    "full": "A long deterministic summary..."\n  }\n]\n'
    },
    ".env": "# OPENAI_API_KEY=your_key_here\n# CHROMA_DB_DIR=./chroma\n",
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    print("🚀 Creating Smart Librarian project scaffold...")
    create_structure(".", PROJECT_STRUCTURE)
    print("✅ Project structure created successfully.")
