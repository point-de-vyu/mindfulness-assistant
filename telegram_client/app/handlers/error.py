from aiogram.types import Message
from aiogram import Router
import logging

router = Router()


async def error(message: Message, exc: Exception | None = None):
    if exc:
        logging.error(exc)
    await message.answer(text="Sorry, something went wrong. Try again later")
