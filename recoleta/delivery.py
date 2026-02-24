from __future__ import annotations

import asyncio

from telegram import Bot


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
        return asyncio.run(self._send_async(text))
