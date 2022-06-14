from app.utils import datetime_to_iso_8601
from database.proxy import ShopUnitProxy


async def test_imports_post_validation_error(client):
    response = await client.post('/imports')
    assert response.status_code == 400


async def test_imports_post_validation_error_with_json(client):
    response = await client.post('/imports', json={'aaa': 'bbb'})
    assert response.status_code == 400


async def check_import_ok(web_client, batches):
    for batch in batches:
        response = await web_client.post('/imports', json=batch)
        assert response.status_code == 200
        for item in batch['items']:
            model = ShopUnitProxy.get(id=item['id'])
            assert model is not None
            assert batch['updateDate'] == datetime_to_iso_8601(model.date)


async def test_imports_post_ok(client, import_batches_data):
    await check_import_ok(client, import_batches_data)


async def test_imports_post_ok_if_exists(
    prepare_db_shop_unit_env, client, import_batches_data
):
    await check_import_ok(client, import_batches_data)
