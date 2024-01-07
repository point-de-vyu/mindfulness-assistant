from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
import random

router = Router()


@router.message(Command("start"))
async def greet_on_start(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    name = user.first_name
    username = user.username
    # TODO make real storage
    existing_user = random.choice([True, False])
    if existing_user:
        greeting_text = f"Hello {name if name else username}. Good to see you again!"
        function_text = "No need to press start anymore. You can use the menu to navigate ;)"
    else:
        greeting_text = f"Hello {name if name else username}. Glad to meet you!"
        function_text = f"You can see the commands I can perform in the menu. Remember that " \
                        f"I'm work in progress and hopefully I'll grow big and cool. I'll do my best to help you."
    await message.answer(
        text=greeting_text,
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=function_text
    )