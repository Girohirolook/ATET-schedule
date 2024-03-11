from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from utils.funcs import read_ids
from utils.funcs import write_ids


class AuthorizationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data1 = read_ids()
        ids = [i[0] for i in data1]
        if str(event.from_user.id) not in ids:
            data1.append([str(event.from_user.id), "1"])
            write_ids(data1)
            # with open("files/ids.txt", mode="w") as f:
            #     f.write("\n".join([" ".join(i) for i in data1]))
        return await handler(event, data)
