"""Telegram bot entrypoint for the AI HR assistant."""

from __future__ import annotations
import logging
from typing import NoReturn

from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from ai_hr_bot.config import Settings
from ai_hr_bot.openai_client import OpenAIClient, OpenAIError
from ai_hr_bot.prompt_builder import build_messages

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet the user when they send /start."""

    await update.message.reply_text(
        "Здравствуйте! Я бот отдела кадров. Задайте мне вопрос, и я подскажу, к кому обратиться."
    )


def build_application(settings: Settings) -> Application:
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        api_url=settings.openai_api_url,
    )

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message is None or not update.message.text:
            return

        user_text = update.message.text.strip()
        messages = build_messages(user_text)

        try:
            reply_text = client.create_chat_completion(messages)
        except OpenAIError:
            await update.message.reply_text("Не удалось получить ответ от ассистента. Попробуйте позже.")
            return

        await update.message.reply_text(reply_text)

    application = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token)
        .concurrent_updates(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return application


def run_bot(settings: Settings) -> NoReturn:
    """Start polling and keep the bot running."""

    application = build_application(settings)
    application.run_polling()


def main() -> None:
    settings = Settings.from_env()

    logger.info("Starting bot with model %s", settings.openai_model)
    run_bot(settings)


if __name__ == "__main__":
    main()
