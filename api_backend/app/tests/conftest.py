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
        return os.environ["TEST_USER_AUTH_TOKEN"]

    def _get_auth_headers(self, token: str | None = None):
        token = token or self._get_default_auth_token()
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
    def reset_db() -> None:
        # test_db_name = os.environ["TEST_DB_NAME"]
        # url = get_db_url(db_name=test_db_name)
        # os.system(f"yoyo apply --database {url} ./yoyo-migrations -b")
        url = "postgresql://postgres:dsfsdg@db:5432/unittest_db"
        os.system(f"yoyo reapply --database {url} ./api_backend/app/tests/yoyo-migrations -b")



def get_postgres_engine_for_testing() -> sqlalchemy.engine.Engine:
    test_db_name = os.environ["TEST_DB_NAME"]
    return get_postgres_engine(db_name=test_db_name)


# @pytest.fixture(scope="session", autouse=True)
# def reset_db() -> None:
#     test_db_name = os.environ["TEST_DB_NAME"]
#     # url = get_db_url(db_name=test_db_name)
#     url = "postgresql://postgres:dsfsdg@localhost:5432/unittest_db"
#     os.system(f"yoyo reapply --database {url} ./api_backend/app/tests/yoyo-migrations -b")


@pytest.fixture()
def api():
    from api_backend.app.main import app
    api = AssistantApi(app=app)
    # override dependency to use test DB
    app.dependency_overrides[get_postgres_engine] = get_postgres_engine_for_testing
    # use yoyo migration to reset db
    api.reset_db()
    yield api


def test_read_root(api: AssistantApi) -> None:
    response = api.get("/")
    assert response.status_code == 200
