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
    auth_token: str

    """
    Added authenticated methods and DB resetting upon inition.
    This api uses default testing user.
    If necessary, each method can take a different auth_token
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        engine = get_postgres_engine_for_testing()
        with engine.connect() as connection:
            self._reset_db(connection)
            self._add_default_test_user(connection)
        connection.close()

    def _get_auth_headers(self, token: str | None = None):
        token = token or self.auth_token
        return {"assist-auth": token}

    def get_with_auth(self, url: str, auth_token: str | None = None) -> Response:
        return self.get(url=url, headers=self._get_auth_headers(auth_token))

    def post_with_auth(self, url: str, json: dict | None = None, auth_token: str | None = None) -> Response:
        return self.post(
            url=url,
            json=json,
            headers=self._get_auth_headers(auth_token),
        )

    def delete_with_auth(self, url: str, auth_token: str | None = None) -> Response:
        return self.delete(
            url=url,
            headers=self._get_auth_headers(auth_token),
        )

    @staticmethod
    def _reset_db(connection: sqlalchemy.Connection) -> None:
        """
        Deleting from users table will cascade to all tables where user_id is a FK.
        """
        connection.execute(sqlalchemy.text("DELETE FROM users;"))
        connection.execute(sqlalchemy.text(f"DELETE FROM {SosTable.RITUALS} "
                                           f"WHERE id NOT IN (SELECT id FROM {SosTable.DEFAULT_IDS});")
                           )
        connection.commit()

    def _add_default_test_user(self, connection: sqlalchemy.Connection) -> None:
        username = os.environ["TEST_USERNAME"]
        first_name = os.environ["TEST_FIRSTNAME"]
        last_name = os.environ["TEST_LASTNAME"]
        token = os.environ["TEST_USER_AUTH_TOKEN"]
        connection.execute(sqlalchemy.func.add_new_user(
            username,
            first_name,
            last_name,
            token
            )
        )
        connection.commit()
        self.auth_token = token


@pytest.fixture()
def api():
    from api_backend.app.main import app
    api = AssistantApi(app=app)
    # override dependency to use test DB
    app.dependency_overrides[get_postgres_engine] = get_postgres_engine_for_testing
    yield api


def test_read_root(api: AssistantApi) -> None:
    response = api.get("/")
    assert response.status_code == 200
