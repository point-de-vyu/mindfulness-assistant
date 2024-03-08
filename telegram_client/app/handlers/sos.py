from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram_client.app.utils.requests import get_headers
import requests
import os
import json
import logging
from telegram_client.app.handlers.sign_up import forbidden_need_signing_up
from telegram_client.app.handlers.error import error

router = Router()


@router.message(Command("sos"))
async def show_sos_situations(message: Message, state: FSMContext):
    endpoint = os.environ["API_ENDPOINT"]
    url = f"http://{endpoint}/sos_situations/"
    user = message.from_user
    user_id = str(user.id)
    headers = get_headers(user_id)
    response = requests.get(url=url, headers=headers)
    status_code = response.status_code
    if status_code == 200:
        situations = response.json()
        buttons = [InlineKeyboardButton(text=sit, callback_data=sit) for sit in situations]
        ans = "What are you dealing with?"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
        await message.answer(
            text=ans,
            reply_markup=keyboard
        )
    elif status_code == 401:
        await forbidden_need_signing_up(message)
    else:
        # LESSON_LEARNT once "auth" removed from token alias, started working
        logging.error(response.json()["detail"])
        await error(message)


@router.callback_query(F.data.lower().in_({"anger", "anxiety", "stress"}))
async def get_rituals_for_situation(callback: CallbackQuery):
    await callback.message.answer(text=f"You chose {callback.data}")
