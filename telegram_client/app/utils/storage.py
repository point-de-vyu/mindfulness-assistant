from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import BaseStorage
import os
from typing import Dict, Any
import logging


async def get_storage_key(user_id: int) -> StorageKey:
    return StorageKey(
        bot_id=int(os.environ["BOT_ID"]),
        chat_id=user_id,
        user_id=user_id
    )


async def add_data_to_storage(data: Dict[str, Any], user_id: int, storage: BaseStorage) -> None:
    storage_key = await get_storage_key(user_id)
    logging.debug(f"adding {storage_key.__repr__()}")
    await storage.update_data(key=storage_key, data=data)


async def extract_data_from_storage(key: str, user_id: int, storage: BaseStorage) -> Any:
    storage_key = await get_storage_key(user_id)
    data = await storage.get_data(key=storage_key)
    logging.debug(f"extracting {storage_key.__repr__()}, {data=}")
    if key not in data:
        return None
    return data[key]


async def delete_key_from_storage(key: str, user_id: int, storage: BaseStorage) -> Any:
    storage_key = await get_storage_key(user_id)
    data = await storage.get_data(key=storage_key)
    if key not in data:
        return None

    key_data = data[key]
    del data[key]
    await storage.set_data(key=storage_key, data=data)
    return key_data

