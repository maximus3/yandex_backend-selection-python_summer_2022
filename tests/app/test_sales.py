async def test_sales_no_date(client):
    response = await client.get(f'/sales')
    assert response.status_code == 400


async def test_sales_wrong_date_format(client):
    response = await client.get(f'/sales?date=2022-02')
    assert response.status_code == 400


async def test_sales_ok_empty(client):
    response = await client.get(f'/sales?date=2022-02-01T12:00:00.000Z')
    assert response.status_code == 200, response.json()
    assert response.json() == {'items': []}
