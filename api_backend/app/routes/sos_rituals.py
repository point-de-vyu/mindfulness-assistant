from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from typing import List
from api_backend.app.schemes.sos_rituals import SosRitual
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.utils import get_postgres_engine
from api_backend.app.managers.sos_manager import SosSelfHelpManager


router = APIRouter(tags=["sos_rituals"])


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_categories/",
    description="Get categories of default rituals, e.g. Meditation"
)
def get_categories() -> List[str]:
    try:
        mng = SosSelfHelpManager()
        result = mng.get_available_categories()
    except RuntimeError as runt_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
    return result


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_situations/",
    description="Get situations of default rituals, e.g. Stress"
)
def get_situations() -> List[str]:
    try:
        mng = SosSelfHelpManager()
        result = mng.get_available_situations()
    except RuntimeError as runt_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
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
        raise HTTPException(status_code=404, detail=str(val_err))
    except RuntimeError as runt_err:
        raise HTTPException(status_code=500, detail=str(runt_err))
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
    try:
        user_mng = UserManager(sql_connection=db_connection)
        user = user_mng.get_user_by_username(username)
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(val_err))
    except RuntimeError as runt_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
    try:
        user_id = user[0].id
        sos_mng = SosSelfHelpManager(sql_connection=db_connection)
        user_rituals = sos_mng.get_user_rituals(user_id, category_name=category, situation_name=situation)
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(val_err))
    return user_rituals


@router.post(
    "/custom_sos_ritual/{username}/",
    summary="Add a custom ritual created by a user",
    description="-"
)
def add_ritual_for_user(username: str, custom_ritual: SosRitual):
    engine = get_postgres_engine()
    db_connection = engine.connect()
    try:
        user_mng = UserManager(sql_connection=db_connection)
        user = user_mng.get_user_by_username(username)
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(val_err))
    except RuntimeError as runt_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
    user_id = user[0].id
    sos_mng = SosSelfHelpManager(sql_connection=db_connection)
    try:
        created_ritual_id = sos_mng.add_custom_ritual(user_id, custom_ritual)
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(val_err))

    return f"{created_ritual_id=}"


@router.post(
    "/default_sos_ritual/{username}/",
    summary="Add a default ritual to user's own",
    description="-"
)
def add_default_ritual_for_user(username: str, default_ritual_id: int):
    engine = get_postgres_engine()
    db_connection = engine.connect()
    try:
        user_mng = UserManager(sql_connection=db_connection)
        user = user_mng.get_user_by_username(username)
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(val_err))
    except RuntimeError as runt_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
    user_id = user[0].id
    sos_mng = SosSelfHelpManager(sql_connection=db_connection)
    try:
        pkey = sos_mng.add_default_ritual_for_user(user_id, default_ritual_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    return f"created entry for {pkey}"


# TODO REMOVE AFTER TESTING
@router.get("/cat_by_name/{name}")
def get_cat_id(name: str):
    sos_mng = SosSelfHelpManager()
    return sos_mng._get_category_id(name)