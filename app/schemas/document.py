from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    text: str = Field(..., min_length=1)
    source: str
    source_path: Path | None = None
    file_type: str
    page: int | None = None
    sheet_name: str | None = None
    row_range: str | None = None
    chunk_index: int
    chunk_id: str
    access_level: str = "employee"
    department: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
