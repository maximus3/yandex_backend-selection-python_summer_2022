import pytest
from httpx import AsyncClient

from database import create_session as real_create_session
from tests.database import tmp_database_engine, tmp_database_name
from tests.database.config import Session, prepare_db, remove_db
from app.creator import create_app


@pytest.fixture()
def prepare_db_env(mocker):
    mocker.patch('database.Session', Session)
    mocker.patch('config.config.cfg.DATABASE_NAME', tmp_database_name)
    mocker.patch('config.config.cfg.DATABASE_ENGINE', tmp_database_engine)
    prepare_db()
    yield
    remove_db()


@pytest.fixture()
def create_session(prepare_db_env):
    return real_create_session


@pytest.fixture()
async def client():
    async with AsyncClient(
        app=create_app(), base_url='http://localhost:8090/'
    ) as client:
        yield client
