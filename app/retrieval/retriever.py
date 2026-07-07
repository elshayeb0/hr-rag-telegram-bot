from app.config import settings
from app.retrieval.vectorstore import get_vectorstore
from app.schemas import RetrievedChunk


def _document_to_retrieved_chunk(document, score: float | None = None) -> RetrievedChunk:
    metadata = document.metadata

    return RetrievedChunk(
        text=document.page_content,
        score=score,
        source=metadata["source"],
        file_type=metadata["file_type"],
        page=metadata.get("page"),
        sheet_name=metadata.get("sheet_name"),
        row_range=metadata.get("row_range"),
        chunk_id=metadata["chunk_id"],
        access_level=metadata.get("access_level", "employee"),
        department=metadata.get("department"),
    )


def retrieve_chunks(query: str, user_groups: list[str] | None = None) -> list[RetrievedChunk]:
    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search_with_relevance_scores(
        query=query,
        k=settings.top_k,
    )

    chunks: list[RetrievedChunk] = []

    for document, score in results:
        if score < settings.min_retrieval_score:
            continue

        chunk = _document_to_retrieved_chunk(document, score=score)

        if user_groups is not None and chunk.access_level not in user_groups:
            continue

        chunks.append(chunk)

    return chunks
