from fastapi import APIRouter
from fastapi import HTTPException
from typing import List
from api_backend.app.schemes.sos_rituals import SosRitual
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.utils import get_postgres_engine

from api_backend.app.managers.sos_manager import SosSelfHelpManager


router = APIRouter()

# TODO
"""
- добавить ритуал юзеру из дефолтных
"""


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_categories/",
    description="Get categories of default rituals, e.g. Meditation"
)
def get_categories() -> List[str]:
    mng = SosSelfHelpManager()
    return mng.get_available_categories()


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_situations/",
    description="Get situations of default rituals, e.g. Stress"
)
def get_situations() -> List[str]:
    mng = SosSelfHelpManager()
    return mng.get_available_situations()


@router.get(
    "/sos_defaults/",
    summary="Get default suggestions of rituals",
    description="Can be filtered by:"
                "\t1) a category"
                "\t2) a situation"
                "\t3) a combination of the two"
)
def get_default_sos_rituals(category: str | None = None, situation: str | None = None) -> List[SosRitual]:
    try:
        mng = SosSelfHelpManager()
        user_rituals = mng.get_default_rituals(category_name=category, situation_name=situation)
    except ValueError as err:
        error_msg = str(err)
        raise HTTPException(status_code=404, detail=error_msg)
    return user_rituals


# TODO может все же клиент будет хранить свой id и обращаться с ним? каждую операцию искать айдишник по имени?..
@router.get(
    "/sos_rituals/{username}/",
    summary="Get rituals by user's username",
    description="Get a user's sos rituals:"
                "\t1) with no params = all of them"
                "\t2) from a category"
                "\t3) for a situation"
                "\t4) with a combination of the above"
)
def get_user_rituals(username: str, category: str | None = None, situation: str | None = None):
    engine = get_postgres_engine()
    db_connection = engine.connect()
    user_mng = UserManager(sql_connection=db_connection)
    user = user_mng.get_users(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="No such user found")
    try:
        user_id = user[0].id
        sos_mng = SosSelfHelpManager(sql_connection=db_connection)
        user_rituals = sos_mng.get_user_rituals(user_id, category_name=category, situation_name=situation)
    except ValueError as err:
        error_msg = str(err)
        raise HTTPException(status_code=404, detail=error_msg)
    return user_rituals


@router.post(
    "/custom_sos_ritual/",
    summary="Add a ritual to a user",
    description="Either a default one by its ID or a custom one with all params?"
)
def add_ritual_to_user(username: str, custom_ritual: SosRitual):
    engine = get_postgres_engine()
    db_connection = engine.connect()
    user_mng = UserManager(sql_connection=db_connection)
    user = user_mng.get_users(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="No such user found")
    user_id = user[0].id
    sos_mng = SosSelfHelpManager(sql_connection=db_connection)
    try:
        created_ritual_id = sos_mng.add_custom_ritual(user_id, custom_ritual)
    except ValueError as err:
        error_msg = str(err)
        raise HTTPException(status_code=404, detail=error_msg)
    # TODO this may be reduntant ?
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal messup:(")

    return f"{created_ritual_id=}"


@router.post(
    "/default_sos_ritual/",
    summary="Add a ritual to a user",
    description="Either a default one by its ID"
)
def add_ritual_to_user(username: str, default_ritual_id: int):
    return "TBD"


# TODO REMOVE AFTER TESTING
@router.get("/cat_by_name/{name}")
def get_cat_id(name:str):
    sos_mng = SosSelfHelpManager()
    return sos_mng._get_category_id(name)