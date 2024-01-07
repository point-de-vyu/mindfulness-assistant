import json
from datetime import datetime
from typing import Any


class MockStorage:


    FILE_PATH = "./telegram_client/app/mock_storage.json"

    def _rewrite_data(self, data: dict):
        with open(MockStorage.FILE_PATH, "w") as file:
            json.dump(data, file)

    def add_user(self, user_id: int, username: str) -> None:
        user_id = str(user_id)
        with open(MockStorage.FILE_PATH) as inp:
            data = json.loads(inp.read())
        user_data = {
            "username": username,
            "date_joined": datetime.today().strftime("%Y-%m-%d %H:%M")
        }
        data[user_id] = user_data
        self._rewrite_data(data)

    def get_user(self, user_id: int):
        user_id = str(user_id)
        with open(MockStorage.FILE_PATH) as inp:
            data = json.loads(inp.read())
            if user_id in data:
                return data[user_id]
            return {}

    def update_user(self, user_id: int, key: str, val: Any):
        user_id = str(user_id)
        user = self.get_user(user_id)
        if user:
            user[key] = val

            with open(MockStorage.FILE_PATH) as inp:
                data = json.loads(inp.read())
            data[user_id] = user
            self._rewrite_data(data)

        else:
            raise ValueError("404 no user")
