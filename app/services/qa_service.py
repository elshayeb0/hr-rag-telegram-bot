from app.retrieval.rag_chain import answer_question
from app.schemas import ChatRequest, ChatResponse


class QAService:
    def answer(self, request: ChatRequest) -> ChatResponse:
        return answer_question(request)


qa_service = QAService()
