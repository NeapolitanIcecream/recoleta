from __future__ import annotations

import asyncio
from collections.abc import Callable
from datetime import timedelta
from threading import Thread

from telegram import Bot
from telegram.error import NetworkError, RetryAfter, TimedOut
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter


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

    async def _send_async(self, text: str) -> str:
        bot = Bot(token=self.token)
        retrying = AsyncRetrying(
            retry=retry_if_exception_type((RetryAfter, TimedOut, NetworkError)),
            stop=stop_after_attempt(4),
            wait=wait_exponential_jitter(initial=0.5, max=8.0),
            reraise=True,
        )
        async for attempt in retrying:
            with attempt:
                try:
                    message = await bot.send_message(
                        chat_id=self.chat_id,
                        text=text,
                        disable_web_page_preview=True,
                    )
                    return str(message.message_id)
                except RetryAfter as exc:
                    retry_after = exc.retry_after
                    delay_seconds = retry_after.total_seconds() if isinstance(retry_after, timedelta) else float(retry_after)
                    await asyncio.sleep(delay_seconds)
                    raise
        raise RuntimeError("Failed to send message after retries")

    def send(self, text: str) -> str:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self._send_async(text))

        return _run_blocking_in_thread(lambda: asyncio.run(self._send_async(text)))
