from fastapi import Depends
import logging
from api_backend.app.logger import get_logger
from api_backend.app.managers.user_manager import UserManager
from api_backend.app.managers.sos_manager import SosSelfHelpManager
from api_backend.app.utils.db import get_postgres_engine
import sqlalchemy


def get_user_manager(
        db_engine: sqlalchemy.Engine = Depends(get_postgres_engine),
        logger: logging.Logger = Depends(get_logger)
) -> UserManager:
    return UserManager(engine=db_engine, logger=logger)


def get_sos_manager(
    db_engine: sqlalchemy.Engine = Depends(get_postgres_engine),
    logger: logging.Logger = Depends(get_logger)
) -> SosSelfHelpManager:
    return SosSelfHelpManager(engine=db_engine, logger=logger)