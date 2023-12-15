from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from typing import List
from api_backend.app.schemes.user import User
from api_backend.app.managers.user_manager import UserManager


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
    "/users/",
    summary="Get user(s)",
    description="Get user(s) by:"
            "\n- any parameter"
            "\n- a combo of parameters"
            "\n- no parameters: simply all users"
)
def get_users(
    id: int | None = None,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    date_registered: str | None = None
) -> List[User]:
    user_mng = UserManager()
    users = user_mng.get_users(
        id=id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        date_registered=date_registered
    )
    return users
