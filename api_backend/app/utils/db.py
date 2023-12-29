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


def get_db_url(db_name: str | None = None) -> str:
    db_endpoint, main_db_name, db_username, db_password = get_db_connection_parameters()
    db_name = db_name or main_db_name
    return f"postgresql+psycopg2://{db_username}:{db_password}@{db_endpoint}/{db_name}"


def get_postgres_engine(db_name: str | None = None) -> sqlalchemy.engine.Engine:
    db_endpoint, main_db_name, db_username, db_password = get_db_connection_parameters()
    db_name = db_name or main_db_name
    engine = sqlalchemy.create_engine(get_db_url(db_name), echo=False)
    return engine





