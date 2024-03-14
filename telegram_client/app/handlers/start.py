from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from telegram_client.app.handlers.sign_up import explain_signing_up

import logging


router = Router()


@router.message(Command("start"))
async def greet_on_start(message: Message):
    user = message.from_user
    name = user.first_name
    username = user.username
    greeting = f"Hello {name if name else username}. Glad to meet you!"
    intro = f"I'm designed to help you with your mindfulness and mental health."
    await message.answer(text=greeting)
    await message.answer(text=intro)
    await skills(message)


async def skills(message: Message):
    text1 = "At the moment, you can call a /sos command if you feel overwhelmed, and I'll offer you an exercise to " \
           "try to deal with your feelings."
    await message.answer(text=text1)
    await explain_signing_up(message)
