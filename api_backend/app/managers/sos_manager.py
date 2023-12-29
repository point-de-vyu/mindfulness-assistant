import sqlalchemy
from api_backend.app.schemes.sos_rituals import SosRitual
from api_backend.app.schemes.sos_rituals import SosRitualToCreate
from api_backend.app.schemes.sos_rituals import SosTable
from api_backend.app.schemes.error_messages import ErrorMsg
import logging
from typing import List


class SosSelfHelpManager:

    def __init__(
            self,
            engine: sqlalchemy.Engine,
            logger: logging.Logger
    ) -> None:
        self.sql_connection = engine.connect()
        self.metadata = sqlalchemy.MetaData()
        self.logger = logger

    def get_available_categories(self) -> List[str]:
        table = sqlalchemy.Table(SosTable.CATEGORIES, self.metadata, autoload_with=self.sql_connection)
        query = sqlalchemy.select(table.c.name)
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchall()
        if not rows:
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT)
        # TODO table schema?
        results = [row._asdict()["name"] for row in rows]
        return results

    def get_available_situations(self) -> List[str]:
        table = sqlalchemy.Table(SosTable.SITUATIONS, self.metadata, autoload_with=self.sql_connection)
        query = sqlalchemy.select(table.c.name)
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchall()
        if not rows:
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT)
        # TODO table schema?
        results = [row._asdict()["name"] for row in rows]
        return results

    def get_default_rituals(
            self,
            category_name: str | None = None,
            situation_name: str | None = None
    ) -> List[SosRitual]:
        category_id = self._get_category_id(category_name) if category_name else None
        situation_id = self._get_situation_id(situation_name) if situation_name else None

        query = sqlalchemy.select('*').select_from(sqlalchemy.func.get_default_sos_rituals(category_id, situation_id))
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchall()
        result_dicts = [SosRitual(**row._asdict()) for row in rows]
        return result_dicts

    def get_user_rituals(
            self,
            user_id: int,
            category_name: str | None = None,
            situation_name: str | None = None
    ) -> List[SosRitual]:
        category_id = self._get_category_id(category_name) if category_name else None
        situation_id = self._get_situation_id(situation_name) if situation_name else None

        query = sqlalchemy.select('*').select_from(sqlalchemy.func.get_user_sos_rituals(user_id, category_id, situation_id))
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchall()
        result_dicts = [SosRitual(**row._asdict()) for row in rows]
        return result_dicts

    def add_custom_ritual(self, user_id: int, custom_ritual: SosRitualToCreate) -> int:
        category_id = self._get_category_id(custom_ritual.category)
        situation_id = self._get_situation_id(custom_ritual.situation)
        result = self.sql_connection.execute(
            sqlalchemy.func.add_custom_sos_ritual(
                user_id,
                category_id,
                situation_id,
                custom_ritual.title,
                custom_ritual.description,
                custom_ritual.url,
                custom_ritual.tags
            )
        )
        self.sql_connection.commit()
        rows = result.fetchmany()
        result = rows[0][0]
        if not result:
            msg = ErrorMsg.FAILED_DB_RESULT
            self.logger.critical(msg)
            raise RuntimeError(msg)
        return result

    def _get_category_id(self, category_name: str) -> int:
        result = self.sql_connection.execute(sqlalchemy.func.get_category_id_from_name(category_name))
        rows = result.fetchmany()
        if len(rows) > 1:
            msg = ErrorMsg.ROWS_MORE_THAN_ONE
            self.logger.critical(msg)
            raise RuntimeError(msg)
        # TODO треш, что с этим делать? это rows[0]._asdict()
        """
        [
            {
                "funct_name_1": result
            }
        ]
        """
        result = rows[0][0]
        if not result:
            raise ValueError(ErrorMsg.SOS_CATEGORY_INVALID)
        return result

    def _get_situation_id(self, situation_name: str) -> int:
        result = self.sql_connection.execute(sqlalchemy.func.get_situation_id_from_name(situation_name))
        rows = result.fetchmany()
        if len(rows) > 1:
            raise RuntimeError(ErrorMsg.ROWS_MORE_THAN_ONE)
        result = rows[0][0]
        if not result:
            raise ValueError(ErrorMsg.SOS_SITUATION_INVALID)
        return result

    def _is_existing_default_ritual_id(self, ritual_id: int) -> bool:
        table = sqlalchemy.Table(SosTable.DEFAULT_IDS, self.metadata, autoload_with=self.sql_connection)
        query = sqlalchemy.select(table).filter(table.c.id == ritual_id)
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchall()
        if rows:
            return True
        return False

    def add_default_ritual_for_user(self, user_id: int, ritual_id: int) -> None:
        if not self._is_existing_default_ritual_id(ritual_id):
            raise ValueError(ErrorMsg.SOS_DEFAULT_RITUAL_ID_INVALID)
        table = sqlalchemy.Table(SosTable.USER_RITUAL, self.metadata, autoload_with=self.sql_connection)

        query = sqlalchemy.insert(table).values(
            user_id=user_id,
            ritual_id=ritual_id
        )
        executed_query = self.sql_connection.execute(query)
        inserted_pkey = executed_query.inserted_primary_key
        self.sql_connection.commit()
        # TODO  sqlalchemy.exc.IntegrityError:
        if not inserted_pkey:
            self.logger.critical(f"Failed to add {ritual_id=} for {user_id=}")
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT)
        self.logger.info(f"Added {ritual_id=} for {user_id=}")

    def remove_ritual_from_user_data(self, user_id: int, ritual_id: int) -> None:
        # todo check if it's even there else 404
        query = sqlalchemy.func.delete_ritual_from_user_data(user_id, ritual_id)
        executed_query = self.sql_connection.execute(query)
        self.sql_connection.commit()
        result = executed_query.fetchone()
        if not result:
            self.logger.critical(f"Failed to delete {ritual_id=} for {user_id=}")
            raise RuntimeError(ErrorMsg.FAILED_DB_RESULT)
        self.logger.info(f"Added {ritual_id=} for {user_id=}")

