"""Simple CLI to test the AI HR assistant prompt without Telegram."""

from __future__ import annotations

import argparse
import logging
from ai_hr_bot.config import Settings
from ai_hr_bot.openai_client import OpenAIClient, OpenAIError
from ai_hr_bot.prompt_builder import build_messages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the AI HR assistant via OpenAI API")
    parser.add_argument("question", help="User question to send to the assistant")
    args = parser.parse_args()

    settings = Settings.from_env()
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        api_url=settings.openai_api_url,
    )

    messages = build_messages(args.question)

    try:
        reply = client.create_chat_completion(messages)
    except OpenAIError:
        logger.exception("Failed to fetch completion")
        raise SystemExit(1)

    print(reply)


if __name__ == "__main__":
    main()
