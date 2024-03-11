import datetime
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

last_date = datetime.date.today()
messages_count = 0


def return_message_count():
    return messages_count


def count_message():
    global last_date, messages_count
    date = datetime.date.today()
    if date != last_date:
        last_date = date
        messages_count = 0
    messages_count += 1


class MessageCounter(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        count_message()
        return await handler(event, data)
