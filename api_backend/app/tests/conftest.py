import os
import pytest
from fastapi.testclient import TestClient

from api_backend.app.utils.db import get_postgres_engine
import sqlalchemy
from requests import Response


class AssistantApi(TestClient):
    auth_token: str

    """
    Added authenticated methods. This api uses default testing token.
    If necessary, each method can take a different auth_token
    """

    def _get_default_auth_token(self):
        return os.environ["UNITTEST_USER_AUTH_TOKEN"]

    def _get_auth_headers(self, token: str | None = None):
        token = token or self._get_default_auth_token()
        return {"Authorization": token}

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


def get_postgres_engine_for_testing(db_name: str | None = None, is_autocommit: bool = False) -> sqlalchemy.engine.Engine:
    test_db_name = os.environ["TEST_DB_NAME"]
    return get_postgres_engine(db_name=test_db_name)


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
