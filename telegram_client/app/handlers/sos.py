from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
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
        buttons = [KeyboardButton(text=sit) for sit in situations]
        ans = "What are you dealing with?"
        keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True, one_time_keyboard=True)
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
        message: Message,
        is_default: bool = False,
        situation: str | None = None,
        category: str | None = None
):
    headers = get_headers(str(message.from_user.id))
    route = "sos_defaults" if is_default else "sos_rituals"
    url = f"http://{API_ENDPOINT}/{route}/"
    if situation:
        url += f"?situation={situation}"
    if category:
        url += f"?category={category}"

    response = requests.get(url=url, headers=headers)
    status_code = response.status_code

    # TODO return {code: int, res: []} - check for this code in handler and go to error from there
    if status_code != 200:
        await error(message)
        return

    rituals = response.json()
    random.shuffle(rituals)
    return rituals


@router.message(F.text.lower().in_({"anger", "anxiety", "stress"}))
async def get_rituals_for_situation(message: Message):
    situation = message.text
    await add_data_to_storage({"sos_situation": situation}, message.from_user.id)
    rituals = await get_rituals(message, situation=situation)
    buttons = [[KeyboardButton(text="Journal your feelings after this exercise")]]
    if not rituals:
        default_rituals = await get_rituals(message, is_default=True, situation=situation)
        if not default_rituals:
            await error(message)
            return
        rituals = default_rituals
        await message.answer(
            text=f"You haven't added or created your {situation.lower()} rituals. Here's my suggestion:"
        )
        buttons.append([KeyboardButton(text="Add to favourites")])
        await add_data_to_storage({"is_default_last_ritual": True}, message.from_user.id)
    # TODO вот если здесь сразу один, мы не предложим посмотреть дефолтные
    current_ritual = rituals.pop()
    available_categories = list(set([ritual["category"] for ritual in rituals]))
    buttons.extend([[KeyboardButton(text=cat) for cat in available_categories]])

    await add_data_to_storage({"current_ritual": current_ritual, "available_rituals": rituals}, message.from_user.id)
    await message.answer(
        text=f"<b>{current_ritual['title']}</b>\n\n{current_ritual['description']}\n\n{current_ritual['url']}",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    )


# TODO better names for buttons "another X"? and input understanding (now 400 for lowercase)
@router.message(F.text.lower().in_({"meditation", "affirmation", "breathing exercise"}))
async def get_ritual_for_category(message: Message):
    category = message.text
    rituals = await extract_data_from_storage("available_rituals", message.from_user.id)
    if not rituals:
        await message.answer(
            text="I'm afraid there's no more. Use the command to restart this flow",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    buttons = [
        [KeyboardButton(text="Journal your feelings after the exercise")]]

    current_ritual = [ritual for ritual in rituals if ritual["category"] == category][0]
    rituals.remove(current_ritual)
    # TODO to bool shown_defaults now is True or ""
    shown_defaults = await extract_data_from_storage("is_default_last_ritual", message.from_user.id)
    if shown_defaults:
        buttons.append([KeyboardButton(text="Add to favourites")])
    if len(rituals) == 0 and not shown_defaults:
        situation = await extract_data_from_storage("sos_situation", message.from_user.id)
        default_rituals = await get_rituals(message, is_default=True, situation=situation, category=category)
        user_rituals = await get_rituals(message, is_default=False, situation=situation, category=category)
        user_ritual_ids = [rit["id"] for rit in user_rituals]
        rituals = [rit for rit in default_rituals if rit["id"] not in user_ritual_ids]

    if rituals:
        if not shown_defaults:
            buttons.extend([[KeyboardButton(text="Show suggested rituals")]])
        else:
            available_categories = list(set([ritual["category"] for ritual in rituals]))
            buttons.extend([[KeyboardButton(text=cat) for cat in available_categories]])

    await add_data_to_storage({"current_ritual": current_ritual, "available_rituals": rituals}, message.from_user.id)
    await message.answer(
        text=f"<b>{current_ritual['title']}</b>\n\n{current_ritual['description']}\n\n{current_ritual['url']}",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    )


@router.message(F.text == "Add to favourites")
async def favourite_default_ritual(message: Message):
    user_id = message.from_user.id
    ritual = await extract_data_from_storage("current_ritual", user_id)
    if not ritual:
        await error(message)
        return
    ritual_id = ritual["id"]
    headers = get_headers(str(user_id))
    response = requests.post(
        url=f"http://{API_ENDPOINT}/default_sos_ritual/?default_ritual_id={ritual_id}",
        headers=headers
    )
    status_code = response.status_code
    if status_code == 200:
        await message.answer(
            text="Added this ritual! Next time you'll see it among the first ones",
            reply_markup=ReplyKeyboardRemove()
        )
    elif status_code == 409:
        await message.answer(text="This one is already in your favourites",
                             reply_markup=ReplyKeyboardRemove()
                             )
    else:
        await error(message)

