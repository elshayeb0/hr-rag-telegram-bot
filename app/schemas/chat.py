from pydantic import BaseModel, Field

from app.schemas.citation import Citation
from app.schemas.retrieval import RetrievedChunk


class ChatRequest(BaseModel):
    user_id: str
    message: str = Field(..., min_length=1)
    user_groups: list[str] = Field(default_factory=lambda: ["employee"])


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    retrieved_chunks: list[RetrievedChunk] = Field(default_factory=list)
    used_external_knowledge: bool = False
    refused: bool = False
