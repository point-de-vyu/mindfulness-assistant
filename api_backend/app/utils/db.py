import sqlalchemy
import os


def get_db_connection_parameters():
    # LESSON_LEARNT: use service name from compose to access other services
    endpoint = os.environ["DB_ENDPOINT"]
    main_db = os.environ["DB_NAME"]
    # LESSON_LEARNT: use docker swarm and access secrets from in-memory path
    with open("/run/secrets/db-password") as pass_f:
        password = pass_f.read()
    username = os.environ["DB_USERNAME"]
    return endpoint, main_db, username, password


def get_postgres_engine(db_name: str | None = None, is_autocommit: bool = False) -> sqlalchemy.engine.Engine:
    db_endpoint, main_db_name, db_username, db_password = get_db_connection_parameters()
    db_name = db_name or main_db_name
    engine = sqlalchemy.create_engine(
        f'postgresql+psycopg2://{db_username}:{db_password}@{db_endpoint}/{db_name}', echo=False
    )
    if is_autocommit:
        engine = engine.execution_options(autocommit=True)
    return engine





