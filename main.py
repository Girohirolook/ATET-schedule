import asyncio
import logging
import os
import sys

from aiogram import Bot
from aiogram import Dispatcher

from handlers import main_hadler
from middlewares.authorization import AuthorizationMiddleware
from middlewares.messages_counter import MessageCounter
from utils.funcs import update_dates, update_menu

bot = Bot(token=os.getenv("TOKEN"), parse_mode="HTML")


async def main():
    dp = Dispatcher()
    dp.message.middleware(MessageCounter())
    dp.message.middleware(AuthorizationMiddleware())
    dp.callback_query.middleware(MessageCounter())
    dp.callback_query.middleware(AuthorizationMiddleware())
    dp.include_routers(main_hadler.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        loop = asyncio.get_event_loop()
        coros = []
        coros.append(update_dates())
        coros.append(update_menu())
        coros.append(main())
        loop.run_until_complete(asyncio.gather(*coros))
        # asyncio.run(update_dates())
        # asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")
