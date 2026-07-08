from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")

    llm_provider: Literal["gemini", "openai"] = Field(default="gemini", alias="LLM_PROVIDER")
    llm_model: str = Field(default="gemini-2.5-flash", alias="LLM_MODEL")

    embedding_provider: Literal["gemini", "openai"] = Field(default="gemini", alias="EMBEDDING_PROVIDER")
    embedding_model: str = Field(default="gemini-embedding-001", alias="EMBEDDING_MODEL")

    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    raw_data_dir: Path = Field(default=Path("data/raw"), alias="RAW_DATA_DIR")
    processed_data_dir: Path = Field(default=Path("data/processed"), alias="PROCESSED_DATA_DIR")
    chroma_dir: Path = Field(default=Path("vectorstore/chroma"), alias="CHROMA_DIR")
    chroma_collection_name: str = Field(default="hr_documents", alias="CHROMA_COLLECTION_NAME")

    chunk_size: int = Field(default=1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, alias="CHUNK_OVERLAP")
    top_k: int = Field(default=5, alias="TOP_K")
    retrieval_fetch_k: int = Field(default=12, alias="RETRIEVAL_FETCH_K")
    max_chunks_per_source: int = Field(default=3, alias="MAX_CHUNKS_PER_SOURCE")
    min_retrieval_score: float = Field(default=0.2, alias="MIN_RETRIEVAL_SCORE")

    temperature: float = Field(default=0.0, alias="TEMPERATURE")
    max_output_tokens: int = Field(default=1000, alias="MAX_OUTPUT_TOKENS")

    max_history_messages: int = Field(default=10, alias="MAX_HISTORY_MESSAGES")

    ingest_batch_size: int = Field(default=25, alias="INGEST_BATCH_SIZE")
    ingest_batch_delay_seconds: float = Field(default=10.0, alias="INGEST_BATCH_DELAY_SECONDS")

    telegram_bot_token: str | None = Field(default=None, alias="TELEGRAM_BOT_TOKEN")


settings = Settings()
