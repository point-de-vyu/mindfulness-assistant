from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram_client.app.utils.requests import get_headers
import requests
import os
import json

router = Router()


@router.message(Command("sos"))
async def show_sos_situations(message: Message, state: FSMContext):
    endpoint = os.environ["API_ENDPOINT"]
    url = f"http://{endpoint}/sos_situations/"
    user = message.from_user
    user_id = str(user.id)
    headers = get_headers(user_id)
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        situations = response.json()
        ans = "What are you dealing with?"
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=sit)] for sit in situations])
    else:
        # LESSON_LEARNT once "auth" removed from token alias, started working
        print(response.json()["detail"])
        det = json.dumps(response.json())
        ans = f"Sorry, smth went wrong: {det}"
        keyboard = ReplyKeyboardRemove()
    await message.answer(
        text=ans,
        reply_markup=keyboard
    )