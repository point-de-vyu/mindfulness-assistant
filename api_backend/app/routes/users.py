from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from api_backend.app.logger import get_logger
from api_backend.app.utils import get_postgres_engine
from api_backend.app.schemes.user import User, UserToCreate
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.utils import raise_404_error

logger = get_logger()
router = APIRouter(tags=["users"])
user_mng = UserManager(engine=get_postgres_engine(), logger=logger)


@router.post(
    "/users/",
    summary="Add a new user"
)
def add_new_user(user: UserToCreate) -> None:
    logger.info(f"Creating new user {user}")
    try:
        result = user_mng.add_new_user(user)
    except RuntimeError as runt_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
    logger.info(f"Created new user with id={result}")


@router.get(
    "/user_by_username/{username}",
    summary="Get user by their unique username"
)
def get_user_by_username(username: str) -> User:
    logger.info(f"Getting user data for {username=}")
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(ErrorMsg.USER_NOT_FOUND)
    return user


@router.get(
    "/user_by_id/{id}",
    summary="Get user by their unique id"
)
def get_user_by_username(id: int) -> User:
    logger.info(f"Getting user data for {id=}")
    user = user_mng.get_by_id(id)
    if not user:
        raise_404_error(ErrorMsg.USER_NOT_FOUND)
    return user


@router.delete(
    "/users/",
    summary="Delete user and all their data"
)
def delete_user(username: str) -> None:
    # мб фиг с 500? все равно клиент их получит, а так можно без трай, если пустой лист юзера - шлем ошибкку:
    logger.info(f"Deleting user data for {username=}")
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    # except RuntimeError as runt_err:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
    user_id = user.id
    user_deleted = user_mng.delete_user(user_id)
    if not user_deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete?")
    logger.info(f"Deleted user with {username=} ({user_id=}) and all their data")