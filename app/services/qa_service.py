from app.memory.memory import conversation_memory
from app.retrieval.rag_chain import answer_question
from app.schemas import ChatRequest, ChatResponse
from app.services.intent_service import UserIntent, classify_intent
from app.services.response_service import (
    frustration_response,
    gratitude_response,
    greeting_response,
    small_talk_response,
    unclear_response,
)
from app.utils.analytics import RequestTimer, log_request_event


class QAService:
    def answer(self, request: ChatRequest) -> ChatResponse:
        with RequestTimer() as timer:
            conversation_memory.add_user_message(request.user_id, request.message)

            intent = classify_intent(request.message)

            if request.message.lower().strip() in {"clear", "/clear", "clear memory", "/clear_memory"}:
                conversation_memory.clear(request.user_id)
                response = ChatResponse(answer="Conversation memory cleared.", refused=False)

            elif intent == UserIntent.GRATITUDE:
                response = gratitude_response()

            elif intent == UserIntent.SMALL_TALK:
                normalized = request.message.lower().strip()
                if normalized in {"hi", "hello", "hey", "salam", "alsalam"}:
                    response = greeting_response()
                else:
                    response = small_talk_response()

            elif intent == UserIntent.ABUSIVE_OR_FRUSTRATED:
                response = frustration_response()

            elif intent == UserIntent.CLARIFICATION_REQUEST:
                history = conversation_memory.format_history(request.user_id)
                response = ChatResponse(
                    answer=f"Here is the recent conversation context:\n\n{history}",
                    refused=False,
                )

            elif intent == UserIntent.OUT_OF_SCOPE:
                response = unclear_response()

            else:
                response = answer_question(request)

            conversation_memory.add_assistant_message(request.user_id, response.answer)

        log_request_event(
            "qa_request_completed",
            {
                "user_id": request.user_id,
                "message": request.message,
                "intent": str(intent),
                "refused": response.refused,
                "citation_count": len(response.citations),
                "latency_ms": timer.latency_ms,
            },
        )

        return response


qa_service = QAService()
