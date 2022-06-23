async def test_delete_not_found(client, import_batches_data):
    response = await client.delete(
        f'/delete/{import_batches_data[0]["items"][0]["id"]}'
    )
    assert response.status_code == 404


async def test_delete_ok(
    prepare_db_shop_unit_env, client, import_batches_data
):
    response = await client.delete(
        f'/delete/{import_batches_data[0]["items"][0]["id"]}'
    )
    assert response.status_code == 200, response.json()
    for batch in import_batches_data:
        for item in batch['items']:
            response = await client.get(f'/nodes/{item["id"]}')
            assert response.status_code == 404, response.json()


async def test_delete_ok_second(
    prepare_db_shop_unit_env, client, import_batches_data
):
    response = await client.delete(
        f'/delete/{import_batches_data[1]["items"][0]["id"]}'
    )
    assert response.status_code == 200, response.json()
    response = await client.delete(
        f'/delete/{import_batches_data[2]["items"][0]["id"]}'
    )
    assert response.status_code == 200, response.json()

    for item in import_batches_data[0]['items']:
        response = await client.get(f'/nodes/{item["id"]}')
        assert response.status_code == 200, response.json()
        assert response.json()['price'] is None
        assert response.json()['children'] == []

    for batch in import_batches_data[1:]:
        for item in batch['items']:
            response = await client.get(f'/nodes/{item["id"]}')
            assert response.status_code == 404, response.json()
