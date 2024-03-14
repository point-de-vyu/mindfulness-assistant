from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums.content_type import ContentType
import random


UNSUPPORTED_MEDIA = [
    "Nothing I can do with <placeholder>. Yet 😉",
    "There is nothing I can do with <placeholder> now. But one day I might!"
]

UNDEF = [
    "Sorry, I do not know what you meant there",
    "I did not understand you there. Hope I can make it up to you",
    "Hate to admit, but the meaning of this message is unclear to me"
]

router = Router()


@router.message(F.content_type.in_(
    {
        ContentType.ANIMATION,
        ContentType.AUDIO,
        ContentType.DOCUMENT,
        ContentType.PHOTO,
        ContentType.STICKER,
        ContentType.VIDEO
    }))
async def unsupported_media(message: Message):
    content_type_pl = f"{message.content_type}s"
    ans_template = random.choice(UNSUPPORTED_MEDIA)
    ans_template = ans_template.replace("<placeholder>", content_type_pl)
    await message.answer(
        text=ans_template,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text)
async def undef_text(message: Message):
    ans = random.choice(UNDEF)
    await message.answer(
        text=ans,
        reply_markup=ReplyKeyboardRemove()
    )