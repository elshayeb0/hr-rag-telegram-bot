import asyncio

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.config import settings
from app.memory.memory import conversation_memory
from app.schemas import ChatRequest
from app.services.qa_service import qa_service


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    await update.message.reply_text(
        "Hi. I can answer questions from indexed company HR documents "
        "and policies."
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    await update.message.reply_text(
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/clear - Clear conversation memory\n\n"
        "Ask questions like:\n"
        "- What is the sickness absence policy?\n"
        "- What should I do on the first day of sickness?"
    )


async def clear_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None or update.effective_user is None:
        return

    user_id = str(update.effective_user.id)
    conversation_memory.clear(user_id)

    await update.message.reply_text("Conversation memory cleared.")


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if (
        update.message is None
        or update.message.text is None
        or update.effective_user is None
    ):
        return

    user_id = str(update.effective_user.id)
    message = update.message.text.strip()

    if not message:
        await update.message.reply_text("Please enter an HR question.")
        return

    await update.message.chat.send_action(ChatAction.TYPING)

    try:
        response = await asyncio.to_thread(
            qa_service.answer,
            ChatRequest(
                user_id=user_id,
                message=message,
                user_groups=["employee"],
            ),
        )
    except Exception as error:
        print(f"Telegram request failed: {error}")
        await update.message.reply_text(
            "I could not process that request. Please try again shortly."
        )
        return

    await update.message.reply_text(response.answer)


def build_telegram_application() -> Application:
    if not settings.telegram_bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is required")

    application = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    return application


def main() -> None:
    application = build_telegram_application()

    print("Telegram bot is running in polling mode...")
    application.run_polling()


if __name__ == "__main__":
    main()