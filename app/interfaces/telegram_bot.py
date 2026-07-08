from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from app.config import settings
from app.memory.memory import conversation_memory
from app.schemas import ChatRequest
from app.services.qa_service import qa_service


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi. I can answer questions from indexed company HR documents and policies."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/clear - Clear conversation memory\n\n"
        "Ask questions like:\n"
        "- What is my annual leave policy?\n"
        "- What should I do on the first day of sickness?"
    )


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    conversation_memory.clear(user_id)
    await update.message.reply_text("Conversation memory cleared.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    message = update.message.text

    response = qa_service.answer(
        ChatRequest(
            user_id=user_id,
            message=message,
            user_groups=["employee"],
        )
    )

    await update.message.reply_text(response.answer)


def main() -> None:
    if not settings.telegram_bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is required")

    app = ApplicationBuilder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
