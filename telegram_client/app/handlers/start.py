from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command("start"))
async def greet_on_start(message: Message, state: FSMContext):
    user = message.from_user
    name = user.first_name
    username = user.username
    greeting_text = f"Hello {name if name else username}. Glad to meet you!"
    function_text = f"You can see the commands I can perform in the menu. Remember that" \
                    f"I'm work in progress and hopefully I'll grow big and cool. I'll do my best to help you."
    await message.answer(
        text=greeting_text,
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=function_text
    )