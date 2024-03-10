from telegram_client.app.utils.types import Update


async def not_implemented(update: Update):
    message = update.message if hasattr(update, "message") else update
    await message.answer(text="Sorry, this piece is yet to be implemented")