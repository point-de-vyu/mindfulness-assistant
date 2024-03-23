import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_db_connection_parameters():
    # LESSON_LEARNT: use service name from compose to access other services
    endpoint = os.environ["DB_ENDPOINT"]
    main_db = os.environ["DB_NAME"]
    # LESSON_LEARNT: use docker swarm and access secrets from in-memory path
    # with open("/run/secrets/db-password") as pass_f:
    #     password = pass_f.read()
    username = os.environ["DB_USERNAME"]
    password = os.environ["DB_SECRET_PASSWORD"]
    return endpoint, main_db, username, password


def get_db_url(db_name: str | None = None) -> str:
    db_endpoint, main_db_name, db_username, db_password = get_db_connection_parameters()
    db_name = db_name or main_db_name
    # db_name = "example"
    return f"postgresql+psycopg2://{db_username}:{db_password}@{db_endpoint}/{db_name}"


class Database:
    # def __init__(self, name: str | None = None, echo: bool = False):
    #     pass
    #     # self.engine = create_engine(
    #     #     url=get_db_url(name),
    #     #     echo=echo,
    #     # )
    #     # self.session_factory = sessionmaker(
    #     #     bind=self.engine,
    #     #     autoflush=False,
    #     #     autocommit=False,
    #     #     expire_on_commit=False,
    #     # )

    @staticmethod
    def get_session_factory(db_name: str | None = None, echo: bool = False):
        engine = create_engine(
            url=get_db_url(db_name),
            echo=echo,
        )
        return sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @staticmethod
    def get_session() -> Session:
        factory = Database.get_session_factory()
        session = factory()
        return session

    @staticmethod
    def get_session_dep():
        factory = Database.get_session_factory()
        with factory() as session:
            yield session
            session.close()

    @staticmethod
    def get_test_session() -> Session:
        factory = Database.get_session_factory(db_name=os.environ["TEST_DB_NAME"])
        session = factory()
        return session

    @staticmethod
    def get_test_session_dep():
        factory = Database.get_session_factory(db_name=os.environ["TEST_DB_NAME"])
        with factory() as session:
            yield session
            session.close()