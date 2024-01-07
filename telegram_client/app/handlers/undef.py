from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
import random


UNSUPPORTED_MEDIA = [
    "Nothing I can do with <placeholder>. Yet 😉",
    "There is nothing I can do with <placeholder> now. But one day I might!",
    "To tell you the truth, <placeholder> have never been my jam"
]

UNDEF = [
    "Sorry, I do not know what you meant there",
    "I did not understand you there, that's a fact. Hope I can make it up to you",
    "Hate to admit, but the meaning of this message is unclear to me",
    "Am I just not smart enough for this? Oh my... I need to learn harder"
]

router = Router()


@router.message(F.content_type.in_({"photo", "video", "audio", "document", "animation", "sticker"}))
async def unsupported_media(message: Message, state: FSMContext):
    content_type_pl = f"{message.content_type}s"
    ans_template = random.choice(UNSUPPORTED_MEDIA)
    ans_template = ans_template.replace("<placeholder>", content_type_pl)
    await message.answer(
        text=ans_template,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text)
async def undef_text(message: Message, state: FSMContext):
    ans = random.choice(UNDEF)
    await message.answer(
        text=ans,
        reply_markup=ReplyKeyboardRemove()
    )