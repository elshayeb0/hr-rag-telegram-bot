import re
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.config.constants import DEFAULT_ACCESS_LEVEL
from app.schemas import DocumentChunk


def _slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def build_chunk_id(source: str, chunk_index: int, page: int | None = None, sheet_name: str | None = None) -> str:
    source_slug = _slugify(source)

    if page is not None:
        return f"{source_slug}_p{page}_c{chunk_index}"

    if sheet_name is not None:
        sheet_slug = _slugify(sheet_name)
        return f"{source_slug}_{sheet_slug}_c{chunk_index}"

    return f"{source_slug}_c{chunk_index}"


def create_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def split_raw_document(raw_document: dict[str, Any]) -> list[DocumentChunk]:
    splitter = create_text_splitter()
    raw_chunks = splitter.split_text(raw_document["text"])

    chunks: list[DocumentChunk] = []

    for index, chunk_text in enumerate(raw_chunks):
        chunk_id = build_chunk_id(
            source=raw_document["source"],
            page=raw_document.get("page"),
            sheet_name=raw_document.get("sheet_name"),
            chunk_index=index,
        )

        chunks.append(
            DocumentChunk(
                text=chunk_text,
                source=raw_document["source"],
                source_path=raw_document.get("source_path"),
                file_type=raw_document["file_type"],
                page=raw_document.get("page"),
                sheet_name=raw_document.get("sheet_name"),
                row_range=raw_document.get("row_range"),
                chunk_index=index,
                chunk_id=chunk_id,
                access_level=raw_document.get("metadata", {}).get("access_level", raw_document.get("access_level", DEFAULT_ACCESS_LEVEL)),
                department=raw_document.get("metadata", {}).get("department", raw_document.get("department")),
                metadata=raw_document.get("metadata", {}),
            )
        )

    return chunks


def split_documents(raw_documents: list[dict[str, Any]]) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []

    for raw_document in raw_documents:
        chunks.extend(split_raw_document(raw_document))

    return chunks
