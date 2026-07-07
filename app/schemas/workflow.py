from typing import Any

from pydantic import BaseModel, Field

from app.schemas.citation import Citation


class WorkflowResult(BaseModel):
    workflow_name: str
    output: str
    citations: list[Citation] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
