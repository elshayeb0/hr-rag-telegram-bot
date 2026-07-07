from pydantic import BaseModel


class Citation(BaseModel):
    source: str
    page: int | None = None
    sheet_name: str | None = None
    row_range: str | None = None
    chunk_id: str | None = None

    def format(self, index: int | None = None) -> str:
        prefix = f"[{index}] " if index is not None else ""

        location_parts: list[str] = []

        if self.page is not None:
            location_parts.append(f"page {self.page}")

        if self.sheet_name is not None:
            location_parts.append(f"sheet {self.sheet_name}")

        if self.row_range is not None:
            location_parts.append(f"rows {self.row_range}")

        location = ", ".join(location_parts)

        if location:
            return f"{prefix}[{self.source}, {location}]"

        return f"{prefix}[{self.source}]"
