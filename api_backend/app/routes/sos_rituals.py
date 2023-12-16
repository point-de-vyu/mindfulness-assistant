from fastapi import APIRouter
from typing import List
from api_backend.app.schemes.sos_rituals import SosRitual
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.utils import get_postgres_engine
from api_backend.app.utils import raise_400_error
from api_backend.app.utils import raise_404_error
from api_backend.app.managers.sos_manager import SosSelfHelpManager


router = APIRouter(tags=["sos_rituals"])


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_categories/",
    description="Get categories of default rituals, e.g. Meditation"
)
def get_categories() -> List[str]:
    mng = SosSelfHelpManager()
    result = mng.get_available_categories()
    return result


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_situations/",
    description="Get situations of default rituals, e.g. Stress"
)
def get_situations() -> List[str]:
    mng = SosSelfHelpManager()
    result = mng.get_available_situations()
    return result


@router.get(
    "/sos_defaults/",
    summary="Get default suggestions of rituals",
    description="Can be filtered by:"
                "\t1) a category"
                "\t2) a situation"
                "\t3) a combination of the two. NB browser does not show BIGINT ids correctly!"
)
def get_default_sos_rituals(category: str | None = None, situation: str | None = None) -> List[SosRitual]:
    try:
        mng = SosSelfHelpManager()
        user_rituals = mng.get_default_rituals(category_name=category, situation_name=situation)
    except ValueError as val_err:
        raise_400_error(msg=str(val_err))
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
def get_user_rituals(username: str, category: str | None = None, situation: str | None = None) -> List[SosRitual]:
    engine = get_postgres_engine()
    db_connection = engine.connect()
    user_mng = UserManager(sql_connection=db_connection)
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    try:
        user_id = user[0].id
        sos_mng = SosSelfHelpManager(sql_connection=db_connection)
        user_rituals = sos_mng.get_user_rituals(user_id, category_name=category, situation_name=situation)
    except ValueError as val_err:
        raise_400_error(msg=str(val_err))
    return user_rituals


@router.post(
    "/custom_sos_ritual/{username}/",
    summary="Add a custom ritual created by a user"
)
def add_ritual_for_user(username: str, custom_ritual: SosRitual):
    engine = get_postgres_engine()
    db_connection = engine.connect()
    user_mng = UserManager(sql_connection=db_connection)
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    user_id = user[0].id
    sos_mng = SosSelfHelpManager(sql_connection=db_connection)
    try:
        created_ritual_id = sos_mng.add_custom_ritual(user_id, custom_ritual)
    except ValueError as val_err:
        raise_400_error(msg=str(val_err))

    return f"{created_ritual_id=}"


@router.post(
    "/default_sos_ritual/{username}/",
    summary="Add a default ritual to user's own"
)
def add_default_ritual_for_user(username: str, default_ritual_id: int):
    engine = get_postgres_engine()
    db_connection = engine.connect()
    user_mng = UserManager(sql_connection=db_connection)
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    user_id = user[0].id
    sos_mng = SosSelfHelpManager(sql_connection=db_connection)
    try:
        pkey = sos_mng.add_default_ritual_for_user(user_id, default_ritual_id)
    except ValueError as err:
        raise_400_error(msg=str(err))

    return f"created entry for {pkey}"


@router.delete(
    "/sos_rituals/{username}/",
    summary="Delete a chosen ritual from a user's data"
)
def remove_ritual_for_user(username: str, ritual_id: int):
    engine = get_postgres_engine()
    db_connection = engine.connect()
    user_mng = UserManager(sql_connection=db_connection)
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    user_id = user[0].id
    sos_mng = SosSelfHelpManager(sql_connection=db_connection)
    result = sos_mng.remove_ritual_from_user_data(user_id, ritual_id)



# TODO REMOVE AFTER TESTING
@router.get("/cat_by_name/{name}")
def get_cat_id(name: str):
    sos_mng = SosSelfHelpManager()
    return sos_mng._get_category_id(name)