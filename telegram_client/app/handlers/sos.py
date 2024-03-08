from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram_client.app.utils.requests import get_headers
import requests
import os
import json
import random
import logging
from telegram_client.app.handlers.sign_up import forbidden_need_signing_up
from telegram_client.app.handlers.error import error
from telegram_client.app.utils.storage import extract_data_from_storage, add_data_to_storage

router = Router()
API_ENDPOINT = os.environ["API_ENDPOINT"]


@router.message(Command("sos"))
async def show_sos_situations(message: Message):
    url = f"http://{API_ENDPOINT}/sos_situations/"
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


async def get_rituals(
        callback: CallbackQuery,
        is_default: bool = False,
        situation: str | None = None,
        category: str | None = None
):
    headers = get_headers(str(callback.from_user.id))
    route = "sos_defaults" if is_default else "sos_rituals"
    url = f"http://{API_ENDPOINT}/{route}/"
    if situation:
        url += f"?situation={situation}"
    if category:
        url += f"?category={category}"

    response = requests.get(url=url, headers=headers)
    status_code = response.status_code

    if status_code != 200:
        await error(callback.message)
        return

    rituals = response.json()
    random.shuffle(rituals)
    return rituals


@router.callback_query(F.data.lower().in_({"anger", "anxiety", "stress"}))
async def get_rituals_for_situation(callback: CallbackQuery):
    situation = callback.data
    await add_data_to_storage({"sos_situation": situation}, callback.from_user.id)
    rituals = await get_rituals(callback, situation=situation)
    buttons = [[InlineKeyboardButton(text="Journal you feelings after the exercise", callback_data="journal_after_sos")]]
    if not rituals:
        default_rituals = await get_rituals(callback, is_default=True, situation=situation)
        if not default_rituals:
            await error(callback.message)
            return
        rituals = default_rituals
        await callback.message.answer(
            text=f"You haven't added or created your {situation.lower()} rituals. Here's my suggestion"
        )
        buttons.append([InlineKeyboardButton(text="Add to favourites", callback_data="add_ritual_to_fav")])
    current_ritual = rituals.pop()
    available_categories = list(set([ritual["category"] for ritual in rituals]))
    buttons.extend([[InlineKeyboardButton(text=cat, callback_data=cat) for cat in available_categories]])

    await add_data_to_storage({"current_ritual": current_ritual, "available_rituals": rituals}, callback.from_user.id)
    await callback.message.answer(
        text=f"<b>{current_ritual['title']}</b>\n\n{current_ritual['description']}\n\n{current_ritual['url']}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
