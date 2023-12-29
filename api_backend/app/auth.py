import secrets
import sqlalchemy
from fastapi import Depends
from fastapi import Header
from api_backend.app.utils.db import get_postgres_engine
from api_backend.app.utils.error_raisers import raise_401_error


def generate_token() -> str:
    return secrets.token_hex()


def get_user_id_by_token(
        # todo подумать об имени либо другой способ
        token: str = Header(alias="assist-auth"),
        db_engine: sqlalchemy.Engine = Depends(get_postgres_engine)
) -> int:
    conn = db_engine.connect()
    table = sqlalchemy.Table("user_tokens", sqlalchemy.MetaData(), autoload_with=conn)
    executed_q = conn.execute(sqlalchemy.select(table.c.user_id).filter_by(token=token))
    user_id = executed_q.scalar()
    if not user_id:
        raise_401_error()
    return user_id
