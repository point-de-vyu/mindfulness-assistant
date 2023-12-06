from fastapi import APIRouter
from typing import List
from api_backend.app.schemes.user import User
from api_backend.app.managers.user_manager import UserManager
from fastapi.responses import HTMLResponse
from api_backend.app.utils import get_postgres_engine
router = APIRouter()


@router.post(
    "/users/",
    summary="Add a new user"
)
def add_new_user(user: User) -> str:
    engine = get_postgres_engine()
    db_connection = engine.connect()
    user_mng = UserManager(sql_connection=db_connection)
    return f"created user with id={user_mng.add_new_user(user)}"


# @router.get(
#     "/users/",
#     summary="Get users"
# )
# def get_users():
#     engine = get_postgres_engine()
#     db_connection = engine.connect()
#     user_mng = UserManager(sql_connection=db_connection)
#     users = user_mng.get_users()
#     return users


# @router.get(
#     "/users/{username}",
#     summary="Get user by their username"
# )
# def get_user_by_username(username: str) -> List[User]:
#     engine = get_postgres_engine()
#     db_connection = engine.connect()
#     user_mng = UserManager(sql_connection=db_connection)
#     user = user_mng.get_user_by_username(username)
#     return user


@router.get(
    "/users/",
    summary="Get users by:"
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
    engine = get_postgres_engine()
    db_connection = engine.connect()
    user_mng = UserManager(sql_connection=db_connection)
    users = user_mng.get_users(
        id=id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        date_registered=date_registered
    )
    return users
