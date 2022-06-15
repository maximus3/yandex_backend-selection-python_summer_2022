async def test_sales_no_data(client, import_batches_data):
    response = await client.get(f'/sales')
    assert response.status_code == 400


async def test_sales_ok(client, import_batches_data):  # TODO
    response = await client.get(f'/sales?date=2022-02-01T12:00:00.000Z')
    assert response.status_code == 200
