from aiogram.types import Message
from aiogram import Router

router = Router()


async def error(message: Message):
    await message.answer(text="Sorry, something went wrong. Try again later")
