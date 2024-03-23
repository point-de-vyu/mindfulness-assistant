import secrets
import sqlalchemy
import os
from fastapi import Depends
from fastapi import Header
from api_backend.app.utils.db import Database
from api_backend.app.utils.error_raisers import raise_401_error
from api_backend.db.models.clients import Clients, ClientsUsers
from api_backend.db.models.users import Users
from sqlalchemy.orm import Session
import logging


def generate_token() -> str:
    return secrets.token_hex()


def client_authentication(
    token: str = Header(alias=os.environ["HEADER_NAME_TOKEN"]),
    db_session: Session = Depends(Database.get_session_dep),
) -> int:

    # table = sqlalchemy.Table("clients", sqlalchemy.MetaData(), autoload_with=conn)
    # executed_q = conn.execute(sqlalchemy.select(table.c.id).filter_by(token=token))
    # executed_q = db_session.execute(
    #     sqlalchemy.text(f"SELECT id from clients WHERE token = '{token}';")
    # )
    executed_q = db_session.execute(sqlalchemy.select(Clients.id).filter_by(token=token))
    client_id = executed_q.scalar()
    if not client_id:
        logging.critical(f"failed {token=}")
        raise_401_error()
    return client_id


def authentication(
    user_id_from_client: str = Header(alias=os.environ["HEADER_NAME_USER_ID"]),
    token: str = Header(alias=os.environ["HEADER_NAME_TOKEN"]),
    db_session: Session = Depends(Database.get_session_dep),
) -> int:
    user_id_from_client = int(user_id_from_client)
    client_id = client_authentication(token, db_session)
    # table = sqlalchemy.Table("clients_users", sqlalchemy.MetaData(), autoload_with=conn)
    # executed_q = conn.execute(
    #     sqlalchemy.select(table.c.user_id).filter_by(
    #         client_id=client_id, user_id_from_client=user_id_from_client
    #     )
    # )
    # executed_q = db_session.execute(
    #     sqlalchemy.text(
    #         f"SELECT user_id FROM clients_users "
    #         f"WHERE client_id='{client_id}' AND "
    #         f"user_id_from_client='{user_id_from_client}';"
    #     )
    # )
    executed_q = db_session.execute(
        sqlalchemy.select(ClientsUsers.user_id).filter_by(
            client_id=client_id, user_id_from_client=user_id_from_client
        )
    )
    user_id = executed_q.scalar()
    if not user_id:
        logging.critical(f"failed id {user_id_from_client=}")
        raise_401_error()
    return user_id
