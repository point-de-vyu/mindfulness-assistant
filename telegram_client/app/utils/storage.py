from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message
from telegram_client.app.main import memory_storage
import os
from typing import Dict, Any
import logging


async def get_storage_key(user_id: int) -> StorageKey:
    return StorageKey(
        bot_id=int(os.environ["DEBUG_BOT_ID"]),
        chat_id=user_id,
        user_id=user_id
    )


async def add_data_to_storage(data: Dict[str, Any], user_id: int, storage=memory_storage) -> None:
    storage_key = await get_storage_key(user_id)
    logging.debug(f"adding {storage_key.__repr__()}")
    await storage.update_data(key=storage_key, data=data)


async def extract_data_from_storage(key: str, user_id: int, storage=memory_storage) -> Any:
    storage_key = await get_storage_key(user_id)
    data = await storage.get_data(key=storage_key)
    logging.debug(f"extracting {storage_key.__repr__()}, {data=}")
    if key not in data:
        return ""
    return data[key]
