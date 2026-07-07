from langchain_core.messages import HumanMessage, SystemMessage

from app.prompts import PromptManager
from app.providers import get_llm
from app.retrieval.citations import build_citations, format_citations
from app.retrieval.retriever import retrieve_chunks
from app.schemas import ChatRequest, ChatResponse
from app.utils.model_errors import model_error_response


def _format_context(chunks) -> str:
    if not chunks:
        return ""

    context_blocks = []

    for index, chunk in enumerate(chunks, start=1):
        context_blocks.append(
            f"[Context {index}: source={chunk.source}, chunk_id={chunk.chunk_id}]\n{chunk.text}"
        )

    return "\n\n".join(context_blocks)


def answer_question(request: ChatRequest) -> ChatResponse:
    chunks = retrieve_chunks(
        query=request.message,
        user_groups=request.user_groups,
    )

    citations = build_citations(chunks)

    if not chunks:
        return ChatResponse(
            answer=PromptManager.refusal_message(),
            citations=[],
            retrieved_chunks=[],
            refused=True,
        )

    context = _format_context(chunks)

    prompt = PromptManager.answer_prompt(
        question=request.message,
        context=context,
    )

    llm = get_llm()
    try:
        response = llm.invoke(
            [
                SystemMessage(content=PromptManager.system_prompt()),
                HumanMessage(content=prompt),
            ]
        )
    except Exception as error:
        return model_error_response(error)

    answer = str(response.content).strip()

    source_block = format_citations(citations)
    if source_block:
        answer = f"{answer}\n\n{source_block}"

    refused = "I do not have enough information from the official company documents" in answer

    return ChatResponse(
        answer=answer,
        citations=citations,
        retrieved_chunks=chunks,
        used_external_knowledge=False,
        refused=refused,
    )
