import sqlalchemy
from sqlalchemy import func
from api_backend.app.schemes.user import User
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.app.utils import get_postgres_engine
import logging
from typing import Dict, List


class UserManager:
    TABLE_NAME = "users"

    def __init__(self, sql_connection: sqlalchemy.Connection | None = None):
        if not sql_connection:
            engine = get_postgres_engine()
            sql_connection = engine.connect()
        self.sql_connection = sql_connection
        metadata = sqlalchemy.MetaData()
        self.users_table = sqlalchemy.Table(UserManager.TABLE_NAME, metadata, autoload_with=self.sql_connection)

    def add_new_user(self, user: User):
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
        if not inserted_pkey:
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT_500)
        return inserted_pkey

    def get_user_by_username(self, username: str):
        query = sqlalchemy.select(self.users_table).where(self.users_table.c.username == username)
        executed_query = self.sql_connection.execute(query)

        rows = executed_query.fetchmany()
        if not rows:
            raise ValueError(ErrorMsg.USER_NOT_FOUND_404)
        if len(rows) > 1:
            raise RuntimeError(ErrorMsg.ROWS_MORE_THAN_ONE_500)
        # LESSON_LEARNT: trying to return row objects causes errors with fastapi decoder. Using _asdict() to get dict
        result = [User(**row._asdict()) for row in rows]
        return result

    def get_users(
            self,
            id: int | None = None,
            username: str | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            date_registered: str | None = None
    ) -> List[User]:
        def find_not_null_params() -> Dict[str, str | int]:
            column_to_val = {}
            if id:
                column_to_val["id"] = id
            if username:
                column_to_val["username"] = username
            if first_name:
                column_to_val["first_name"] = first_name
            if last_name:
                column_to_val["last_name"] = last_name
            if date_registered:
                column_to_val["date_registered"] = date_registered
            return column_to_val

        params = find_not_null_params()
        # logging.log(level=0, msg=params)
        query = sqlalchemy.select(self.users_table)
        if params:
            query = query.filter_by(**params)
        executed_query = self.sql_connection.execute(query)
        # will need caution with fetchall for q with no params if loads of users
        rows = executed_query.fetchall()
        result_dicts = [User(**row._asdict()) for row in rows]
        return result_dicts
