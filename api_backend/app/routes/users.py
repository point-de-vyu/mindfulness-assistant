from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from api_backend.app.auth import get_user_id_by_token
from api_backend.app.logger import get_logger
from api_backend.app.utils.mng_getters import get_user_manager
from api_backend.app.utils.error_raisers import raise_404_error
from api_backend.app.schemes.user import User
from api_backend.app.schemes.user import UserToCreate
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.app.managers.user_manager import UserManager

from typing import Dict
from typing import Annotated

logger = get_logger()
router = APIRouter(tags=["users"])
UserMngDep = Annotated[UserManager, Depends(get_user_manager)]


@router.post(
    "/users/",
    summary="Add a new user"
)
def add_new_user(
        user: UserToCreate,
        user_mng: UserMngDep
) -> Dict[str, str]:
    logger.info(f"Creating new user {user}")
    try:
        id, token = user_mng.add_new_user(user)
    except RuntimeError as runt_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
    logger.info(f"Created new user with {id=}")
    return {"your_secret_authorization_token": token}


@router.get(
    "/users/",
    summary="Get user info"
)
def get_user(
    user_mng: UserMngDep,
    user_id: int = Depends(get_user_id_by_token)
) -> User:
    user = user_mng.get_by_id(user_id)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    return user


@router.get(
    "/user_by_username/{username}",
    summary="Get user by their unique username"
)
def get_user_by_username(
        username: str,
        user_mng: UserMngDep
) -> User:
    logger.info(f"Getting user data for {username=}")
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(ErrorMsg.USER_NOT_FOUND)
    return user


@router.get(
    "/user_by_id/{id}",
    summary="Get user by their unique id"
)
def get_user_by_username(
        id: int,
        user_mng: UserMngDep
) -> User:
    logger.info(f"Getting user data for {id=}")
    user = user_mng.get_by_id(id)
    if not user:
        raise_404_error(ErrorMsg.USER_NOT_FOUND)
    return user


@router.delete(
    "/users/",
    summary="Delete user and all their data"
)
def delete_user(
        user_mng: UserMngDep,
        user_id: int = Depends(get_user_id_by_token)
) -> None:
    # мб фиг с 500? все равно клиент их получит, а так можно без трай, если пустой лист юзера - шлем ошибкку:
    logger.info(f"Deleting user data for {user_id=}")
    user_deleted = user_mng.delete_user(user_id)
    if not user_deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete?")
    logger.info(f"Deleted user with {user_id=} and all their data")