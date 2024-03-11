from aiogram.filters import Filter
from aiogram.types import Message


class AdminFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        return (
            message.from_user.id == 1047809355 and self.my_text in message.text
        )
