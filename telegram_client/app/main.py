import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from telegram_client.app.handlers import start


async def main():
    bot = Bot(token=os.environ["DEBUG_BOT_TOKEN"])
    logging.basicConfig(level=logging.DEBUG)
    dispatcher = Dispatcher()
    dispatcher.include_router(start.router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())