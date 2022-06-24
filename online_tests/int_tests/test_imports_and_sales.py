from tests_data.utils import print_diff


async def send_imports_request(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                },
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id_1',
                    'parentId': 'id',
                    'price': 100,
                },
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()


async def send_update_request(client, date: str):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id_1',
                    'parentId': 'id',
                    'price': 200,
                },
            ],
            'updateDate': date,
        },
    )
    assert response.status_code == 200, response.json()


async def test_have_one_modif(client):
    result = {
        'items': [
            {
                'type': 'OFFER',
                'name': 'Товар',
                'id': 'id_1',
                'price': 100,
                'parentId': 'id',
                'date': '2022-02-01T12:00:00.000Z',
            }
        ]
    }
    await send_imports_request(client)

    response = await client.get(f'/sales?date=2022-02-01T12:00:00.000Z')
    assert response.status_code == 200, response.json()
    assert (
        response.json() == result
    ), f'see {print_diff(result, response.json())}'


async def test_have_many_modif(client):
    result = {
        'items': [
            {
                'type': 'OFFER',
                'name': 'Товар',
                'id': 'id_1',
                'price': 200,
                'parentId': 'id',
                'date': '2022-02-03T12:00:00.000Z',
            }
        ]
    }
    await send_imports_request(client)
    await send_update_request(client, '2022-02-03T12:00:00.000Z')

    response = await client.get(f'/sales?date=2022-02-03T12:00:00.000Z')
    assert response.status_code == 200, response.json()
    assert (
        response.json() == result
    ), f'see {print_diff(result, response.json())}'


async def test_have_many_modif_in_24h(client):
    result = {
        'items': [
            {
                'type': 'OFFER',
                'name': 'Товар',
                'id': 'id_1',
                'price': 200,
                'parentId': 'id',
                'date': '2022-02-01T13:00:00.000Z',
            }
        ]
    }
    await send_imports_request(client)
    await send_update_request(client, '2022-02-01T13:00:00.000Z')

    response = await client.get(f'/sales?date=2022-02-01T13:00:00.000Z')
    assert response.status_code == 200, response.json()
    assert (
        response.json() == result
    ), f'see {print_diff(result, response.json())}'


async def test_utc_ok(client):
    result = {
        'items': [
            {
                'type': 'OFFER',
                'name': 'Товар',
                'id': 'id_1',
                'price': 100,
                'parentId': 'id',
                'date': '2022-02-01T12:00:00.000Z',
            }
        ]
    }
    await send_imports_request(client)

    response = await client.get(f'/sales?date=2022-02-01T11:59:59.000Z')
    assert response.status_code == 200, response.json()
    assert response.json() == {
        'items': []
    }, f'see {print_diff({"items": []}, response.json())}'

    response = await client.get(f'/sales?date=2022-02-01T12:00:00.000Z')
    assert response.status_code == 200, response.json()
    assert (
        response.json() == result
    ), f'see {print_diff(result, response.json())}'

    response = await client.get(f'/sales?date=2022-02-02T12:00:00.000Z')
    assert response.status_code == 200, response.json()
    assert (
        response.json() == result
    ), f'see {print_diff(result, response.json())}'

    response = await client.get(f'/sales?date=2022-02-02T12:00:01.000Z')
    assert response.status_code == 200, response.json()
    assert response.json() == {
        'items': []
    }, f'see {print_diff({"items": []}, response.json())}'
