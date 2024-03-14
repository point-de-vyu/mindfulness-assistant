from typing import List
import requests
import logging

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold, TextLink, as_list, as_key_value

from telegram_client.app.utils.requests import get_headers, get_base_url
from telegram_client.app.utils.types import Update
from telegram_client.app.utils.storage import extract_data_from_storage, add_data_to_storage
from telegram_client.app.schemes.sos_rituals import SosRitual

from telegram_client.app.handlers.account.sign_up import forbidden_need_signing_up
from telegram_client.app.handlers.error import error
from telegram_client.app.handlers.sos.static_data import MemoryKey, SOS_ID_REGEXP
from telegram_client.app.handlers.sos.request_wraps import get_rituals
from telegram_client.app.handlers.sos.common_handlers import no_more_rituals


router = Router()


@router.message(Command("my_rituals"))
async def get_all_user_rituals(message: Message, state: FSMContext):
    user_id = message.from_user.id
    res = await get_rituals(user_id, is_default=False, search_params={})
    if res.status_code == 401:
        await forbidden_need_signing_up(message)
        return
    if res.status_code != 200:
        logging.error(res.detail)
        await error(message)
        return
    rituals = res.data
    if not rituals:
        await message.answer(
            text="You haven't got any rituals yet! You can add some when you are in the /sos flow",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    current_ritual = rituals.pop()
    await show_ritual_full_info(rituals, current_ritual, message, state)


async def show_ritual_full_info(
        rituals: List[SosRitual],
        current_ritual: SosRitual,
        update: Update,
        state: FSMContext
):
    user_id = update.from_user.id
    message = update.message if hasattr(update, "message") else update

    await add_data_to_storage({MemoryKey.USR_AVAIL_RITUALS: rituals}, user_id, state.storage)
    button_row = [InlineKeyboardButton(
        text="Delete",
        callback_data=f"delete_sos_{current_ritual.id}"
    )]
    if rituals:
        button_row.append(InlineKeyboardButton(text="Next", callback_data="show_next_full_ritual"))
    buttons = [button_row]

    ans = [
        Bold(current_ritual.title),
        as_list(
            as_key_value("🧘Type", current_ritual.category.lower()),
            as_key_value("🤍What for", current_ritual.situation.lower()),
            as_key_value("📝Description", current_ritual.description.lower())
        )
    ]
    if current_ritual.url:
        ans.append(TextLink("Open link", url=current_ritual.url))

    await message.answer(
        text=as_list(*ans, sep="\n\n").as_html(),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@router.callback_query(F.data.regexp(rf"delete_sos_{SOS_ID_REGEXP}"))
async def delete_ritual_from_fav(callback: CallbackQuery):
    ritual_id = callback.data.split("_")[-1]
    url = f"{get_base_url(router='/sos_rituals/')}{ritual_id}"
    response = requests.delete(url=url, headers=get_headers(callback.from_user.id))
    if response.status_code == 404:
        await callback.answer(text="You already deleted this ritual!")
        return
    if response.status_code != 200:
        await error(callback.message)
        return

    # add a checkmark to the button when added, its position is hardcoded :(
    markup = callback.message.reply_markup.inline_keyboard
    markup[0][0] = InlineKeyboardButton(text="Delete ✅", callback_data=f"delete_sos_{ritual_id}")
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=markup))
    await callback.answer(text="Successfully deleted this ritual from your favourites!")


@router.callback_query(F.data == "show_next_full_ritual")
async def get_next_full_ritual(callback: CallbackQuery, state: FSMContext):
    rituals = await extract_data_from_storage(MemoryKey.USR_AVAIL_RITUALS, callback.from_user.id, state.storage)
    if not rituals:
        await no_more_rituals(callback)
        return
    current_ritual = rituals.pop()
    await show_ritual_full_info(rituals, current_ritual, callback, state)
