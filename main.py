import asyncio
import os
import logging
import sys

from aiogram import Bot
from aiogram import Dispatcher

from handlers import main_hadler
from utils.funcs import update_dates

bot = Bot(
    token=os.getenv("TOKEN"), parse_mode="HTML"
)


async def main():
    dp = Dispatcher()
    dp.include_routers(main_hadler.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        loop = asyncio.get_event_loop()
        coros = []
        coros.append(update_dates())
        coros.append(main())
        loop.run_until_complete(asyncio.gather(*coros))
        # asyncio.run(update_dates())
        # asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")
