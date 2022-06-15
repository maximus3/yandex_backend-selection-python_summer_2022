async def test_node_no_data(client, import_batches_data):
    response = await client.get(
        f'/node/{import_batches_data[0]["items"][0]["id"]}/statistic'
    )
    assert response.status_code == 400


async def test_node_ok(client, import_batches_data):
    response = await client.get(
        f'/node/{import_batches_data[0]["items"][0]["id"]}/statistic?item_id={import_batches_data[0]["items"][0]["id"]}&date_start=2020-01-01T12:00:00.000Z&date_end=2020-01-02T12:00:00.000Z'
    )
    assert response.status_code == 200
