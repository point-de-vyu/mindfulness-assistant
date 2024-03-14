import requests
from telegram_client.app.handlers.error import error
from telegram_client.app.utils.requests import get_headers, get_base_url
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router = Router()


class DeleteAcc(StatesGroup):
    confirming_acc_deletion = State()


@router.message(Command("delete_account"))
async def delete_account(message: Message, state: FSMContext):
    await state.set_state(DeleteAcc.confirming_acc_deletion)
    await message.answer(
        text="I will proceed to delete your account and all of your data. Are you sure?",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Yes"), KeyboardButton(text="No")]])
    )


@router.message(F.text.lower() == "yes", DeleteAcc.confirming_acc_deletion)
async def confirmed_deleting_account(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    delete_response = requests.delete(url=get_base_url(router="users"), headers=get_headers(user_id))
    status_code = delete_response.status_code
    if status_code == 200:
        text = "Your account and all of your data has been deleted. You can delete chat history too, if you wish"
    elif status_code == 401:
        text = "Don't worry, your account has been deleted for good"
    else:
        await error(message)
        return
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


@router.message(F.text.lower() == "no", DeleteAcc.confirming_acc_deletion)
async def refused_deleting_account(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="I'm glad you'll stay ☺️", reply_markup=ReplyKeyboardRemove())
