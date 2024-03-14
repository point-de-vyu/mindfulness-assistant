import asyncio
import os
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from telegram_client.app.handlers import start
from telegram_client.app.handlers.account import sign_up, delete_account
from telegram_client.app.handlers.sos import delete_ritual, get_ritual, journal_sos_feedback
from telegram_client.app.handlers import undef

memory_storage = MemoryStorage()


async def main():
    bot = Bot(token=os.environ["BOT_TOKEN"])
    logging.basicConfig(level=logging.DEBUG)
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(start.router)
    dispatcher.include_routers(sign_up.router, delete_account.router)
    dispatcher.include_routers(delete_ritual.router, get_ritual.router, journal_sos_feedback.router)
    dispatcher.include_router(undef.router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
