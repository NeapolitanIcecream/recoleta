from __future__ import annotations

import hashlib
import os
import sys
from collections.abc import Iterable
from urllib.parse import quote

from loguru import logger
from rich.console import Console
from rich.text import Text


_DEFAULT_SECRET_ENV_KEYS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "HUGGINGFACE_HUB_TOKEN",
    "HF_TOKEN",
    "HUGGINGFACE_TOKEN",
    "LITELLM_API_KEY",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
)

_DEFAULT_SECRET_ENV_KEY_SUBSTRINGS = (
    "API_KEY",
    "TOKEN",
    "SECRET",
    "PASSWORD",
    "PRIVATE_KEY",
)


def collect_environment_secrets(*, extra_keys: Iterable[str] = ()) -> tuple[str, ...]:
    keys = {key.upper() for key in _DEFAULT_SECRET_ENV_KEYS}
    for key in extra_keys:
        if not isinstance(key, str):
            continue
        stripped = key.strip()
        if not stripped:
            continue
        keys.add(stripped.upper())

    collected: list[str] = []
    for key in keys:
        value = os.getenv(key, "").strip()
        if value:
            collected.append(value)

    for key, value in os.environ.items():
        if not value:
            continue
        upper = key.upper()
        if upper in keys:
            continue
        if any(token in upper for token in _DEFAULT_SECRET_ENV_KEY_SUBSTRINGS):
            candidate = str(value).strip()
            if candidate:
                collected.append(candidate)

    return tuple(dict.fromkeys(collected))


def configure_process_logging(*, level: str = "INFO", log_json: bool = False) -> None:
    logger.remove()
    normalized_level = level.upper()
    if log_json:
        logger.add(
            sys.stdout,
            level=normalized_level,
            serialize=True,
            backtrace=False,
            diagnose=False,
        )
        return

    console = Console(stderr=True)

    def rich_sink(message: object) -> None:
        message_text = str(message)
        renderable = Text.from_ansi(message_text)
        console.print(renderable, end="")

    logger.add(
        rich_sink,
        level=normalized_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra}</cyan> | "
            "<level>{message}</level>\n"
        ),
        colorize=True,
        backtrace=False,
        diagnose=False,
    )


def mask_value(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def scrub_secrets(text: str, *, secrets: Iterable[str]) -> str:
    if not text:
        return text
    sanitized = text
    for secret in secrets:
        if not secret:
            continue
        masked = mask_value(secret)
        variants = {secret, quote(secret, safe="")}
        for variant in variants:
            if variant and variant in sanitized:
                sanitized = sanitized.replace(variant, masked)
    return sanitized
