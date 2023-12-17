from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from typing import List
from api_backend.app.schemes.user import User
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.utils import raise_404_error

router = APIRouter(tags=["users"])


@router.post(
    "/users/",
    summary="Add a new user"
)
def add_new_user(user: User) -> str:
    user_mng = UserManager()
    try:
        result = user_mng.add_new_user(user)
    except RuntimeError as runt_err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
    return f"created user with id={result}"


@router.get(
    "/user_by_username/{username}",
    summary="Get user by their unique username"
)
def get_user_by_username(username: str) -> User:
    user_mng = UserManager()
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(ErrorMsg.USER_NOT_FOUND)
    return user


@router.get(
    "/user_by_id/{id}",
    summary="Get user by their unique id"
)
def get_user_by_username(id: int) -> User:
    user_mng = UserManager()
    user = user_mng.get_by_id(id)
    if not user:
        raise_404_error(ErrorMsg.USER_NOT_FOUND)
    return user


@router.delete(
    "/users/",
    summary="Delete user and all their data"
)
def delete_user(username: str):
    user_mng = UserManager()
    # мб фиг с 500? все равно клиент их получит, а так можно без трай, если пустой лист юзера - шлем ошибкку:
    user = user_mng.get_by_username(username)
    if not user:
        raise_404_error(msg=ErrorMsg.USER_NOT_FOUND)
    # except RuntimeError as runt_err:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(runt_err))
    user_id = user.id
    user_deleted = user_mng.delete_user(user_id)
    if not user_deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete?")
    return f"deleted user with id={user_id} and all their data"