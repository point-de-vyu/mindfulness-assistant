import json

import pytest
from typing import List
from api_backend.app.tests.conftest import AssistantApi
from api_backend.app.schemes.sos_rituals import SosRitualToCreate
from api_backend.app.schemes.sos_rituals import SosRitual
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

custom_ritual_title = "test custom ritual"
custom_ritual_descr = "...some description..."
custom_ritual_url = "https://media.giphy.com/media/maNB0qAiRVAty/giphy.gif"
custom_ritual_tags = None

bad_rituals_to_create = [
    SosRitualToCreate(
        title=custom_ritual_title,
        category=random.choice(bad_categories),
        situation=random.choice(ok_situations),
        description=custom_ritual_descr,
        url=custom_ritual_url,
        tags=custom_ritual_tags
    ),
    SosRitualToCreate(
        title=custom_ritual_title,
        category=random.choice(ok_categories),
        situation=random.choice(bad_situations),
        description=custom_ritual_descr,
        url=custom_ritual_url,
        tags=custom_ritual_tags
    ),
    SosRitualToCreate(
        title=custom_ritual_title,
        category=random.choice(bad_categories),
        situation=random.choice(bad_situations),
        description=custom_ritual_descr,
        url=custom_ritual_url,
        tags=custom_ritual_tags
    )
]


@pytest.fixture()
def ok_ritual_to_create() -> SosRitualToCreate:
    return SosRitualToCreate(
        title=custom_ritual_title,
        category=random.choice(ok_categories),
        situation=random.choice(ok_situations),
        description=custom_ritual_descr,
        url=custom_ritual_url,
        tags=custom_ritual_tags
    )


@pytest.fixture()
def correct_default_ritual_id() -> int:
    return 3000129241702033816


@pytest.fixture()
def wrong_default_ritual_id() -> int:
    return 2000129247500863806


def test_get_sos_categories(api: AssistantApi) -> None:
    response = api.get_with_auth(url="/v1/sos_categories/")
    assert response.status_code == 200
    assert response.json()


def test_get_sos_situations(api: AssistantApi) -> None:
    response = api.get_with_auth(url="/v1/sos_situations/")
    assert response.status_code == 200
    assert response.json()


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


def test_get_all_user_rituals(api: AssistantApi) -> None:
    get_user_rits_response = api.get_with_auth("/v1/sos_rituals/")
    assert get_user_rits_response.status_code == 200
    # might be []
    assert get_user_rits_response.json() is not None


@pytest.mark.parametrize(param_category, ok_categories)
def test_get_user_rituals_with_correct_category(api: AssistantApi, category: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_rituals/?category={category}")
    assert response.status_code == 200


@pytest.mark.parametrize(param_category, bad_categories)
def test_get_user_rituals_with_wrong_category(api: AssistantApi, category: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_rituals/?category={category}")
    assert response.status_code == 400


@pytest.mark.parametrize(param_situation, ok_situations)
def test_get_user_rituals_with_correct_situation(api: AssistantApi, situation: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_rituals/?situation={situation}")
    assert response.status_code == 200


@pytest.mark.parametrize(param_situation, bad_situations)
def test_get_user_rituals_with_wrong_situation(api: AssistantApi, situation: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_rituals/?situation={situation}")
    assert response.status_code == 400


@pytest.mark.parametrize(param_combo, ok_combos)
def test_get_user_rituals_with_correct_combo(api: AssistantApi, category: str, situation: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_rituals/?category={category}&situation={situation}")
    assert response.status_code == 200


@pytest.mark.parametrize(param_combo, bad_combos)
def test_get_user_rituals_with_wrong_combo(api: AssistantApi, category: str, situation: str) -> None:
    response = api.get_with_auth(url=f"/v1/sos_rituals/?category={category}&situation={situation}")
    assert response.status_code == 400


def test_add_ok_default_ritual_to_user(api: AssistantApi, correct_default_ritual_id: int) -> None:
    id = correct_default_ritual_id
    post_response = api.post_with_auth(url=f"/v1/default_sos_ritual/?default_ritual_id={id}")
    assert post_response.status_code == 200

    get_user_rits_response_after_post = api.get_with_auth(f"/v1/sos_rituals/{id}")
    assert get_user_rits_response_after_post.status_code == 200
    assert get_user_rits_response_after_post.json() is not None

    delete_response = api.delete_with_auth(url=f"/v1/sos_rituals/{id}")
    assert delete_response.status_code == 200


def test_add_duplicate_default_ritual_to_user(api: AssistantApi, correct_default_ritual_id: int) -> None:
    id = correct_default_ritual_id
    post_response = api.post_with_auth(url=f"/v1/default_sos_ritual/?default_ritual_id={id}")
    assert post_response.status_code == 200

    post_duplicate_response = api.post_with_auth(url=f"/v1/default_sos_ritual/?default_ritual_id={id}")
    assert post_duplicate_response.status_code == 409


def test_add_wrong_default_ritual_to_user(api: AssistantApi, wrong_default_ritual_id: int) -> None:
    id = wrong_default_ritual_id
    post_response = api.post_with_auth(url=f"/v1/default_sos_ritual/?default_ritual_id={id}")
    assert post_response.status_code == 400


def test_add_correct_custom_ritual_to_user(api: AssistantApi, ok_ritual_to_create: SosRitualToCreate) -> None:
    ritual = ok_ritual_to_create
    post_response = api.post_with_auth(url="/v1/custom_sos_ritual/", content=ritual.model_dump_json())
    assert post_response.status_code == 200
    assert post_response.json()
    created_ritual_id = post_response.json()["created_ritual_id"]

    get_created_ritual_response = api.get_with_auth(f"/v1/sos_rituals/{created_ritual_id}")
    assert get_created_ritual_response.status_code == 200
    assert get_created_ritual_response.json()
    created_ritual = SosRitual(**get_created_ritual_response.json())
    assert ritual.title == created_ritual.title
    assert ritual.description == created_ritual.description
    assert ritual.category == created_ritual.category
    assert ritual.situation == created_ritual.situation
    assert ritual.url == created_ritual.url

    delete_response = api.delete_with_auth(url=f"/v1/sos_rituals/{created_ritual_id}")
    assert delete_response.status_code == 200


@pytest.mark.parametrize("ritual", bad_rituals_to_create)
def test_add_wrong_custom_ritual_to_user(api: AssistantApi, ritual: SosRitualToCreate) -> None:
    post_response = api.post_with_auth(url="/v1/custom_sos_ritual/", content=ritual.model_dump_json())
    assert post_response.status_code == 400


def test_delete_existing_ritual_from_user(api: AssistantApi, correct_default_ritual_id: int) -> None:
    id = correct_default_ritual_id
    post_response = api.post_with_auth(url=f"/v1/default_sos_ritual/?default_ritual_id={id}")
    assert post_response.status_code == 200

    delete_response = api.delete_with_auth(url=f"/v1/sos_rituals/{id}")
    assert delete_response.status_code == 200

    get_response = api.get_with_auth(url=f"/v1/sos_rituals/{id}")
    assert get_response.status_code == 404


def test_delete_absent_ritual_from_user(api: AssistantApi, wrong_default_ritual_id: int) -> None:
    id = wrong_default_ritual_id
    delete_response = api.delete_with_auth(url=f"/v1/sos_rituals/{id}")
    assert delete_response.status_code == 404

