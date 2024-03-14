import pytest
from api_backend.app.tests.conftest import AssistantApi
from api_backend.app.schemes.user import UserToCreate
from api_backend.app.schemes.user import User


@pytest.fixture()
def user_to_create():
    return UserToCreate(
        username="@007",
        first_name="James",
        last_name="Bond",
        id_from_client=1007
    )


def test_add_and_delete_user(api: AssistantApi, user_to_create: UserToCreate) -> None:
    url = "/v1/users/"
    # post new user
    user_id = user_to_create.id_from_client
    post_response = api.post_with_auth(url, user_id=user_id, content=user_to_create.model_dump_json())
    assert post_response.status_code == 200
    # check user by getting them
    get_response = api.get_with_auth(url, user_id=user_id)
    assert get_response.status_code == 200
    assert get_response.json()
    created_user = User(**get_response.json())
    assert user_to_create.username == created_user.username
    assert user_to_create.first_name == created_user.first_name
    assert user_to_create.last_name == created_user.last_name
    # delete the user
    deletion_response = api.delete_with_auth(url, user_id=user_id)
    assert deletion_response.status_code == 200
    get_response_after_deletion = api.get_with_auth(url, user_id=user_id)
    assert get_response_after_deletion.status_code == 401


def test_delete_nonexistent_user(api: AssistantApi) -> None:
    url = "/v1/users/"
    # since we authenticate user by id, a nonexistent user is an anauthenticated user
    delete_response = api.delete_with_auth(url=url, user_id=38072345)
    assert delete_response.status_code == 401
