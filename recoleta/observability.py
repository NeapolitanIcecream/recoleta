from __future__ import annotations

import hashlib
import logging
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
    "RECOLETA_LLM_API_KEY",
    "RECOLETA_RESEND_API_KEY",
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
    keys = _normalized_secret_keys(extra_keys=extra_keys)
    collected = _collect_explicit_secret_values(keys=keys)
    collected.extend(_collect_discovered_secret_values(keys=keys))
    return tuple(dict.fromkeys(collected))


def _normalized_secret_keys(*, extra_keys: Iterable[str]) -> tuple[str, ...]:
    keys: list[str] = [key.upper() for key in _DEFAULT_SECRET_ENV_KEYS]
    for key in extra_keys:
        if not isinstance(key, str):
            continue
        stripped = key.strip()
        if stripped:
            keys.append(stripped.upper())
    return tuple(dict.fromkeys(keys))


def _collect_explicit_secret_values(*, keys: tuple[str, ...]) -> list[str]:
    values: list[str] = []
    for key in keys:
        value = os.getenv(key, "").strip()
        if value:
            values.append(value)
    return values


def _collect_discovered_secret_values(*, keys: tuple[str, ...]) -> list[str]:
    explicit_keys = set(keys)
    values: list[str] = []
    for key, value in os.environ.items():
        if not value:
            continue
        upper = key.upper()
        if upper in explicit_keys:
            continue
        if any(token in upper for token in _DEFAULT_SECRET_ENV_KEY_SUBSTRINGS):
            candidate = str(value).strip()
            if candidate:
                values.append(candidate)
    return values


def _stream_supports_ansi(stream: object) -> bool:
    isatty = getattr(stream, "isatty", None)
    if not callable(isatty) or not isatty():
        return False

    fileno = getattr(stream, "fileno", None)
    if not callable(fileno):
        return False

    try:
        fileno()
    except Exception:
        return False

    return True


_RICH_CONSOLE: Console | None = None


def get_rich_console() -> Console:
    """Return a shared Console used for both logs and progress rendering."""

    global _RICH_CONSOLE
    if _RICH_CONSOLE is not None:
        current_file = getattr(_RICH_CONSOLE, "file", None)
        if current_file is sys.stderr and not bool(
            getattr(current_file, "closed", False)
        ):
            return _RICH_CONSOLE
        _RICH_CONSOLE = None

    if _RICH_CONSOLE is not None:
        return _RICH_CONSOLE

    enable_ansi = _stream_supports_ansi(sys.stderr)
    _RICH_CONSOLE = Console(
        file=sys.stderr,
        stderr=True,
        no_color=not enable_ansi,
        force_terminal=enable_ansi,
    )
    return _RICH_CONSOLE


class _InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except Exception:
            level = record.levelno

        logger.bind(logger_name=record.name).opt(
            exception=record.exc_info,
            depth=6,
        ).log(level, record.getMessage())


def configure_process_logging(*, level: str = "INFO", log_json: bool = False) -> None:
    logger.remove()
    normalized_level = level.upper()

    # Route stdlib logging (e.g. surya) through loguru.
    logging.captureWarnings(True)
    root_logger = logging.getLogger()
    root_logger.handlers = [_InterceptHandler()]
    stdlib_level = getattr(logging, normalized_level, logging.INFO)
    root_logger.setLevel(stdlib_level)
    for candidate in logging.root.manager.loggerDict.values():
        if isinstance(candidate, logging.Logger):
            candidate.handlers = []
            candidate.propagate = True

    if log_json:
        logger.add(
            sys.stdout,
            level=normalized_level,
            serialize=True,
            backtrace=False,
            diagnose=False,
        )
        return

    def rich_sink(message: object) -> None:
        message_text = str(message)
        renderable = Text.from_ansi(message_text)
        get_rich_console().print(renderable, end="")

    logger.add(
        rich_sink,
        level=normalized_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra}</cyan> | "
            "<level>{message}</level>\n"
        ),
        colorize=not get_rich_console().no_color,
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
