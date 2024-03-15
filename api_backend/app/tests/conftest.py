import os
import pytest
from fastapi.testclient import TestClient

from api_backend.app.utils.db import get_postgres_engine
from api_backend.app.schemes.sos_rituals import SosTable
import sqlalchemy
from requests import Response


def get_postgres_engine_for_testing() -> sqlalchemy.engine.Engine:
    test_db_name = os.environ["TEST_DB_NAME"]
    return get_postgres_engine(db_name=test_db_name)


class AssistantApi(TestClient):
    client_auth_token: str
    user_id: int

    """
    Added authenticated methods and DB resetting upon inition.
    This api uses default testing user.
    If necessary, each method can take different id and token
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        engine = get_postgres_engine_for_testing()
        self.client_auth_token = os.environ["TEST_CLIENT_AUTH_TOKEN"]
        with engine.connect() as connection:
            self._reset_db(connection)
            self._add_authorised_client(connection)
            self._add_default_test_user(connection)
        connection.close()

    def _get_auth_headers(self, token: str | None = None, user_id: int | None = None):
        token = token or self.client_auth_token
        user_id = str(user_id) if user_id else str(self.user_id)
        token_header = os.environ["HEADER_NAME_TOKEN"]
        id_header = os.environ["HEADER_NAME_USER_ID"]
        return {token_header: token, id_header: user_id}

    def get_with_auth(self, url: str, auth_token: str | None = None, user_id: int | None = None) -> Response:
        return self.get(url=url, headers=self._get_auth_headers(auth_token, user_id))

    def post_with_auth(
            self,
            url: str,
            content: str | None = None,
            params: dict | None = None,
            auth_token: str | None = None,
            user_id: int | None = None
    ) -> Response:
        return self.post(
            url=url,
            content=content,
            params=params,
            headers=self._get_auth_headers(auth_token, user_id),
        )

    def delete_with_auth(self, url: str, auth_token: str | None = None, user_id: int | None = None) -> Response:
        return self.delete(
            url=url,
            headers=self._get_auth_headers(auth_token, user_id),
        )

    @staticmethod
    def _reset_db(connection: sqlalchemy.Connection) -> None:
        """
        Deleting from users table will cascade to all tables where user_id is a FK.
        """
        connection.execute(sqlalchemy.text("DELETE FROM clients_users;"))
        connection.execute(sqlalchemy.text("DELETE FROM clients;"))
        connection.execute(sqlalchemy.text("DELETE FROM users;"))
        connection.execute(sqlalchemy.text(f"DELETE FROM {SosTable.RITUALS} "
                                           f"WHERE id NOT IN (SELECT id FROM {SosTable.DEFAULT_IDS});")
                           )
        connection.commit()

    def _add_authorised_client(self, connection: sqlalchemy.Connection) -> None:
        client_id = os.environ["TEST_CLIENT_ID"]
        client_type_id = os.environ["TEST_CLIENT_TYPE_ID"]
        token = self.client_auth_token
        connection.execute(sqlalchemy.text(f"INSERT INTO clients VALUES("
                                           f"{client_id}, {client_type_id}, '{token}');")
                           )

    def _add_default_test_user(self, connection: sqlalchemy.Connection) -> None:
        username = os.environ["TEST_USERNAME"]
        first_name = os.environ["TEST_FIRSTNAME"]
        last_name = os.environ["TEST_LASTNAME"]
        client_id = os.environ["TEST_CLIENT_ID"]
        user_id = os.environ["TEST_USER_ID"]
        self.user_id = int(user_id)
        connection.execute(sqlalchemy.func.add_new_user(
            username,
            first_name,
            last_name,
            client_id,
            user_id
            )
        )
        connection.commit()


@pytest.fixture(scope="session")
def api():
    from api_backend.app.main import app
    api = AssistantApi(app=app)
    # override dependency to use test DB
    app.dependency_overrides[get_postgres_engine] = get_postgres_engine_for_testing
    yield api


@pytest.fixture(scope="session")
def nonexistent_user_id() -> int:
    return 123456789


def test_read_root(api: AssistantApi) -> None:
    response = api.get("/")
    assert response.status_code == 200
