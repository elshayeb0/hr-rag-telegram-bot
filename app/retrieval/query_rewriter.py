from langchain_core.messages import HumanMessage, SystemMessage

from app.memory.memory import conversation_memory
from app.prompts import PromptManager
from app.providers import get_llm


def rewrite_query(user_id: str, question: str) -> str:
    history = conversation_memory.format_history(user_id)

    if not history:
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
