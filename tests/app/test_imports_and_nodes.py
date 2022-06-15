from tests.utils import deep_sort_children, print_diff


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
