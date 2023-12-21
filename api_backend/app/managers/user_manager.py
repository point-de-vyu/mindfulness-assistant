import sqlalchemy
from sqlalchemy import func
from api_backend.app.schemes.user import User, UserToCreate
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.app.utils import get_postgres_engine
import logging
from typing import Dict, List


class UserManager:
    TABLE_NAME = "users"

    def __init__(
            self,
            engine: sqlalchemy.Engine,
            logger: logging.Logger
    ):
        if not engine:
            engine = get_postgres_engine()
        self.sql_connection = engine.connect()
        metadata = sqlalchemy.MetaData()
        self.users_table = sqlalchemy.Table(UserManager.TABLE_NAME, metadata, autoload_with=self.sql_connection)
        self.logger = logger

    def add_new_user(self, user: UserToCreate):
        query = sqlalchemy.insert(self.users_table).values(
            id=func.generate_user_id(),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            date_registered=sqlalchemy.sql.functions.now()
        )
        executed_query = self.sql_connection.execute(query)
        self.sql_connection.commit()
        inserted_pkey = executed_query.inserted_primary_key
        # TODO мб как и в delete возвращать bool. Как-то унифицировать - после логгера.
        if not inserted_pkey:
            msg = ErrorMsg.FAILED_DB_RESULT
            self.logger.critical(f"{msg} adding new user")
            raise RuntimeError(msg)
        return inserted_pkey

    def get_by_id(self, id: int) -> User | None:
        return self._get_user(id=id)

    def get_by_username(self, username: str) -> User | None:
        return self._get_user(username=username)

    def _get_user(
            self,
            id: int | None = None,
            username: str | None = None
    ) -> User | None:
        def find_not_null_params() -> Dict[str, str | int]:
            column_to_val = {}
            # priority to id
            if username:
                column_to_val["username"] = username
            elif id:
                column_to_val["id"] = id
            return column_to_val

        params = find_not_null_params()
        if not params:
            return None
        query = sqlalchemy.select(self.users_table).filter_by(**params)
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchall()
        if len(rows) > 1:
            msg = ErrorMsg.ROWS_MORE_THAN_ONE
            self.logger.critical(msg)
            raise RuntimeError(msg)

        if not rows:
            return None
        # LESSON_LEARNT: trying to return row objects causes errors with fastapi decoder. Using _asdict() to get dict
        return User(**rows[0]._asdict())

    def delete_user(self, user_id: int) -> bool:
        # TODO: все удаление каскадируется, но не удалятся кастомные штуки, созданные юзером.
        #  Плюс далее будут еще их штуки: надо кастом функцию написать
        query = sqlalchemy.delete(self.users_table).where(self.users_table.c.id == user_id)
        executed_query = self.sql_connection.execute(query)
        self.sql_connection.commit()
        rowcount = executed_query.rowcount
        if rowcount != 1:
            self.logger.critical(f"Failed to delete user with {user_id}")
            return False
        return True


