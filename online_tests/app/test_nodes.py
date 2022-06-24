from tests_data.utils import deep_sort_children, print_diff


async def test_nodes_get_not_found(client, import_batches_data):
    response = await client.get(
        f'/nodes/{import_batches_data[0]["items"][0]["id"]}'
    )
    assert response.status_code == 404


async def test_nodes_get_ok(
    prepare_db_shop_unit_env, client, import_batches_data, expected_tree_data
):
    response = await client.get(
        f'/nodes/{import_batches_data[0]["items"][0]["id"]}'
    )
    assert response.status_code == 200
    data = response.json()
    deep_sort_children(data)
    deep_sort_children(expected_tree_data)
    assert (
        data == expected_tree_data
    ), f'see {print_diff(expected_tree_data, data)}'
