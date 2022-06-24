from tests_data.utils import deep_sort_children, print_diff


async def test_change_parents_ok(client, imports_and_nodes_data):
    for imp_data, nodes_data in imports_and_nodes_data:
        response = await client.post(
            '/imports',
            json=imp_data,
        )
        assert response.status_code == 200, response.json()

        response = await client.get(f'/nodes/id1')
        assert response.status_code == 200
        data = response.json()
        deep_sort_children(data)
        deep_sort_children(nodes_data)
        assert data == nodes_data, f'see {print_diff(nodes_data, data)}'


async def test_import_avg_price_ok(client):
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
                    'name': 'Товар 1',
                    'id': 'id_1',
                    'parentId': 'id',
                    'price': 100,
                },
                {
                    'type': 'OFFER',
                    'name': 'Товар 2',
                    'id': 'id_2',
                    'parentId': 'id',
                    'price': 1,
                },
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()

    response = await client.get(f'/nodes/id')
    assert response.status_code == 200
    assert response.json()['price'] == 50

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар 3',
                    'id': 'id_3',
                    'parentId': 'id',
                    'price': 1,
                },
            ],
            'updateDate': '2022-02-02T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()

    response = await client.get(f'/nodes/id')
    assert response.status_code == 200
    assert response.json()['price'] == 34
