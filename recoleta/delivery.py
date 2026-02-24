from __future__ import annotations

import asyncio
from collections.abc import Callable
from threading import Thread

from telegram import Bot


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
        message = await bot.send_message(
            chat_id=self.chat_id,
            text=text,
            disable_web_page_preview=True,
        )
        return str(message.message_id)

    def send(self, text: str) -> str:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self._send_async(text))

        return _run_blocking_in_thread(lambda: asyncio.run(self._send_async(text)))
