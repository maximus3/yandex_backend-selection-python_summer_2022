from database.proxy import ShopUnitProxy


async def test_delete_not_found(client, import_batches_data):
    response = await client.delete(f'/delete/{import_batches_data[0]["items"][0]["id"]}')
    assert response.status_code == 404


async def test_imports_post_ok(
    prepare_db_shop_unit_env, client, import_batches_data
):
    response = await client.delete(f'/delete/{import_batches_data[0]["items"][0]["id"]}')
    assert response.status_code == 200
    for batch in import_batches_data:
        for item in batch['items']:
            model = ShopUnitProxy.get(id=item['id'])
            assert model is None
