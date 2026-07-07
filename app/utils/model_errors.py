from app.retrieval.citations import format_citations
from app.schemas import ChatResponse, Citation


def model_error_response(error: Exception, citations: list[Citation] | None = None) -> ChatResponse:
    message = str(error)
    source_block = format_citations(citations or [])

    if "RESOURCE_EXHAUSTED" in message or "429" in message:
        answer = (
            "The AI model quota is temporarily exhausted, so I cannot generate a full answer right now. "
            "However, retrieval is working and the relevant sources were found."
        )

        if source_block:
            answer = f"{answer}\n\n{source_block}"

        return ChatResponse(
            answer=answer,
            citations=citations or [],
            refused=True,
        )

    answer = "The AI model failed while generating the answer. Check logs and retry."

    if source_block:
        answer = f"{answer}\n\n{source_block}"

    return ChatResponse(
        answer=answer,
        citations=citations or [],
        refused=True,
    )
