from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from api_backend.app.auth import authentication
from api_backend.app.auth import client_authentication
from api_backend.app.logger import get_logger
from api_backend.app.utils.mng_getters import get_user_manager
from api_backend.app.utils.error_raisers import raise_404_error
from api_backend.app.utils.error_raisers import raise_409_error
from api_backend.app.schemes.user import User
from api_backend.app.schemes.user import UserToCreate
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.app.managers.user_manager import UserManager
from sqlalchemy.exc import IntegrityError
from typing import Dict
from typing import Annotated

logger = get_logger()
router = APIRouter(tags=["users"])
UserMngDep = Annotated[UserManager, Depends(get_user_manager)]


@router.post("/users/", summary="Add a new user")
def add_new_user(
    user: UserToCreate,
    user_mng: UserMngDep,
    client_id: int = Depends(client_authentication),
) -> None:
    logger.info(f"Creating new user {user}")
    try:
        id = user_mng.add_new_user(user, client_id)
    except IntegrityError:
        raise_409_error(ErrorMsg.USER_ALREADY_EXISTS)
    except RuntimeError as runt_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err)
        )
    logger.info(f"Created new user with {id=}")


@router.delete("/users/", summary="Delete user and all their data")
def delete_user(user_mng: UserMngDep, user_id: int = Depends(authentication)) -> None:
    logger.info(f"Deleting user data for {user_id=}")
    user_deleted = user_mng.delete_user(user_id)
    if not user_deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete?",
        )
    logger.info(f"Deleted user with {user_id=} and all their data")
