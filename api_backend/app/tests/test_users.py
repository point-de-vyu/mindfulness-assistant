import pytest
from api_backend.app.tests.conftest import AssistantApi
from api_backend.app.schemes.user import UserToCreate
from api_backend.app.schemes.user import User


@pytest.fixture()
def user_to_create():
    return UserToCreate(
        username="@007",
        first_name="James",
        last_name="Bond"
    )


def test_add_and_delete_user(api: AssistantApi, user_to_create: UserToCreate) -> None:
    url = "/v1/users/"
    # post new user
    post_response = api.post(url, content=user_to_create.model_dump_json())
    assert post_response.status_code == 200
    assert post_response.json()
    user_token = list(post_response.json().values())[0]
    assert user_token
    # check user by getting them
    get_response = api.get_with_auth(url, auth_token=user_token)
    assert get_response.status_code == 200
    assert get_response.json()
    created_user = User(**get_response.json())
    assert user_to_create.username == created_user.username
    assert user_to_create.first_name == created_user.first_name
    assert user_to_create.last_name == created_user.last_name
    # delete the user
    deletion_response = api.delete_with_auth(url, auth_token=user_token)
    assert deletion_response.status_code == 200
    get_response_after_deletion = api.get_with_auth(url, auth_token=user_token)
    assert get_response_after_deletion.status_code == 401


