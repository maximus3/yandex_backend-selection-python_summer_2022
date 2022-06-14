import pytest
from httpx import AsyncClient

from app.creator import create_app
from app.utils import iso_8601_to_datetime
from database import create_session as real_create_session
from tests.database import tmp_database_engine, tmp_database_name
from tests.database.config import Session, prepare_db, remove_db
from tests.static import (
    IMPORT_BATCHES,
    import_batches_proxy_data,
    shop_unit_proxy_data_single,
)


@pytest.fixture()
def prepare_db_env(mocker):
    mocker.patch('database.Session', Session)
    mocker.patch('config.config.cfg.DATABASE_NAME', tmp_database_name)
    mocker.patch('config.config.cfg.DATABASE_ENGINE', tmp_database_engine)
    prepare_db()
    yield
    remove_db()


@pytest.fixture()
def prepare_db_shop_unit_env(prepare_db_env):
    model_list, model_schema_list, batch_list = import_batches_proxy_data()
    for model, _, batch in zip(model_list, model_schema_list, batch_list):
        date = iso_8601_to_datetime(batch['updateDate'])
        for item in batch['items']:
            model.create(
                **item,
                date=date,
            )
    yield


@pytest.fixture()
def prepare_db_shop_unit_single_env(prepare_db_env):
    for model, _, parameters in shop_unit_proxy_data_single():
        model.create(**parameters)


@pytest.fixture()
def create_session(prepare_db_env):
    return real_create_session


@pytest.fixture()
async def client(prepare_db_env):
    async with AsyncClient(
        app=create_app(), base_url='http://localhost:8090/'
    ) as client:
        yield client


@pytest.fixture()
def import_batches_data():
    return IMPORT_BATCHES[:]
