async def test_imports_post_validation_error(client):
    response = await client.post('/imports')
    assert response.status_code == 400


async def test_imports_post_validation_error_with_json(client):
    response = await client.post('/imports', json={'aaa': 'bbb'})
    assert response.status_code == 400


async def test_imports_post_ok(client, import_batches_data):
    for batch in import_batches_data:
        response = await client.post('/imports', json=batch)
        assert response.status_code == 200


async def test_imports_post_ok_if_exists(
    prepare_db_shop_unit_env, client, import_batches_data
):
    for batch in import_batches_data:
        response = await client.post('/imports', json=batch)
        assert response.status_code == 200
