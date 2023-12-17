import sqlalchemy

from fastapi import HTTPException
from fastapi import status


def get_db_connection_parameters():
    # LESSON_LEARNT: use service name from compose to access other services
    endpoint = "db:5432"
    main_db = "example"
    # LESSON_LEARNT: use docker swarm and access secrets from in-memory path
    with open("/run/secrets/db-password") as pass_f:
        password = pass_f.read()
    username = "postgres"
    return endpoint, main_db, username, password


def get_postgres_engine(db_name: str | None = None, is_autocommit: bool = False) -> sqlalchemy.engine.Engine:
    db_endpoint, main_db_name, db_username, db_password = get_db_connection_parameters()
    db_name = db_name or main_db_name
    engine = sqlalchemy.create_engine(
        f'postgresql+psycopg2://{db_username}:{db_password}@{db_endpoint}/{db_name}', echo=True
    )
    if is_autocommit:
        engine = engine.execution_options(autocommit=True)
    return engine


def raise_404_error(msg: str = "Not found") -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=msg
    )


def raise_400_error(msg: str = "Invalid parameter") -> None:
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
    )