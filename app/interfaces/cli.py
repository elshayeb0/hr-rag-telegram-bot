from app.schemas import ChatRequest
from app.services.qa_service import qa_service


def main() -> None:
    print("HR RAG CLI")
    print("Type 'exit' to quit.\n")

    user_id = "local-cli-user"
    user_groups = ["employee"]

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        response = qa_service.answer(
            ChatRequest(
                user_id=user_id,
                message=question,
                user_groups=user_groups,
            )
        )

        print("\nAssistant:")
        print(response.answer)
        print()


if __name__ == "__main__":
    main()
