from pydantic import BaseModel, Field

from app.schemas.citation import Citation


class RetrievedChunk(BaseModel):
    text: str = Field(..., min_length=1)
    score: float | None = None
    source: str
    file_type: str
    page: int | None = None
    sheet_name: str | None = None
    row_range: str | None = None
    section_heading: str | None = None
    chunk_id: str
    access_level: str = "employee"
    department: str | None = None

    def to_citation(self) -> Citation:
        return Citation(
            source=self.source,
            page=self.page,
            sheet_name=self.sheet_name,
            row_range=self.row_range,
            chunk_id=self.chunk_id,
        )
