import os

from app.interfaces.gradio_app import demo


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        show_error=True,
    )
