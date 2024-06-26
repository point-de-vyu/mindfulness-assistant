import os
import pytest
from fastapi.testclient import TestClient

from api_backend.app.utils.db import Database, database
from api_backend.db.models.clients import Client, ClientsUsers
from api_backend.db.models.users import User
from api_backend.db.models.sos import SosRitual, SosDefaultRitualId
import sqlalchemy
from sqlalchemy.orm import Session
from requests import Response


test_database = Database(name=os.environ["TEST_DB_NAME"])


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
        self.client_auth_token = os.environ["TEST_CLIENT_AUTH_TOKEN"]
        self.user_id = int(os.environ["TEST_USER_ID"])
        with test_database.get_session() as session:
            self.prepare_db(session)
            session.close()

    def prepare_db(self, session: Session):
        self._reset_db(session)
        self._add_authorised_client(session)
        self._add_default_test_user(session)

    def _get_auth_headers(self, token: str | None = None, user_id: int | None = None):
        token = token or self.client_auth_token
        user_id = str(user_id) if user_id else str(self.user_id)
        token_header = os.environ["HEADER_NAME_TOKEN"]
        id_header = os.environ["HEADER_NAME_USER_ID"]
        return {token_header: token, id_header: user_id}

    def get_with_auth(
        self,
        url: str,
        params: dict | None = None,
        auth_token: str | None = None,
        user_id: int | None = None,
    ) -> Response:
        return self.get(
            url=url, params=params, headers=self._get_auth_headers(auth_token, user_id)
        )

    def post_with_auth(
        self,
        url: str,
        json: dict | None = None,
        params: dict | None = None,
        auth_token: str | None = None,
        user_id: int | None = None,
    ) -> Response:
        return self.post(
            url=url,
            json=json,
            params=params,
            headers=self._get_auth_headers(auth_token, user_id),
        )

    def delete_with_auth(
        self, url: str, auth_token: str | None = None, user_id: int | None = None
    ) -> Response:
        return self.delete(
            url=url,
            headers=self._get_auth_headers(auth_token, user_id),
        )

    @staticmethod
    def _reset_db(session: Session) -> None:
        """
        Deleting from users table will cascade to all tables where user_id is a FK.
        """
        session.execute(sqlalchemy.delete(ClientsUsers))
        session.execute(sqlalchemy.delete(Client))
        session.execute(sqlalchemy.delete(User))
        session.execute(
            sqlalchemy.delete(SosRitual).where(
                SosRitual.id.notin_(sqlalchemy.select(SosDefaultRitualId.id))
            )
        )

        session.commit()

    def _add_authorised_client(self, session: Session) -> None:
        client_id = os.environ["TEST_CLIENT_ID"]
        client_type_id = os.environ["TEST_CLIENT_TYPE_ID"]
        test_client = Client(
            id=client_id, client_type_id=client_type_id, token=self.client_auth_token
        )
        session.add(test_client)
        session.commit()

    def _add_default_test_user(self, session: Session) -> None:
        username = os.environ["TEST_USERNAME"]
        first_name = os.environ["TEST_FIRSTNAME"]
        last_name = os.environ["TEST_LASTNAME"]
        client_id = os.environ["TEST_CLIENT_ID"]
        session.execute(
            sqlalchemy.func.add_new_user(
                username, first_name, last_name, client_id, self.user_id
            )
        )
        session.commit()


@pytest.fixture(scope="session")
def api():
    from api_backend.app.main import app

    api = AssistantApi(app=app)
    # override dependency to use test DB
    app.dependency_overrides[database.get_session_dep] = test_database.get_session_dep
    yield api


@pytest.fixture(scope="session")
def nonexistent_user_id() -> int:
    return 123456789


def test_read_root(api: AssistantApi) -> None:
    response = api.get("/")
    assert response.status_code == 200
