import sqlalchemy
import random
import time
from api_backend.app.schemes.user import User
from api_backend.app.utils import get_postgres_engine


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
        user_id = self._generate_user_id()
        query = sqlalchemy.insert(self.users_table).values(
            id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            date_registered=sqlalchemy.sql.functions.now()
        )
        executed_query = self.sql_connection.execute(query)
        self.sql_connection.commit()
        return executed_query.inserted_primary_key

    @staticmethod
    def _generate_user_id() -> int:
        # 64-bit signed int ID (BIGINT in SQL). The first decimal digit is the ID type.
        # The Second, the third anfloor(random() * 99999999)d the fourth decimal digits are ID subtype
        # Next 5 digits are random int
        # Then the 32-bit timestamp
        return 1000000000000000000 + random.randint(0, 99999) * 10000000000 + int(time.time())

    def get_users(self):
        # res = self.sql_connection.execute(sqlalchemy.text(f"SELECT * FROM users"))
        query = sqlalchemy.select(self.users_table)
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchall()
        # LESSON_LEARNT: trying to return row objects causes errors with fastapi decoder. Using _asdict() to get dict
        result_dicts = [row._asdict() for row in rows]
        return result_dicts

    def get_user_by_username(self, username: str):
        query = sqlalchemy.select(self.users_table).where(self.users_table.c.username == username)
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchmany()
        if len(rows) > 1:
            raise RuntimeError(f"found {len(rows)} rows")
        result_dicts = [row._asdict() for row in rows]
        return result_dicts
