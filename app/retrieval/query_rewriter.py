from langchain_core.messages import HumanMessage, SystemMessage

from app.memory.memory import conversation_memory
from app.prompts import PromptManager
from app.providers import get_llm


FOLLOW_UP_PREFIXES = {
    "what about",
    "and",
    "also",
    "then",
    "it",
    "that",
    "this",
    "those",
    "these",
    "same",
}


def should_rewrite(question: str) -> bool:
    normalized = question.lower().strip()

    if len(normalized.split()) <= 4:
        return True

    return any(normalized.startswith(prefix) for prefix in FOLLOW_UP_PREFIXES)


def rewrite_query(user_id: str, question: str) -> str:
    history = conversation_memory.format_history(user_id)

    if not history or not should_rewrite(question):
        return question

    prompt = PromptManager.render(
        "reformulation.md",
        history=history,
        question=question,
    )

    try:
        llm = get_llm()
        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Rewrite follow-up questions into standalone retrieval queries. "
                        "Return only the rewritten question."
                    )
                ),
                HumanMessage(content=prompt),
            ]
        )
    except Exception:
        return question

    rewritten = str(response.content).strip()
    return rewritten or question
