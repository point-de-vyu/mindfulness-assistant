from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from typing import List
from api_backend.app.auth import authentication
from api_backend.app.auth import client_authentication
from api_backend.app.schemes.sos_rituals import SosRitual
from api_backend.app.schemes.sos_rituals import SosRitualToCreate
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.app.logger import get_logger
from api_backend.app.utils.mng_getters import get_sos_manager
from api_backend.app.utils.error_raisers import raise_400_error
from api_backend.app.utils.error_raisers import raise_404_error
from api_backend.app.utils.error_raisers import raise_409_error
from api_backend.app.managers.sos_manager import SosSelfHelpManager
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=["sos_rituals"])
logger = get_logger()
SosMngDep = Annotated[SosSelfHelpManager, Depends(get_sos_manager)]


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_categories/",
    description="Get categories of default rituals, e.g. Meditation"
)
def get_categories(
        sos_mng: SosMngDep,
        user_id: int = Depends(authentication)
) -> List[str]:
    logger.info(f"{user_id=} getting available sos categories")
    result = sos_mng.get_available_categories()
    return result


# TODO может, возвращать не лист строк, а лист диктов {id: name}? чтобы посылать id
@router.get(
    "/sos_situations/",
    description="Get situations of default rituals, e.g. Stress"
)
def get_situations(
    sos_mng: SosMngDep,
    user_id: int = Depends(authentication),
) -> List[str]:
    logger.info(f"{user_id=} getting available sos situations")
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
def get_default_sos_rituals(
    sos_mng: SosMngDep,
    user_id: int = Depends(authentication),
    category: str | None = None,
    situation: str | None = None
) -> List[SosRitual]:
    logger.info(f"{user_id=} getting the list of default sos rituals")
    try:
        user_rituals = sos_mng.get_default_rituals(category_name=category, situation_name=situation)
    except ValueError as val_err:
        raise_400_error(msg=str(val_err))
    return user_rituals


@router.get(
    "/sos_rituals/",
    summary="Get user's rituals",
    description="Get a user's sos rituals:"
                "\t1) with no params = all of them"
                "\t2) from a category"
                "\t3) for a situation"
                "\t4) with a combination of the above"
)
def get_user_rituals(
        sos_mng: SosMngDep,
        user_id: int = Depends(authentication),
        category: str | None = None,
        situation: str | None = None
) -> List[SosRitual]:
    logger.info(f"{user_id=} getting sos rituals their rituals")
    try:
        user_rituals = sos_mng.get_user_rituals(user_id, category_name=category, situation_name=situation)
    except ValueError as val_err:
        raise_400_error(msg=str(val_err))
    return user_rituals


@router.get(
    "/sos_rituals/{ritual_id}",
    summary="Get user's ritual by ritual id",
)
def get_ritual_by_id(
        ritual_id: int,
        sos_mng: SosMngDep,
        user_id: int = Depends(authentication)
) -> SosRitual:
    ritual = sos_mng.get_user_ritual_by_id(user_id, ritual_id)
    if not ritual:
        raise_404_error(ErrorMsg.SOS_RITUAL_ID_NOT_IN_USER)
    return ritual


@router.post(
    "/custom_sos_ritual/",
    summary="Add a custom ritual created by a user"
)
def add_ritual_for_user(
        sos_mng: SosMngDep,
        custom_ritual: SosRitualToCreate,
        user_id: int = Depends(authentication)
) -> dict:
    logger.info(f"Adding a custom sos ritual for {user_id=}: {custom_ritual}")
    try:
        created_id = sos_mng.add_custom_ritual(user_id, custom_ritual)
    except ValueError as val_err:
        raise_400_error(msg=str(val_err))
    return {"created_ritual_id": created_id}


@router.post(
    "/default_sos_ritual/",
    summary="Add a default ritual to user's own"
)
def add_default_ritual_for_user(
        default_ritual_id: int,
        sos_mng: SosMngDep,
        user_id: int = Depends(authentication),

) -> None:
    logger.info(f"Adding a default ritual {default_ritual_id=} for {user_id=}")
    try:
        sos_mng.add_default_ritual_for_user(user_id, default_ritual_id)
    except ValueError as err:
        raise_400_error(msg=str(err))
    except IntegrityError:
        raise_409_error(msg=ErrorMsg.RITUAL_ALREADY_ADDED)


@router.delete(
    "/sos_rituals/{ritual_id}",
    summary="Delete a chosen ritual from a user's data"
)
def remove_ritual_for_user(
        ritual_id: int,
        sos_mng: SosMngDep,
        user_id: int = Depends(authentication)
) -> None:
    logger.info(f"Deleting a ritual {ritual_id=} from {user_id=}")
    try:
        sos_mng.remove_ritual_from_user_data(user_id, ritual_id)
    except ValueError as err:
        raise_404_error(msg=str(err))


@router.post(
    "/sos_feedback/",
    summary="Log a journal entry about a ritual"
)
def log_ritual_feedback(
    ritual_id: int,
    feedback: str,
    sos_mng: SosMngDep,
    user_id: int = Depends(authentication)
) -> None:
    logger.info(f"Saving journal entry for {ritual_id=} from {user_id=}")
    try:
        sos_mng.log_ritual_feedback(user_id, ritual_id, feedback)
    except IntegrityError as err:
        raise_400_error(msg=str(err))

