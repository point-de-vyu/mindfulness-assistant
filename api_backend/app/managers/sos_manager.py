import sqlalchemy
from sqlalchemy import func
from api_backend.app.schemes.sos_rituals import SosRitual
from api_backend.app.schemes.sos_rituals import SosTable
from api_backend.app.utils import get_postgres_engine
import logging
from typing import Dict, List


class SosSelfHelpManager():

    def __init__(self, sql_connection: sqlalchemy.Connection | None = None) -> None:
        if not sql_connection:
            engine = get_postgres_engine()
            sql_connection = engine.connect()
        self.sql_connection = sql_connection
        self.metadata = sqlalchemy.MetaData()

    def get_available_categories(self) -> List[str]:
        table = sqlalchemy.Table(SosTable.CATEGORIES, self.metadata, autoload_with=self.sql_connection)
        query = sqlalchemy.select(table.c.name)
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchall()
        # TODO table schema?
        results = [row._asdict()["name"] for row in rows]
        return results

    def get_available_situations(self) -> List[str]:
        table = sqlalchemy.Table(SosTable.SITUATIONS, self.metadata, autoload_with=self.sql_connection)
        query = sqlalchemy.select(table.c.name)
        executed_query = self.sql_connection.execute(query)
        rows = executed_query.fetchall()
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

    def add_custom_ritual(self, user_id: int, custom_ritual: SosRitual) -> int:
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
        # LESSON_LEARNT with connections you always have to commit. And with engine?
        # TODO learn engine VS session VS connection
        self.sql_connection.commit()
        rows = result.fetchmany()
        result = rows[0][0]
        if not result:
            raise RuntimeError("smth went wrong")
        return result

    def _get_category_id(self, category_name: str):
        result = self.sql_connection.execute(sqlalchemy.func.get_category_id_from_name(category_name))
        rows = result.fetchmany()
        if len(rows) > 1:
            raise RuntimeError(f"found {len(rows)} rows")
        # TODO треш, что с этим делать? это rows[0]._asdict()
        """
        [
            {
                "funct_name_1": result
            }
        ]
        """
        result = rows[0][0]
        # result = list(rows[0]._asdict().values())[0]
        if not result:
            raise ValueError(f"{category_name=} doesn't exist")
        return result

    def _get_situation_id(self, situation_name: str) -> int:
        result = self.sql_connection.execute(sqlalchemy.func.get_situation_id_from_name(situation_name))
        rows = result.fetchmany()
        if len(rows) > 1:
            raise RuntimeError(f"found {len(rows)} rows")
        result = rows[0][0]
        # result = list(rows[0]._asdict().values())[0]
        if not result:
            raise ValueError(f"{situation_name=} doesn't exist")
        return result
