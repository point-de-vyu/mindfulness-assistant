import asyncio
import os
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from telegram_client.app.handlers import start
from telegram_client.app.handlers import sign_up
from telegram_client.app.handlers.sos_ import delete_ritual
from telegram_client.app.handlers.sos_ import get_ritual
from telegram_client.app.handlers import undef

memory_storage = MemoryStorage()


async def main():
    bot = Bot(token=os.environ["DEBUG_BOT_TOKEN"])
    logging.basicConfig(level=logging.DEBUG)
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(start.router)
    dispatcher.include_router(sign_up.router)

    # dispatcher.include_router(sos.router)
    dispatcher.include_routers(delete_ritual.router, get_ritual.router)
    dispatcher.include_router(undef.router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
