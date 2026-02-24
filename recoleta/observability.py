from __future__ import annotations

import hashlib
import sys

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
