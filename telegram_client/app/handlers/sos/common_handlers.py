from aiogram.types import CallbackQuery, ReplyKeyboardRemove


async def no_more_rituals(callback: CallbackQuery):
    await callback.message.answer(
        text="There's no more rituals to show",
        reply_markup=ReplyKeyboardRemove()
    )