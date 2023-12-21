import pytest
from fastapi.testclient import TestClient
from api_backend.app.main import app
from api_backend.app.utils import get_postgres_engine
import sqlalchemy

# class AssistantApi(TestClient):
client = TestClient(app)

#  docker exec api_backend-backend_api-1 pytest /app/api_backend/app/tests/test_client.py

def overridden_get_postgres_engine(db_name: str | None = None, is_autocommit: bool = False) -> sqlalchemy.engine.Engine:
    if not db_name:
        db_name = ":memory:"
    engine = sqlalchemy.create_engine(
        f'postgresql+psycopg2:///{db_name}', echo=True
    )
    if is_autocommit:
        engine = engine.execution_options(autocommit=True)
    return engine


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
