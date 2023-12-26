import pytest
from api_backend.app.tests.conftest import AssistantApi
import random

param_category = "category"
param_situation = "situation"
param_combo = f"{param_category}, {param_situation}"
ok_categories = ["Meditation", "Affirmation", "Breathing exercise"]
ok_situations = ["Stress", "Anxiety", "Anger"]
bad_categories = ["Miditatio", "Affid wation", "Bsing exeddrcse"]
bad_situations = ["Sres", "Axieti", "Angerrrr"]
ok_combos = [
    (random.choice(ok_categories), random.choice(ok_situations)),
    (random.choice(ok_categories), random.choice(ok_situations)),
    (random.choice(ok_categories), random.choice(ok_situations))
]
bad_combos = [
    (random.choice(bad_categories), random.choice(bad_situations)),
    (random.choice(ok_categories), random.choice(bad_situations)),
    (random.choice(bad_categories), random.choice(ok_situations))
]


def test_get_sos_categories(api: AssistantApi) -> None:
    response = api.get_with_auth(url="/v1/sos_categories/")
    assert response.status_code == 200
    assert response.json()


def test_get_sos_situations(api: AssistantApi) -> None:
    response = api.get_with_auth(url="/v1/sos_situations/")
    assert response.status_code == 200
    assert response.json()


def test_get_test_user_rituals(api: AssistantApi) -> None:
    response = api.get_with_auth(url="/v1/sos_rituals/")
    assert response.status_code == 200
    # TODO add rituals
    assert len(response.json()) == 0


def test_get_all_default_rituals(api: AssistantApi) -> None:
    response = api.get_with_auth(url="/v1/sos_defaults/")
    assert response.status_code == 200


@pytest.mark.parametrize(param_category, ok_categories)
def test_get_default_rituals_with_correct_category(api: AssistantApi, category: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_defaults/?category={category}")
    assert response.status_code == 200


@pytest.mark.parametrize(param_category, bad_categories)
def test_get_default_rituals_with_wrong_category(api: AssistantApi, category: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_defaults/?category={category}")
    assert response.status_code == 400


@pytest.mark.parametrize(param_situation, ok_situations)
def test_get_default_rituals_with_correct_situation(api: AssistantApi, situation: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_defaults/?situation={situation}")
    assert response.status_code == 200


@pytest.mark.parametrize(param_situation, bad_situations)
def test_get_default_rituals_with_wrong_situation(api: AssistantApi, situation: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_defaults/?situation={situation}")
    assert response.status_code == 400


@pytest.mark.parametrize(param_combo, ok_combos)
def test_get_default_rituals_with_correct_combo(api: AssistantApi, category: str, situation: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_defaults/?category={category}&situation={situation}")
    assert response.status_code == 200


@pytest.mark.parametrize(param_combo, bad_combos)
def test_get_default_rituals_with_wrong_combo(api: AssistantApi, category: str, situation: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_defaults/?category={category}&situation={situation}")
    assert response.status_code == 400


def test_add_ok_default_ritual_to_user(api: AssistantApi) -> None:
    get_user_rits_response = api.get_with_auth("/v1/sos_rituals/")
    assert get_user_rits_response.status_code == 200
    # might be []
    assert get_user_rits_response.json() is not None
    prev_numb_of_rits = len(get_user_rits_response.json())

    correct_id = 3000129241702033816
    post_response = api.post_with_auth(url=f"/v1/default_sos_ritual/?default_ritual_id={correct_id}")
    assert post_response.status_code == 200

    get_user_rits_response_after_post = api.get_with_auth("/v1/sos_rituals/")
    assert get_user_rits_response_after_post.status_code == 200
    assert get_user_rits_response_after_post.json() is not None
    new_len_of_rits = len(get_user_rits_response_after_post.json())
    assert new_len_of_rits - prev_numb_of_rits == 1

    delete_response = api.delete_with_auth(url=f"/v1/sos_rituals/?ritual_id={correct_id}")
    assert delete_response.status_code == 200


def test_add_wrong_default_ritual_to_user(api: AssistantApi) -> None:
    wrong_id = 2000129241702033816
    post_response = api.post_with_auth(url=f"/v1/default_sos_ritual/?default_ritual_id={wrong_id}")
    assert post_response.status_code == 400