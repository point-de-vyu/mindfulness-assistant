from typing import List
import requests
import logging

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import BaseStorage
from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.formatting import Bold, TextLink, as_list

from telegram_client.app.utils.requests import get_headers, get_base_url
from telegram_client.app.utils.storage import (
    extract_data_from_storage,
    add_data_to_storage,
    delete_key_from_storage,
)
from telegram_client.app.utils.types import Update
from telegram_client.app.schemes.sos_rituals import SosRitual

from telegram_client.app.handlers.account.sign_up import forbidden_need_signing_up
from telegram_client.app.handlers.error import error
from telegram_client.app.handlers.sos.static_data import (
    MemoryKey,
    SosSearchParams,
    SOS_ID_REGEXP,
)
from telegram_client.app.handlers.sos.request_wraps import get_rituals
from telegram_client.app.handlers.sos.common_handlers import no_more_rituals

router = Router()


async def clear_memory_vars(user_id: int, storage: BaseStorage):
    await delete_key_from_storage(MemoryKey.SOS_SITUATION, user_id, storage)
    await delete_key_from_storage(MemoryKey.SOS_CATEGORY, user_id, storage)
    await delete_key_from_storage(MemoryKey.AVAIL_RITUALS, user_id, storage)
    await delete_key_from_storage(MemoryKey.IS_LAST_RITUAL_DEFAULT, user_id, storage)


@router.message(Command("sos"))
async def show_sos_situations(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await clear_memory_vars(user_id, state.storage)
    url = get_base_url(router="sos_situations")
    response = requests.get(url=url, headers=get_headers(user_id))
    status_code = response.status_code
    if status_code == 200 and response.json():
        situations = response.json()
        buttons = [KeyboardButton(text=sit) for sit in situations]
        ans = "What are you dealing with?"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[buttons], resize_keyboard=True, one_time_keyboard=True
        )
        await message.answer(text=ans, reply_markup=keyboard)
    elif status_code == 401:
        await forbidden_need_signing_up(message)
    else:
        # LESSON_LEARNT once "auth" removed from token alias, started working
        logging.error(response.json())
        await error(message)


@router.message(F.text.lower().in_({"anger", "anxiety", "stress"}))
async def get_rituals_for_situation(message: Message, state: FSMContext):
    situation = message.text
    user_id = message.from_user.id
    params = {SosSearchParams.SITUATION: situation}
    res = await get_rituals(user_id, is_default=False, search_params=params)
    if res.status_code != 200:
        await error(message)
        return
    is_default_last_ritual = False
    if not res.data:
        res = await get_rituals(user_id, is_default=True, search_params=params)
        if res.status_code != 200 or not res.data:
            await error(message)
            return
        is_default_last_ritual = True
        await message.answer(
            text=f"You haven't added or created your {situation.lower()} rituals. Here's my suggestion:"
        )
    rituals = res.data
    current_ritual = rituals.pop()
    data = {
        MemoryKey.AVAIL_RITUALS: rituals,
        MemoryKey.SOS_SITUATION: situation,
        MemoryKey.IS_LAST_RITUAL_DEFAULT: is_default_last_ritual,
    }
    await add_data_to_storage(data, user_id, state.storage)
    await get_and_show_ritual(rituals, current_ritual, message, state)


