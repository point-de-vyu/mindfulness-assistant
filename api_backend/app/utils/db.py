import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class Database:
    def __init__(self, name: str | None = None, echo: bool = False):
        self.engine = create_engine(
            url=self.get_db_url(name),
            echo=echo,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_session(self) -> Session:
        return self.session_factory()

    def get_session_dep(self):
        with self.session_factory() as session:
            yield session
            session.close()

    def get_db_url(self, db_name: str | None = None) -> str:
        db_endpoint, main_db_name, db_username, db_password = (
            self.get_db_connection_parameters()
        )
        db_name = db_name or main_db_name
        return (
            f"postgresql+psycopg2://{db_username}:{db_password}@{db_endpoint}/{db_name}"
        )

    @staticmethod
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


database = Database(name="example")
