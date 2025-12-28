"""Configuration helpers for the AI HR bot."""

from dataclasses import dataclass
import os


@dataclass
class Settings:
    """Runtime settings loaded from environment variables."""

    telegram_bot_token: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_api_url: str = "https://api.openai.com/v1/chat/completions"

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables."""

        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_model = os.getenv("OPENAI_MODEL", cls.openai_model)
        openai_api_url = os.getenv("OPENAI_API_URL", cls.openai_api_url)

        if not telegram_bot_token:
            raise ValueError("Environment variable TELEGRAM_BOT_TOKEN is required.")
        if not openai_api_key:
            raise ValueError("Environment variable OPENAI_API_KEY is required.")

        return cls(
            telegram_bot_token=telegram_bot_token,
            openai_api_key=openai_api_key,
            openai_model=openai_model,
            openai_api_url=openai_api_url,
        )
