from __future__ import annotations

import asyncio
from collections.abc import Callable
from datetime import timedelta
from threading import Thread
from typing import Any, cast

from telegram import Bot, InputFile
from telegram.constants import ParseMode
from telegram.error import NetworkError, RetryAfter, TimedOut
from tenacity import (
    AsyncRetrying,
    Retrying,
    RetryCallState,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)
from tenacity.wait import wait_base

try:
    import resend
    from resend.exceptions import ResendError as _ImportedResendError
except Exception:  # noqa: BLE001
    resend = None

    class _FallbackResendError(Exception):
        code: int | None = None
        error_type: str | None = None

    _RESEND_ERROR_TYPE: type[BaseException] = _FallbackResendError
else:
    _RESEND_ERROR_TYPE = _ImportedResendError


def _run_blocking_in_thread(fn: Callable[[], str]) -> str:
    result: str | None = None
    error: BaseException | None = None

    def _runner() -> None:
        nonlocal result, error
        try:
            result = fn()
        except BaseException as exc:
            error = exc

    thread = Thread(target=_runner, daemon=True)
    thread.start()
    thread.join()

    if error is not None:
        raise error
    if result is None:
        raise RuntimeError("Thread runner returned no result")
    return result


class TelegramSender:
    def __init__(self, *, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id

    def _retrying(self) -> AsyncRetrying:
        class _TelegramWait(wait_base):
            def __init__(self) -> None:
                self._fallback = wait_exponential_jitter(initial=0.5, max=8.0)

            def __call__(self, retry_state: RetryCallState) -> float:
                if retry_state.outcome is None:
                    return self._fallback(retry_state)
                exc = retry_state.outcome.exception()
                if not isinstance(exc, RetryAfter):
                    return self._fallback(retry_state)

                retry_after = exc.retry_after
                try:
                    if isinstance(retry_after, timedelta):
                        return max(0.0, retry_after.total_seconds())
                    return max(0.0, float(retry_after))
                except Exception:
                    return self._fallback(retry_state)

        return AsyncRetrying(
            retry=retry_if_exception_type((RetryAfter, TimedOut, NetworkError)),
            stop=stop_after_attempt(4),
            wait=_TelegramWait(),
            reraise=True,
        )

    async def _send_async(self, text: str) -> str:
        bot = Bot(token=self.token)
        async for attempt in self._retrying():
            with attempt:
                message = await bot.send_message(
                    chat_id=self.chat_id,
                    text=text,
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.HTML,
                )
                return str(message.message_id)
        raise RuntimeError("Failed to send message after retries")

    async def _send_document_async(
        self,
        *,
        filename: str,
        content: bytes,
        caption: str | None = None,
    ) -> str:
        bot = Bot(token=self.token)
        document = InputFile(content, filename=filename)
        async for attempt in self._retrying():
            with attempt:
                message = await bot.send_document(
                    chat_id=self.chat_id,
                    document=document,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    disable_content_type_detection=True,
                )
                return str(message.message_id)
        raise RuntimeError("Failed to send document after retries")

    def send(self, text: str) -> str:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self._send_async(text))

        return _run_blocking_in_thread(lambda: asyncio.run(self._send_async(text)))

    def send_document(
        self,
        *,
        filename: str,
        content: bytes,
        caption: str | None = None,
    ) -> str:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(
                self._send_document_async(
                    filename=filename,
                    content=content,
                    caption=caption,
                )
            )

        return _run_blocking_in_thread(
            lambda: asyncio.run(
                self._send_document_async(
                    filename=filename,
                    content=content,
                    caption=caption,
                )
            )
        )


def _is_retryable_resend_error(exc: BaseException) -> bool:
    if not isinstance(exc, _RESEND_ERROR_TYPE):
        return False
    try:
        code = int(getattr(exc, "code", 0) or 0)
    except Exception:
        code = 0
    error_type = str(getattr(exc, "error_type", "") or "").strip()
    return code == 429 or code >= 500 or error_type == "HttpClientError"


def _normalize_resend_error_message(error: Any) -> str:
    if isinstance(error, dict):
        for key in ("message", "error", "name"):
            normalized = str(error.get(key) or "").strip()
            if normalized:
                return normalized
        return str(error)
    normalized = str(error or "").strip()
    return normalized or "unknown resend error"


class ResendBatchSender:
    def __init__(self, *, api_key: str) -> None:
        self.api_key = str(api_key or "").strip()
        if not self.api_key:
            raise ValueError("Resend API key is required")

    def _retrying(self) -> Retrying:
        return Retrying(
            retry=retry_if_exception(_is_retryable_resend_error),
            stop=stop_after_attempt(4),
            wait=wait_exponential_jitter(initial=0.5, max=8.0),
            reraise=True,
        )

    def send_batch(
        self,
        *,
        emails: list[dict[str, object]],
        idempotency_key: str,
    ) -> list[dict[str, str | None]]:
        if resend is None:
            raise RuntimeError(
                "Resend transport requires the 'resend' package to be installed"
            )
        resend.api_key = self.api_key
        prepared_emails = [dict(email) for email in emails]
        response: Any | None = None
        for attempt in self._retrying():
            with attempt:
                response = resend.Batch.send(
                    cast(Any, prepared_emails),
                    cast(
                        Any,
                        {
                            "idempotency_key": str(idempotency_key),
                        },
                    ),
                )
        if response is None:
            raise RuntimeError("Resend batch send returned no response")

        response_data = list(getattr(response, "data", None) or [])
        response_errors = list(getattr(response, "errors", None) or [])
        error_by_index: dict[int, str] = {}
        for position, raw_error in enumerate(response_errors):
            if not raw_error:
                continue
            raw_index: Any | None = None
            if isinstance(raw_error, dict):
                raw_index = raw_error.get("index")
            else:
                raw_index = getattr(raw_error, "index", None)
            target_index = position
            if raw_index is None:
                normalized_index = None
            else:
                try:
                    normalized_index = int(raw_index)
                except (TypeError, ValueError):
                    normalized_index = None
            if normalized_index is not None and normalized_index >= 0:
                target_index = normalized_index
            error_by_index[target_index] = _normalize_resend_error_message(raw_error)
        outcomes: list[dict[str, str | None]] = []
        for index, email in enumerate(prepared_emails):
            message_id: str | None = None
            error: str | None = None
            if index in error_by_index:
                error = error_by_index[index]
            elif index < len(response_data):
                raw_id = None
                result = response_data[index]
                if isinstance(result, dict):
                    raw_id = result.get("id") or result.get("Id")
                else:
                    raw_id = getattr(result, "id", None)
                normalized_id = str(raw_id or "").strip()
                if normalized_id:
                    message_id = normalized_id
                else:
                    error = "missing provider message id"
            else:
                error = "missing provider batch result"
            outcomes.append(
                {
                    "destination": str(email.get("to") or "").strip() or None,
                    "message_id": message_id,
                    "error": error,
                }
            )
        return outcomes
