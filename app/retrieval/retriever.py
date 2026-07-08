from app.config import settings
from app.retrieval.category_router import infer_policy_category
from app.retrieval.vectorstore import get_vectorstore
from app.schemas import RetrievedChunk


POLICY_QUERY_TERMS = {
    "policy",
    "procedure",
    "rule",
    "rules",
    "leave",
    "absence",
    "sickness",
    "sick",
    "maternity",
    "paternity",
    "disciplinary",
    "grievance",
    "harassment",
    "bullying",
    "alcohol",
    "drugs",
    "expenses",
    "byod",
    "device",
    "data protection",
    "gdpr",
    "notice",
}


def _looks_like_policy_query(query: str) -> bool:
    normalized = query.lower()
    return any(term in normalized for term in POLICY_QUERY_TERMS)


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


def _contains_restricted_term(query: str) -> bool:
    restricted_terms = {"ceo", "executive", "board", "director-only", "confidential"}
    normalized = query.lower()
    return any(term in normalized for term in restricted_terms)


def retrieve_chunks(query: str, user_groups: list[str] | None = None) -> list[RetrievedChunk]:
    if _contains_restricted_term(query) and (not user_groups or "executive" not in user_groups):
        return []

    vectorstore = get_vectorstore()

    search_kwargs = {
        "k": settings.retrieval_fetch_k,
    }

    if _looks_like_policy_query(query):
        category = infer_policy_category(query)

        if category:
            search_kwargs["filter"] = {
                "$and": [
                    {"document_type": "policy"},
                    {"policy_category": category},
                ]
            }
        else:
            search_kwargs["filter"] = {"document_type": "policy"}

    results = vectorstore.similarity_search_with_relevance_scores(
        query=query,
        **search_kwargs,
    )

    chunks: list[RetrievedChunk] = []
    source_counts: dict[str, int] = {}

    for document, score in results:
        if score < settings.min_retrieval_score:
            continue

        chunk = _document_to_retrieved_chunk(document, score=score)

        if user_groups is not None and chunk.access_level not in user_groups:
            continue

        current_source_count = source_counts.get(chunk.source, 0)
        if current_source_count >= settings.max_chunks_per_source:
            continue

        chunks.append(chunk)
        source_counts[chunk.source] = current_source_count + 1

        if len(chunks) >= settings.top_k:
            break

    return chunks
