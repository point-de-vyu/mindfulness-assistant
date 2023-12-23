import pytest
from api_backend.app.tests.conftest import AssistantApi


def test_get_sos_categories(api: AssistantApi):
    response = api.get_with_auth(url="/v1/sos_categories/")
    assert response.status_code == 200
    assert response.json()
    numb_of_cats = len(response.json())
    assert numb_of_cats == 3


def test_get_user_rituals(api: AssistantApi):
    response = api.get_with_auth(url="/v1/sos_rituals/")
    assert response.status_code == 200
    assert len(response.json()) == 0