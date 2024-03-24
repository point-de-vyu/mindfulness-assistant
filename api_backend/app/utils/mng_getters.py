from fastapi import Depends
import logging
from api_backend.app.logger import get_logger
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.managers.sos_manager import SosSelfHelpManager
from api_backend.app.utils.db import database
from sqlalchemy.orm import Session


def get_user_manager(
    db_session: Session = Depends(database.get_session_dep),
    logger: logging.Logger = Depends(get_logger),
) -> UserManager:
    return UserManager(session=db_session, logger=logger)


def get_sos_manager(
    db_session: Session = Depends(database.get_session_dep),
    logger: logging.Logger = Depends(get_logger),
) -> SosSelfHelpManager:
    return SosSelfHelpManager(session=db_session, logger=logger)
