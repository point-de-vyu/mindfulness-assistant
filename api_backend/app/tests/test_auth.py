import pytest
import os
from api_backend.app.tests.conftest import AssistantApi


@pytest.fixture()
def unauthorized_client_token() -> str:
    return "nhjkehbuhgelknvjevnklsb"


def test_unauth_request(api: AssistantApi) -> None:
    response = api.get(url="/v1/sos_categories/")
    assert response.status_code == 422


def test_no_token_header(api: AssistantApi) -> None:
    user_id = os.environ["TEST_USER_ID"]
    id_header = os.environ["HEADER_NAME_USER_ID"]
    response = api.get(url="/v1/sos_categories/", headers={id_header: user_id})
    assert response.status_code == 422


def test_no_id_header(api: AssistantApi) -> None:
    client_token = os.environ["TEST_CLIENT_AUTH_TOKEN"]
    token_header = os.environ["HEADER_NAME_TOKEN"]
    response = api.get(url="/v1/sos_categories/", headers={token_header: client_token})
    assert response.status_code == 422


def test_unauthorized_client_token(api: AssistantApi, unauthorized_client_token: str) -> None:
    response = api.get_with_auth(url="/v1/sos_categories/", auth_token=unauthorized_client_token)
    assert response.status_code == 401


def test_unauthorised_user(api: AssistantApi, nonexistent_user_id: int) -> None:
    response = api.get_with_auth(url="/v1/sos_categories/", user_id=nonexistent_user_id)
    assert response.status_code == 401
