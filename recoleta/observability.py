from __future__ import annotations

import hashlib
import sys
from collections.abc import Iterable
from urllib.parse import quote

from loguru import logger
from rich.console import Console


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

    def rich_sink(message: str) -> None:
        console.print(message, end="")

    logger.add(
        rich_sink,
        level=normalized_level,
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
