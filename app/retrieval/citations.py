from app.schemas import Citation, RetrievedChunk


def build_citations(chunks: list[RetrievedChunk]) -> list[Citation]:
    seen: set[str] = set()
    citations: list[Citation] = []

    for chunk in chunks:
        citation = chunk.to_citation()
        key = citation.chunk_id or citation.format()

        if key in seen:
            continue

        seen.add(key)
        citations.append(citation)

    return citations


def format_citations(citations: list[Citation]) -> str:
    if not citations:
        return ""

    lines = ["Sources:"]

    for index, citation in enumerate(citations, start=1):
        lines.append(citation.format(index=index))

    return "\n".join(lines)
