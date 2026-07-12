import os
import secrets
from contextlib import asynccontextmanager
from typing import AsyncIterator

import gradio as gr
from fastapi import FastAPI, Header, HTTPException, Request
from telegram import Update
from telegram.ext import Application

from app.interfaces.gradio_app import demo
from app.interfaces.telegram_bot import build_telegram_application


TELEGRAM_WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL", "").strip()
TELEGRAM_WEBHOOK_SECRET = os.getenv(
    "TELEGRAM_WEBHOOK_SECRET",
    "",
).strip()

telegram_application: Application | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global telegram_application

    if not TELEGRAM_WEBHOOK_URL:
        raise RuntimeError("TELEGRAM_WEBHOOK_URL is required")

    if not TELEGRAM_WEBHOOK_SECRET:
        raise RuntimeError("TELEGRAM_WEBHOOK_SECRET is required")

    telegram_application = build_telegram_application()

    await telegram_application.initialize()
    await telegram_application.start()

    webhook_configured = await telegram_application.bot.set_webhook(
        url=TELEGRAM_WEBHOOK_URL,
        secret_token=TELEGRAM_WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=False,
    )

    if not webhook_configured:
        raise RuntimeError("Telegram rejected the webhook configuration")

    print(f"Telegram webhook configured: {TELEGRAM_WEBHOOK_URL}")

    try:
        yield
    finally:
        if telegram_application.running:
            await telegram_application.stop()

        await telegram_application.shutdown()


api = FastAPI(
    title="HR RAG Chatbot",
    lifespan=lifespan,
)


@api.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "gradio": "available",
        "telegram": (
            "running"
            if telegram_application is not None
            and telegram_application.running
            else "stopped"
        ),
    }


@api.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(
        default=None
    ),
) -> dict[str, bool]:
    if not x_telegram_bot_api_secret_token:
        raise HTTPException(
            status_code=401,
            detail="Missing Telegram webhook secret",
        )

    if not secrets.compare_digest(
        x_telegram_bot_api_secret_token,
        TELEGRAM_WEBHOOK_SECRET,
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid Telegram webhook secret",
        )

    if telegram_application is None:
        raise HTTPException(
            status_code=503,
            detail="Telegram application is not initialized",
        )

    payload = await request.json()

    update = Update.de_json(
        payload,
        telegram_application.bot,
    )

    await telegram_application.process_update(update)

    return {"ok": True}


app = gr.mount_gradio_app(
    api,
    demo,
    path="/",
)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "10000"))

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
    )