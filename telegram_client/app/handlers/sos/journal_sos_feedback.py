import requests
import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from telegram_client.app.utils.requests import get_headers, get_base_url
from telegram_client.app.utils.storage import (
    add_data_to_storage,
    delete_key_from_storage,
)
from telegram_client.app.handlers.sos.static_data import MemoryKey, SOS_ID_REGEXP
from telegram_client.app.handlers.error import error
from aiogram.fsm.state import State, StatesGroup


router = Router()


class Journaling(StatesGroup):
    is_journaling = State()


@router.callback_query(F.data.regexp(rf"journal_sos_{SOS_ID_REGEXP}"))
async def get_journal_entry_for_ritual(callback: CallbackQuery, state: FSMContext):
    ritual_id = callback.data.split("_")[-1]
    await add_data_to_storage(
        {MemoryKey.CURRENT_RITUAL: ritual_id}, callback.from_user.id, state.storage
    )
    await state.set_state(Journaling.is_journaling)
    await callback.message.answer(
        text="This is an invitation to reflect on this experience:\n- how does your body feel?\n- your mind?"
        "\nYou can also journal any associations, or anything at all"
    )
    await callback.message.answer(
        text="If you changed your mind about journaling, please write 'cancel' or 'quit'",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(
    F.text.lower().in_({"cancel", "quit", "exit", "no", "nah"}),
    Journaling.is_journaling,
)
async def refused_journaling(message: Message, state: FSMContext):
    await delete_key_from_storage(
        MemoryKey.CURRENT_RITUAL, message.from_user.id, state.storage
    )
    await message.answer(text="As you wish! Hope you'll do it next time")


@router.message(F.text, Journaling.is_journaling)
async def save_journal_entry(message: Message, state: FSMContext):
    user_id = message.from_user.id
    ritual_id = await delete_key_from_storage(
        MemoryKey.CURRENT_RITUAL, user_id, state.storage
    )
    params = {"ritual_id": ritual_id, "feedback": message.text}
    response = requests.post(
        url=get_base_url(router="sos_feedback"),
        params=params,
        headers=get_headers(user_id),
    )
    if response.status_code != 200:
        await error(message)
        return
    await message.answer(text="Keep up the good mindful work ☀️")
