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


async def get_postgres_session(db_name: str | None = None) -> Session:
    db_endpoint, main_db_name, db_username, db_password = get_db_connection_parameters()
    db_name = db_name or main_db_name
    engine = create_engine(get_db_url(db_name), echo=False)

    session_factory = sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async with session_factory() as session:
        yield session
        await session.close()


# class Database:
#     def __init__(self, name: str | None = None, echo: bool = False):
#         self.engine = create_async_engine(
#             url=get_db_url(name),
#             echo=echo,
#         )
#         self.session_factory = async_sessionmaker(
#             bind=self.engine,
#             autoflush=False,
#             autocommit=False,
#             expire_on_commit=False,
#         )
#
#     # def get_scoped_session(self):
#     #     session = async_scoped_session(
#     #         session_factory=self.session_factory,
#     #         scopefunc=current_task,
#     #     )
#     #     return session
#
#     async def get_session(self) -> AsyncSession:
#         async with self.session_factory() as session:
#             yield session
#             await session.close()
#
#     # async def scoped_session_dependency(self) -> AsyncSession:
#     #     session = self.get_scoped_session()
#     #     yield session
#     #     await session.close()
#
#
# db_helper = Database()
