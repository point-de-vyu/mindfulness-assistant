from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from typing import Dict, List
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton,\
    InlineKeyboardButton, InlineKeyboardMarkup
from telegram_client.app.utils.requests import get_headers
import requests
import os
import random
import logging
from telegram_client.app.handlers.sign_up import forbidden_need_signing_up
from telegram_client.app.handlers.error import error
from telegram_client.app.handlers.not_implemented import not_implemented
from telegram_client.app.utils.storage import extract_data_from_storage, add_data_to_storage
from telegram_client.app.schemes.sos_rituals import SosRitual
from telegram_client.app.utils.types import Update


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
        update: Update,
        is_default: bool,
        search_params: Dict[str, str]
) -> List[SosRitual] | None:
    user_id = update.from_user.id
    message = update.message if hasattr(update, "message") else update
    headers = get_headers(str(user_id))
    route = "sos_defaults" if is_default else "sos_rituals"
    url = f"http://{API_ENDPOINT}/{route}/?"
    if not search_params:
        await error(message)
        return
    # if "situation" in search_params:
    #     url += f"?situation={search_params['situation']}"
    # if "category" in search_params:
    #     url += f"?category={search_params['category']}"
    str_params = []
    for key in search_params:
        str_params.append(f"{key}={search_params[key]}")
    url += "&".join(str_params)

    response = requests.get(url=url, headers=headers)
    status_code = response.status_code

    # TODO return {code: int, res: []} - check for this code in handler and go to error from there
    if status_code != 200:
        await error(message)
        return

    rituals = [SosRitual(**rit) for rit in response.json()]
    random.shuffle(rituals)
    return rituals


@router.message(F.text.lower().in_({"anger", "anxiety", "stress"}))
async def get_rituals_for_situation(message: Message):
    situation = message.text
    params = {"situation": situation}
    rituals = await get_rituals(message, is_default=False, search_params=params)
    is_default_last_ritual = False
    if not rituals:
        default_rituals = await get_rituals(message, is_default=True, search_params=params)
        if not default_rituals:
            await error(message)
            return
        rituals = default_rituals
        is_default_last_ritual = True
        await message.answer(
            text=f"You haven't added or created your {situation.lower()} rituals. Here's my suggestion:"
        )

    current_ritual = rituals.pop()
    data = {
        "available_rituals": rituals,
        "sos_situation": situation,
        "is_default_last_ritual": is_default_last_ritual
    }
    logging.debug(f"{current_ritual=}, {rituals=}")
    await add_data_to_storage(data, message.from_user.id)
    await get_and_show_ritual(
        rituals,
        current_ritual,
        message
    )


async def no_more_rituals(callback: CallbackQuery):
    await callback.message.answer(
        text="I'm afraid there's no more. Use the /sos command to restart this flow",
        reply_markup=ReplyKeyboardRemove()
    )


@router.callback_query(F.data.lower().in_({"meditation", "affirmation", "breathing exercise"}))
async def get_ritual_for_category(callback: CallbackQuery):
    user_id = callback.from_user.id
    category = callback.data
    await add_data_to_storage({"sos_category": category}, user_id)
    rituals = await extract_data_from_storage("available_rituals", user_id)
    if not rituals:
        await no_more_rituals(callback)
        return

    current_ritual = [ritual for ritual in rituals if ritual.category == category][0]
    rituals.remove(current_ritual)
    await get_and_show_ritual(
        rituals,
        current_ritual,
        callback
    )


async def get_and_show_ritual(
        rituals: List[SosRitual],
        current_ritual: SosRitual,
        update: Update
):
    user_id = update.from_user.id
    message = update.message if hasattr(update, "message") else update
    current_ritual_id = current_ritual.id
    is_default_ritual = await extract_data_from_storage("is_default_last_ritual", user_id)

    buttons = [
        [InlineKeyboardButton(
            text="Journal your feelings after the exercise",
            callback_data=f"journal_sos_{current_ritual_id}"
        )]]
    if is_default_ritual:
        buttons.append([InlineKeyboardButton(text="Add to favourites", callback_data=f"add_sos_{current_ritual_id}")])
    # if avail USER rituals are finished
    # check if there are default rituals that fit params
    if len(rituals) == 0:
        if not is_default_ritual:
            situation = await extract_data_from_storage("sos_situation", user_id)
            category = await extract_data_from_storage("sos_category", user_id)
            params = {
                "situation": situation
            }
            if category:
                params["category"] = category
            default_rituals = await get_rituals(update, is_default=True, search_params=params)
            user_rituals = await get_rituals(update, is_default=False, search_params=params)
            user_ritual_ids = [rit.id for rit in user_rituals]
            rituals = [rit for rit in default_rituals if rit.id not in user_ritual_ids]
            if rituals:
                buttons.extend([[InlineKeyboardButton(text="Suggest more rituals",
                                                  callback_data="suggest_default_ritual")]])
    else:
        available_categories = list(set([ritual.category for ritual in rituals]))
        buttons.extend([[InlineKeyboardButton(
            text=f"More: {cat}",
            callback_data=cat
        ) for cat in available_categories]])

    await add_data_to_storage({"current_ritual": current_ritual, "available_rituals": rituals}, user_id)
    await message.answer(
        text=f"<b>{current_ritual.title}</b>\n\n{current_ritual.description}\n\n{current_ritual.url}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@router.callback_query(F.data == "suggest_default_ritual")
async def show_suggested_ritual(callback: CallbackQuery):
    user_id = callback.from_user.id
    rituals = await extract_data_from_storage("available_rituals", user_id)
    if not rituals:
        await no_more_rituals(callback)
        return
    current_ritual = rituals.pop()
    await add_data_to_storage({"is_default_last_ritual": True}, user_id)
    await callback.message.answer(text="Sure! Here's one:")
    await get_and_show_ritual(
        rituals,
        current_ritual,
        callback
    )


@router.callback_query(F.data.regexp(r"add_sos_3\d{18}"))
async def add_default_ritual_to_fav(callback: CallbackQuery):
    user_id = callback.from_user.id
    ritual_id = callback.data.split("_")[-1]
    headers = get_headers(str(user_id))
    response = requests.post(
        url=f"http://{API_ENDPOINT}/default_sos_ritual/?default_ritual_id={ritual_id}",
        headers=headers
    )
    status_code = response.status_code
    if status_code == 200:
        await callback.answer(
            text=f"Added this ritual {ritual_id=}! Next time you'll see it among the first ones",
            reply_markup=ReplyKeyboardRemove()
        )
    elif status_code == 409:
        await callback.answer(
            text="This one is already in your favourites",
            reply_markup=ReplyKeyboardRemove()
            )
    else:
        await error(callback.message)


@router.callback_query(F.data.regexp(r"journal_sos_3\d{18}"))
# TODO some FSM state?
async def get_journal_entry_for_ritual(callback: CallbackQuery, state: FSMContext):
    await not_implemented(callback)