@router.callback_query(
    F.data.lower().in_({"meditation", "affirmation", "breathing exercise"})
)
async def get_ritual_for_category(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    category = callback.data
    await add_data_to_storage(
        {MemoryKey.SOS_CATEGORY: category}, user_id, state.storage
    )
    rituals = await extract_data_from_storage(
        MemoryKey.AVAIL_RITUALS, user_id, state.storage
    )
    if not rituals:
        await no_more_rituals(callback)
        await callback.message.answer(text="Use the /sos command to restart the flow")
        return

    current_ritual = [ritual for ritual in rituals if ritual.category == category][0]
    rituals.remove(current_ritual)
    await get_and_show_ritual(rituals, current_ritual, callback, state)


async def get_and_show_ritual(
    rituals: List[SosRitual],
    current_ritual: SosRitual,
    update: Update,
    state: FSMContext,
):
    user_id = update.from_user.id
    message = update.message if hasattr(update, "message") else update
    current_ritual_id = current_ritual.id
    is_default_ritual = await extract_data_from_storage(
        MemoryKey.IS_LAST_RITUAL_DEFAULT, user_id, state.storage
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Completed? Journal your experience",
                callback_data=f"journal_sos_{current_ritual_id}",
            )
        ]
    ]
    if is_default_ritual:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Add to favourites",
                    callback_data=f"add_sos_{current_ritual_id}",
                )
            ]
        )
    # if available USER rituals are finished, check if there are default rituals that fit params
    if len(rituals) == 0:
        if not is_default_ritual:
            situation = await extract_data_from_storage(
                MemoryKey.SOS_SITUATION, user_id, state.storage
            )
            category = await extract_data_from_storage(
                MemoryKey.SOS_CATEGORY, user_id, state.storage
            )
            params = {SosSearchParams.SITUATION: situation}
            if category:
                params[SosSearchParams.CATEGORY] = category

            def_res = await get_rituals(user_id, is_default=True, search_params=params)
            user_res = await get_rituals(
                user_id, is_default=False, search_params=params
            )
            default_rituals = def_res.data
            user_rituals = user_res.data
            rituals = [rit for rit in default_rituals if rit not in user_rituals]
            if rituals:
                buttons.extend(
                    [
                        [
                            InlineKeyboardButton(
                                text="Suggest more rituals",
                                callback_data="suggest_default_ritual",
                            )
                        ]
                    ]
                )
    else:
        available_categories = list(set([ritual.category for ritual in rituals]))
        buttons.extend(
            [
                [
                    InlineKeyboardButton(text=f"More: {cat.lower()}", callback_data=cat)
                    for cat in available_categories
                ]
            ]
        )

    await add_data_to_storage(
        {MemoryKey.AVAIL_RITUALS: rituals}, user_id, state.storage
    )

    ans = [Bold(current_ritual.title), current_ritual.description]
    if current_ritual.url:
        ans.append(TextLink("Open link", url=current_ritual.url))

    await message.answer(
        text=as_list(*ans, sep="\n\n").as_html(),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )


@router.callback_query(F.data == "suggest_default_ritual")
async def show_suggested_ritual(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    rituals = await extract_data_from_storage(
        MemoryKey.AVAIL_RITUALS, user_id, state.storage
    )
    if not rituals:
        await no_more_rituals(callback)
        return
    current_ritual = rituals.pop()
    await add_data_to_storage(
        {MemoryKey.IS_LAST_RITUAL_DEFAULT: True}, user_id, state.storage
    )
    await callback.message.answer(text="Sure! Here's one:")
    await get_and_show_ritual(rituals, current_ritual, callback, state)


@router.callback_query(F.data.regexp(rf"add_sos_{SOS_ID_REGEXP}"))
async def add_default_ritual_to_fav(callback: CallbackQuery, state: FSMContext):
    ritual_id = callback.data.split("_")[-1]
    url = get_base_url(router="default_sos_ritual")
    response = requests.post(
        url=url,
        params={"default_ritual_id": ritual_id},
        headers=get_headers(callback.from_user.id),
    )
    status_code = response.status_code
    if status_code == 200:
        await callback.answer(
            text=f"Ritual added! Next time you'll see it among the first ones",
            reply_markup=ReplyKeyboardRemove(),
        )
        # add a checkmark to the button when added, its position is hardcoded :(
        markup = callback.message.reply_markup.inline_keyboard
        markup[1] = [
            InlineKeyboardButton(
                text="Add to favourites ✅", callback_data=f"add_sos_{ritual_id}"
            )
        ]
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(inline_keyboard=markup)
        )

    elif status_code == 409:
        await callback.answer(
            text="This one is already in your favourites",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await error(callback.message)
