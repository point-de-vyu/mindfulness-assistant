from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from typing import Dict, List
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton,\
    InlineKeyboardButton, InlineKeyboardMarkup
from telegram_client.app.utils.requests import get_headers, get_base_url
import requests
import random
import logging
from enum import Enum
from telegram_client.app.handlers.sign_up import forbidden_need_signing_up
from telegram_client.app.handlers.error import error
from telegram_client.app.handlers.not_implemented import not_implemented
from telegram_client.app.utils.storage import extract_data_from_storage, add_data_to_storage, delete_key_from_storage
from telegram_client.app.schemes.sos_rituals import SosRitual
from telegram_client.app.utils.types import Update
from aiogram.utils.formatting import Bold, TextLink, as_list


router = Router()


SOS_ID_REGEXP = r"3\d{18}"


class MemoryKey(str, Enum):
    SOS_SITUATION = "sos_situation"
    SOS_CATEGORY = "sos_category"
    AVAIL_RITUALS = "available_rituals"
    IS_LAST_RITUAL_DEFAULT = "is_last_ritual_default"
    
    def __str__(self):
        return self.value


class SosSearchParams(str, Enum):
    SITUATION = "situation"
    CATEGORY = "category"

    def __str__(self):
        return self.value

    
async def clear_memory_vars(user_id: int):
    await delete_key_from_storage(MemoryKey.SOS_SITUATION, user_id)
    await delete_key_from_storage(MemoryKey.SOS_CATEGORY, user_id)
    await delete_key_from_storage(MemoryKey.AVAIL_RITUALS, user_id)
    await delete_key_from_storage(MemoryKey.IS_LAST_RITUAL_DEFAULT, user_id)


@router.message(Command("sos"))
async def show_sos_situations(message: Message):
    user_id = message.from_user.id
    await clear_memory_vars(user_id)
    url = get_base_url(router="sos_situations")
    response = requests.get(url=url, headers=get_headers(user_id))
    status_code = response.status_code
    if status_code == 200 and response.json():
        situations = response.json()
        buttons = [KeyboardButton(text=sit) for sit in situations]
        ans = "What are you dealing with?"
        keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True, one_time_keyboard=True)
        await message.answer(text=ans, reply_markup=keyboard)
    elif status_code == 401:
        await forbidden_need_signing_up(message)
    else:
        # LESSON_LEARNT once "auth" removed from token alias, started working
        logging.error(response.json()["detail"])
        await error(message)


async def get_rituals(update: Update, is_default: bool, search_params: Dict[str, str]) -> List[SosRitual] | None:
    message = update.message if hasattr(update, "message") else update
    route = "sos_defaults" if is_default else "sos_rituals"
    url = get_base_url(router=route)
    response = requests.get(url=url, params=search_params, headers=get_headers(update.from_user.id))
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
    params = {SosSearchParams.SITUATION: situation}
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
        MemoryKey.AVAIL_RITUALS: rituals,
        MemoryKey.SOS_SITUATION: situation,
        MemoryKey.IS_LAST_RITUAL_DEFAULT: is_default_last_ritual
    }
    await add_data_to_storage(data, message.from_user.id)
    await get_and_show_ritual(rituals, current_ritual, message)


async def no_more_rituals(callback: CallbackQuery):
    await callback.message.answer(
        text="I'm afraid there's no more. Use the /sos command to restart this flow",
        reply_markup=ReplyKeyboardRemove()
    )


@router.callback_query(F.data.lower().in_({"meditation", "affirmation", "breathing exercise"}))
async def get_ritual_for_category(callback: CallbackQuery):
    user_id = callback.from_user.id
    category = callback.data
    await add_data_to_storage({MemoryKey.SOS_CATEGORY: category}, user_id)
    rituals = await extract_data_from_storage(MemoryKey.AVAIL_RITUALS, user_id)
    if not rituals:
        await no_more_rituals(callback)
        return

    current_ritual = [ritual for ritual in rituals if ritual.category == category][0]
    rituals.remove(current_ritual)
    await get_and_show_ritual(rituals, current_ritual, callback)


