import gradio as gr

from app.memory.memory import conversation_memory
from app.schemas import ChatRequest
from app.services.qa_service import qa_service


USER_ID = "gradio-local-user"


def answer(message: str) -> str:
    try:
        response = qa_service.answer(
            ChatRequest(
                user_id=USER_ID,
                message=message,
                user_groups=["employee"],
            )
        )
    except Exception as error:
        if "RESOURCE_EXHAUSTED" in str(error) or "429" in str(error):
            return (
                "Embedding or model quota is currently exhausted. "
                "The Gradio UI is working, but RAG retrieval cannot run until quota resets."
            )
        return f"Application error:\n{error}"

    debug = (
        "\n\n---\n"
        f"Refused: {response.refused}\n"
        f"Citations: {[citation.model_dump() for citation in response.citations]}\n"
        f"Retrieved chunks: "
        f"{[{'source': c.source, 'chunk_id': c.chunk_id, 'score': c.score, 'section_heading': c.section_heading} for c in response.retrieved_chunks]}"
    )

    return response.answer + debug


def clear_memory() -> str:
    conversation_memory.clear(USER_ID)
    return "Memory cleared."


with gr.Blocks(title="HR RAG Debug UI") as demo:
    gr.Markdown("# HR RAG Debug UI")
    gr.Markdown("Local debug interface for testing retrieval, citations, refusal behavior, and answer quality.")

    question = gr.Textbox(label="Question", placeholder="Ask about HR policies...")
    answer_box = gr.Textbox(label="Answer + Debug", lines=18)

    with gr.Row():
        ask_button = gr.Button("Ask", variant="primary")
        clear_button = gr.Button("Clear Memory")

    ask_button.click(answer, inputs=question, outputs=answer_box)
    question.submit(answer, inputs=question, outputs=answer_box)
    clear_button.click(clear_memory, inputs=[], outputs=answer_box)


if __name__ == "__main__":
    demo.launch()
