from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    chroma_db_dir: str = Field("./chroma", env="CHROMA_DB_DIR")
    embed_model: str = Field("text-embedding-3-small", env="EMBED_MODEL")
    collection_name: str = Field("books", env="CHROMA_COLLECTION")
    top_k: int = Field(5, env="TOP_K")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")  # 👈 add this

    class Config:
        env_file = ".env"

settings = Settings()
