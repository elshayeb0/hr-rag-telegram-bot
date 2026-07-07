from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import settings
from app.providers import get_embeddings
from app.schemas import DocumentChunk


def chunk_to_document(chunk: DocumentChunk) -> Document:
    return Document(
        page_content=chunk.text,
        metadata={
            "source": chunk.source,
            "file_type": chunk.file_type,
            "page": chunk.page,
            "sheet_name": chunk.sheet_name,
            "row_range": chunk.row_range,
            "chunk_index": chunk.chunk_index,
            "chunk_id": chunk.chunk_id,
            "access_level": chunk.access_level,
            "department": chunk.department,
        },
    )


def get_vectorstore() -> Chroma:
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=settings.chroma_collection_name,
        embedding_function=get_embeddings(),
        persist_directory=str(settings.chroma_dir),
    )


def add_chunks(chunks: list[DocumentChunk]) -> None:
    if not chunks:
        return

    vectorstore = get_vectorstore()
    documents = [chunk_to_document(chunk) for chunk in chunks]
    ids = [chunk.chunk_id for chunk in chunks]

    vectorstore.add_documents(documents=documents, ids=ids)


def clear_vectorstore() -> None:
    vectorstore = get_vectorstore()
    vectorstore.delete_collection()