async def get_and_show_ritual(rituals: List[SosRitual], current_ritual: SosRitual, update: Update):
    user_id = update.from_user.id
    message = update.message if hasattr(update, "message") else update
    current_ritual_id = current_ritual.id
    is_default_ritual = await extract_data_from_storage(MemoryKey.IS_LAST_RITUAL_DEFAULT, user_id)

    buttons = [
        [InlineKeyboardButton(
            text="Completed? Journal your experience",
            callback_data=f"journal_sos_{current_ritual_id}"
        )]]
    if is_default_ritual:
        buttons.append([InlineKeyboardButton(text="Add to favourites", callback_data=f"add_sos_{current_ritual_id}")])
    # if available USER rituals are finished, check if there are default rituals that fit params
    if len(rituals) == 0:
        if not is_default_ritual:
            situation = await extract_data_from_storage(MemoryKey.SOS_SITUATION, user_id)
            category = await extract_data_from_storage(MemoryKey.SOS_CATEGORY, user_id)
            params = {SosSearchParams.SITUATION: situation}
            if category:
                params[SosSearchParams.CATEGORY] = category
            default_rituals = await get_rituals(update, is_default=True, search_params=params)
            user_rituals = await get_rituals(update, is_default=False, search_params=params)
            rituals = [rit for rit in default_rituals if rit not in user_rituals]
            if rituals:
                buttons.extend([[InlineKeyboardButton(
                    text="Suggest more rituals",
                    callback_data="suggest_default_ritual")]]
                )
    else:
        available_categories = list(set([ritual.category for ritual in rituals]))
        buttons.extend([[InlineKeyboardButton(
            text=f"More: {cat.lower()}",
            callback_data=cat
        ) for cat in available_categories]])

    await add_data_to_storage({MemoryKey.AVAIL_RITUALS: rituals}, user_id)

    ans = [Bold(current_ritual.title), current_ritual.description]
    if current_ritual.url:
        ans.append(TextLink("Open link", url=current_ritual.url))

    await message.answer(
        text=as_list(*ans, sep="\n\n").as_html(),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@router.callback_query(F.data == "suggest_default_ritual")
async def show_suggested_ritual(callback: CallbackQuery):
    user_id = callback.from_user.id
    rituals = await extract_data_from_storage(MemoryKey.AVAIL_RITUALS, user_id)
    if not rituals:
        await no_more_rituals(callback)
        return
    current_ritual = rituals.pop()
    await add_data_to_storage({MemoryKey.IS_LAST_RITUAL_DEFAULT: True}, user_id)
    await callback.message.answer(text="Sure! Here's one:")
    await get_and_show_ritual(rituals, current_ritual, callback)


@router.callback_query(F.data.regexp(rf"add_sos_{SOS_ID_REGEXP}"))
async def add_default_ritual_to_fav(callback: CallbackQuery):
    ritual_id = callback.data.split("_")[-1]
    url = get_base_url(router="default_sos_ritual")
    response = requests.post(
        url=url,
        params={"default_ritual_id": ritual_id},
        headers=get_headers(callback.from_user.id)
    )
    status_code = response.status_code
    if status_code == 200:
        await callback.answer(
            text=f"Ritual added! Next time you'll see it among the first ones",
            reply_markup=ReplyKeyboardRemove()
        )
        # add a checkmark to the button when added, its position is hardcoded :(
        markup = callback.message.reply_markup.inline_keyboard
        markup[1] = [InlineKeyboardButton(text="Add to favourites ✅", callback_data=f"add_sos_{ritual_id}")]
        await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=markup))

    elif status_code == 409:
        await callback.answer(
            text="This one is already in your favourites",
            reply_markup=ReplyKeyboardRemove()
            )
    else:
        await error(callback.message)


@router.callback_query(F.data.regexp(rf"journal_sos_{SOS_ID_REGEXP}"))
# TODO some FSM state?
async def get_journal_entry_for_ritual(callback: CallbackQuery, state: FSMContext):
    await not_implemented(callback)
