from fastapi import APIRouter
from typing import List
from api_backend.app.schemes.user import User
from api_backend.app.schemes.sos_rituals import SosRitual
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.utils import get_postgres_engine

from api_backend.app.managers.sos_manager import SosSelfHelpManager


router = APIRouter()

# TODO
"""
- получить ритуалы юзера
- получить дефолтные ритуалы
- добавить ритуал юзеру
- добавить ритуал юзеру из дефолтных
"""


@router.get(
    "/sos_categories/",
    description="Get categories of default rituals, e.g. Meditation"
)
def get_categories() -> List[str]:
    mng = SosSelfHelpManager()
    return mng.get_available_categories()


@router.get(
    "/sos_situations/",
    description="Get situations of default rituals, e.g. Stress"
)
def get_situations() -> List[str]:
    mng = SosSelfHelpManager()
    return mng.get_available_situations()


@router.get(
    "/sos_defaults/",
    description="Get default suggestions of rituals"
)
def get_default_sos_rituals() -> List[SosRitual]:
    mng = SosSelfHelpManager()
    return mng.get_default_rituals()