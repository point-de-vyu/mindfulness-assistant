from fastapi import APIRouter
from typing import List
from api_backend.app.schemes.sos_rituals import SosRitual
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.logger import get_logger
from api_backend.app.utils import get_postgres_engine
from api_backend.app.utils import raise_400_error
from api_backend.app.utils import raise_404_error
from api_backend.app.managers.sos_manager import SosSelfHelpManager


router = APIRouter(tags=["sos_rituals"])
logger = get_logger()
sql_engine = get_postgres_engine()
sos_mng = SosSelfHelpManager(engine=sql_engine, logger=logger)
user_mng = UserManager(engine=sql_engine, logger=logger)


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_categories/",
    description="Get categories of default rituals, e.g. Meditation"
)
def get_categories() -> List[str]:
    logger.info("Getting available sos categories")
    result = sos_mng.get_available_categories()
    return result


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_situations/",
    description="Get situations of default rituals, e.g. Stress"
)
def get_situations() -> List[str]:
    logger.info("Getting available sos situations")
    result = sos_mng.get_available_situations()
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
    logger.info("Getting the list of default sos rituals")
    try:
        user_rituals = sos_mng.get_default_rituals(category_name=category, situation_name=situation)
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
    logger.info(f"Getting sos rituals for {username=}")
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    try:
        user_id = user.id
        user_rituals = sos_mng.get_user_rituals(user_id, category_name=category, situation_name=situation)
    except ValueError as val_err:
        raise_400_error(msg=str(val_err))
    return user_rituals


@router.post(
    "/custom_sos_ritual/{username}/",
    summary="Add a custom ritual created by a user"
)
def add_ritual_for_user(username: str, custom_ritual: SosRitual) -> None:
    logger.info(f"Adding a custom sos rituals for {username=}: {custom_ritual}")
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    user_id = user.id
    try:
        sos_mng.add_custom_ritual(user_id, custom_ritual)
    except ValueError as val_err:
        raise_400_error(msg=str(val_err))


@router.post(
    "/default_sos_ritual/{username}/",
    summary="Add a default ritual to user's own"
)
def add_default_ritual_for_user(username: str, default_ritual_id: int) -> None:
    logger.info(f"Adding a default ritual {default_ritual_id=} for {username=}")
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    user_id = user.id
    try:
        sos_mng.add_default_ritual_for_user(user_id, default_ritual_id)
    except ValueError as err:
        raise_400_error(msg=str(err))


@router.delete(
    "/sos_rituals/{username}/",
    summary="Delete a chosen ritual from a user's data"
)
def remove_ritual_for_user(username: str, ritual_id: int) -> None:
    logger.info(f"Deleting a ritual {ritual_id=} from {username=}")
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    user_id = user.id
    sos_mng.remove_ritual_from_user_data(user_id, ritual_id)
