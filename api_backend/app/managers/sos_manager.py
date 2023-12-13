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

    def get_default_rituals(self) -> List[SosRitual]:
        query = sqlalchemy.text("SELECT * FROM get_default_sos_rituals()")
        executed_q = self.sql_connection.execute(query)
        rows = executed_q.fetchall()
        result_dicts = [SosRitual(**row._asdict()) for row in rows]
        return result_dicts