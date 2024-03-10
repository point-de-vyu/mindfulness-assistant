import requests
import logging
from telegram_client.app.handlers.error import error
from telegram_client.app.utils.requests import get_headers, get_base_url
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup


router = Router()


@router.callback_query(F.data == "sign_up")
async def sign_up(callback: CallbackQuery):
    user = callback.from_user
    new_user = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "id_from_client": user.id
    }
    url = get_base_url(router="users")
    headers = get_headers(callback.from_user.id)
    response = requests.post(url=url, headers=headers, json=new_user)
    status_code = response.status_code
    if status_code == 200:
        text = "You are registered!"
    elif status_code == 409:
        text = "You are already registered, no need to do that again :)"
    else:
        await error(callback.message)

    await callback.message.answer(text=text)


async def explain_signing_up(message: Message):
    text1 = "If you are ready to give me a try, please sign up." \
           "\n\nTo be transparent, after you click the button, I will store some of your personal info, " \
           "such as your id, name and username."
    text2 = "If you are ok with that, press the button and let's begin the journey!"
    await message.answer(text=text1)
    await message.answer(
        text=text2,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Sign up", callback_data="sign_up")]]
        )
    )


async def forbidden_need_signing_up(message: Message):
    text = "Sorry, you can only use me if you've signed up. It is very simple though!"
    await message.answer(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Sign up", callback_data="sign_up")]]
        )
    )
