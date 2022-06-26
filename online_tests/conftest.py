import pytest
from httpx import AsyncClient

from online_tests import API_BASEURL
from tests_data.static import (
    EXPECTED_STATISTIC,
    EXPECTED_TREE,
    IMPORT_BATCHES,
    IMPORTS_AND_NODES_DATA,
)
from tests_data.utils import clear_used_ids


@pytest.fixture()
def import_batches_data():
    return IMPORT_BATCHES[:]


@pytest.fixture()
async def client(import_batches_data):
    all_item_ids = set()
    for batch in import_batches_data:
        for item in batch['items']:
            all_item_ids.add(item['id'])
    async with AsyncClient(base_url=API_BASEURL) as client:
        yield client
        await clear_used_ids(client, all_item_ids)
        await clear_used_ids(
            client,
            [
                'id',
                'id_1',
                'id_2',
                'id_3',
                'id1',
                'id2',
                'id3',
                'id_cat',
                'id200',
            ],
        )


@pytest.fixture()
async def prepare_db_shop_unit_env(client, import_batches_data):
    all_item_ids = set()
    for batch in import_batches_data:
        for item in batch['items']:
            all_item_ids.add(item['id'])

    for batch in import_batches_data:
        response = await client.post('/imports', json=batch)
        assert response.status_code == 200, response.json()

    yield

    await client.delete(f'delete/{import_batches_data[0]["items"][0]["id"]}')
    for item_id in all_item_ids:
        response = await client.get(f'nodes/{item_id}')
        assert response.status_code == 404


@pytest.fixture()
def expected_tree_data():
    return EXPECTED_TREE.copy()


@pytest.fixture()
def expected_statistic():
    return EXPECTED_STATISTIC.copy()


@pytest.fixture()
async def imports_and_nodes_data(client):
    all_item_ids = set()
    for batch, _ in IMPORTS_AND_NODES_DATA[:]:
        for item in batch['items']:
            all_item_ids.add(item['id'])

    yield IMPORTS_AND_NODES_DATA[:]

    await clear_used_ids(client, all_item_ids)
