import sqlalchemy
from api_backend.app.schemes.sos_rituals import SosRitual
from api_backend.app.schemes.sos_rituals import SosRitualToCreate
from api_backend.app.schemes.sos_rituals import SosTable
from api_backend.app.schemes.error_messages import ErrorMsg
from api_backend.db.models.sos import SosSituations, SosCategories, SosDefaultRitualIds, UserRitual
import logging
from typing import List
from sqlalchemy.orm import Session


class SosSelfHelpManager:
    def __init__(self, session: Session, logger: logging.Logger) -> None:
        self.db_session = session
        self.logger = logger

    def get_available_categories(self) -> List[str]:
        query = sqlalchemy.select(SosCategories.name)
        executed_query = self.db_session.execute(query)
        result = list(executed_query.scalars().all())
        if not result:
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT)

        return result

    def get_available_situations(self) -> List[str]:
        query = sqlalchemy.select(SosSituations.name)
        executed_query = self.db_session.execute(query)
        result = list(executed_query.scalars().all())
        if not result:
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT)
        return result

    def get_default_rituals(
        self, category_name: str | None = None, situation_name: str | None = None
    ) -> List[SosRitual]:
        category_id = self._get_category_id(category_name) if category_name else None
        situation_id = (
            self._get_situation_id(situation_name) if situation_name else None
        )
        query = sqlalchemy.select("*").select_from(
            sqlalchemy.func.get_default_sos_rituals(category_id, situation_id)
        )
        executed_query = self.db_session.execute(query)
        rows = executed_query.fetchall()
        result_dicts = [SosRitual(**row._asdict()) for row in rows]
        return result_dicts

    def get_user_rituals(
        self,
        user_id: int,
        category_name: str | None = None,
        situation_name: str | None = None,
    ) -> List[SosRitual]:
        category_id = self._get_category_id(category_name) if category_name else None
        situation_id = (
            self._get_situation_id(situation_name) if situation_name else None
        )
        query = sqlalchemy.select("*").select_from(
            sqlalchemy.func.get_user_sos_rituals(user_id, category_id, situation_id)
        )
        executed_query = self.db_session.execute(query)
        rows = executed_query.fetchall()
        result_dicts = [SosRitual(**row._asdict()) for row in rows]
        return result_dicts

    def get_user_ritual_by_id(self, user_id: int, ritual_id: int) -> SosRitual | None:
        user_rituals = self.get_user_rituals(user_id)
        for ritual in user_rituals:
            if ritual.id == ritual_id:
                return ritual
        return None

    def add_custom_ritual(self, user_id: int, custom_ritual: SosRitualToCreate) -> int:
        category_id = self._get_category_id(custom_ritual.category)
        situation_id = self._get_situation_id(custom_ritual.situation)
        result = self.db_session.execute(
            sqlalchemy.func.add_custom_sos_ritual(
                user_id,
                category_id,
                situation_id,
                custom_ritual.title,
                custom_ritual.description,
                custom_ritual.url,
                custom_ritual.tags,
            )
        )
        self.db_session.commit()
        result = result.scalar_one_or_none()
        if not result:
            msg = ErrorMsg.FAILED_DB_RESULT
            self.logger.critical(msg)
            raise RuntimeError(msg)
        return result

    def _get_category_id(self, category_name: str) -> int:
        query = sqlalchemy.select(SosCategories.id).filter_by(name=category_name)
        result = self.db_session.execute(query)
        result = result.scalar_one_or_none()
        if not result:
            raise ValueError(ErrorMsg.SOS_CATEGORY_INVALID)
        return result

    def _get_situation_id(self, situation_name: str) -> int:
        query = sqlalchemy.select(SosSituations.id).filter_by(name=situation_name)
        result = self.db_session.execute(query)
        result = result.scalar_one_or_none()
        if not result:
            raise ValueError(ErrorMsg.SOS_SITUATION_INVALID)
        return result

    def _is_existing_default_ritual_id(self, ritual_id: int) -> bool:
        query = sqlalchemy.select(SosDefaultRitualIds.id).filter_by(id=ritual_id)
        executed_query = self.db_session.execute(query)
        result = executed_query.scalar_one_or_none()
        if result:
            return True
        return False

    def add_default_ritual_for_user(self, user_id: int, ritual_id: int) -> None:
        if not self._is_existing_default_ritual_id(ritual_id):
            raise ValueError(ErrorMsg.SOS_DEFAULT_RITUAL_ID_INVALID)

        query = sqlalchemy.insert(UserRitual).values(user_id=user_id, ritual_id=ritual_id)
        executed_query = self.db_session.execute(query)
        inserted_pkey = executed_query.inserted_primary_key
        self.db_session.commit()
        if not inserted_pkey:
            self.logger.critical(f"Failed to add {ritual_id=} for {user_id=}")
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT)
        self.logger.info(f"Added {ritual_id=} for {user_id=}")

    def remove_ritual_from_user_data(self, user_id: int, ritual_id: int) -> None:
        ritual = self.get_user_ritual_by_id(user_id, ritual_id)
        if not ritual:
            raise ValueError(ErrorMsg.SOS_RITUAL_ID_NOT_IN_USER)

        query = sqlalchemy.func.delete_ritual_from_user_data(user_id, ritual_id)
        executed_query = self.db_session.execute(query)
        self.db_session.commit()
        result = executed_query.fetchone()
        if not result:
            self.logger.critical(f"Failed to delete {ritual_id=} for {user_id=}")
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT)
        self.logger.info(f"Added {ritual_id=} for {user_id=}")

    def log_ritual_feedback(self, user_id: int, ritual_id: int, feedback: str) -> None:
        query = sqlalchemy.func.add_sos_ritual_feedback(user_id, ritual_id, feedback)
        executed_query = self.db_session.execute(query)
        self.db_session.commit()
        result = executed_query.scalar()
        if not result:
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT)
        self.logger.info(f"Logged journal entry for {ritual_id=} from {user_id=}")
