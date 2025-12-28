"""Lightweight OpenAI client for generating answers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict
import logging
import requests


class OpenAIError(RuntimeError):
    """Raised when the OpenAI API returns an error."""


@dataclass
class OpenAIClient:
    """Simple wrapper around the OpenAI chat completions API."""

    api_key: str
    model: str
    api_url: str

    def build_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.3) -> str:
        """Call the OpenAI API and return the assistant's reply text."""

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        try:
            response = requests.post(
                self.api_url,
                headers=self.build_headers(),
                json=payload,
                timeout=15,
            )
            response.raise_for_status()
        except requests.RequestException as exc:  # pragma: no cover - network code
            logging.exception("OpenAI request failed: %s", exc)
            raise OpenAIError("Failed to contact OpenAI API") from exc

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            logging.exception("Unexpected OpenAI response: %s", data)
            raise OpenAIError("Malformed response from OpenAI API") from exc
