from app.schemas import ChatResponse


def small_talk_response() -> ChatResponse:
    return ChatResponse(
        answer="I'm good. Ask me anything about your company policies, leave rules, HR procedures, or indexed documents.",
        refused=False,
    )


def greeting_response() -> ChatResponse:
    return ChatResponse(
        answer="Hi. I can help you find answers from company HR documents, policies, and procedures.",
        refused=False,
    )


def gratitude_response() -> ChatResponse:
    return ChatResponse(
        answer="You're welcome.",
        refused=False,
    )


def frustration_response() -> ChatResponse:
    return ChatResponse(
        answer="Fair criticism. Right now I’m still limited to indexed HR documents. Ask me a policy question and I’ll retrieve the relevant source.",
        refused=False,
    )


def unclear_response() -> ChatResponse:
    return ChatResponse(
        answer="I can help with company HR documents. Try asking about annual leave, sick leave, approvals, employee policies, or document summaries.",
        refused=True,
    )


def memory_not_ready_response() -> ChatResponse:
    return ChatResponse(
        answer="I cannot track the previous conversation yet. Conversation memory is the next feature we need to implement.",
        refused=True,
    )
