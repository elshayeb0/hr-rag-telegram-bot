from app.schemas import ChatResponse


def model_error_response(error: Exception) -> ChatResponse:
    message = str(error)

    if "RESOURCE_EXHAUSTED" in message or "429" in message:
        return ChatResponse(
            answer=(
                "The AI model quota is temporarily exhausted. Retrieval is working, "
                "but generation cannot run right now. Try again later or switch to another model/provider."
            ),
            refused=True,
        )

    return ChatResponse(
        answer="The AI model failed while generating the answer. Check logs and retry.",
        refused=True,
    )
