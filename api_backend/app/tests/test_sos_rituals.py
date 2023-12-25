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


def test_get_sos_categories(api: AssistantApi):
    response = api.get_with_auth(url="/v1/sos_categories/")
    assert response.status_code == 200
    assert response.json()


def test_get_sos_situations(api: AssistantApi):
    response = api.get_with_auth(url="/v1/sos_situations/")
    assert response.status_code == 200
    assert response.json()


def test_get_test_user_rituals(api: AssistantApi):
    response = api.get_with_auth(url="/v1/sos_rituals/")
    assert response.status_code == 200
    # TODO add rituals
    assert len(response.json()) == 0


def test_get_all_default_rituals(api: AssistantApi):
    response = api.get_with_auth(url="/v1/sos_defaults/")
    assert response.status_code == 200


@pytest.mark.parametrize(param_category, ok_categories)
def test_get_default_rituals_with_correct_category(api: AssistantApi, category: str):
    response = api.get_with_auth(url=f"/v1/sos_defaults/?category={category}")
    assert response.status_code == 200


@pytest.mark.parametrize(param_category, bad_categories)
def test_get_default_rituals_with_wrong_category(api: AssistantApi, category: str):
    response = api.get_with_auth(url=f"/v1/sos_defaults/?category={category}")
    assert response.status_code == 400


@pytest.mark.parametrize(param_situation, ok_situations)
def test_get_default_rituals_with_correct_situation(api: AssistantApi, situation: str):
    response = api.get_with_auth(url=f"/v1/sos_defaults/?situation={situation}")
    assert response.status_code == 200


@pytest.mark.parametrize(param_situation, bad_situations)
def test_get_default_rituals_with_wrong_situation(api: AssistantApi, situation: str):
    response = api.get_with_auth(url=f"/v1/sos_defaults/?situation={situation}")
    assert response.status_code == 400


@pytest.mark.parametrize(param_combo, ok_combos)
def test_get_default_rituals_with_correct_combo(api: AssistantApi, category: str, situation: str):
    response = api.get_with_auth(url=f"/v1/sos_defaults/?category={category}&situation={situation}")
    assert response.status_code == 200


@pytest.mark.parametrize(param_combo, bad_combos)
def test_get_default_rituals_with_wrong_combo(api: AssistantApi, category: str, situation: str):
    response = api.get_with_auth(url=f"/v1/sos_defaults/?category={category}&situation={situation}")
    assert response.status_code == 400
