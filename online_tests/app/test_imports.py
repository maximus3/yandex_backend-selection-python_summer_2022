async def test_imports_post_validation_error(client):
    response = await client.post('/imports')
    assert response.status_code == 400


async def test_imports_post_validation_error_with_json(client):
    response = await client.post('/imports', json={'aaa': 'bbb'})
    assert response.status_code == 400


async def check_import_ok(web_client, batches):
    for batch in batches:
        response = await web_client.post('/imports', json=batch)
        assert response.status_code == 200, response.json()
        for item in batch['items']:
            response = await web_client.get(f'/nodes/{item["id"]}')
            assert response.status_code == 200, response.json()
            assert batch['updateDate'] == response.json()['date']


async def test_imports_post_ok(client, import_batches_data):
    await check_import_ok(client, import_batches_data)


async def test_imports_post_ok_if_exists(
    prepare_db_shop_unit_env, client, import_batches_data
):
    await check_import_ok(client, import_batches_data)


async def test_imports_post_not_iso_8601_text(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                }
            ],
            'updateDate': 'aaa',
        },
    )
    assert response.status_code == 400


async def test_imports_post_not_iso_8601(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                }
            ],
            'updateDate': '2022-02-32T12:00:00',
        },
    )
    assert response.status_code == 400


async def test_imports_post_not_iso_8601_with_dot(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                }
            ],
            'updateDate': '2022-02-32T12:00:00.000',
        },
    )
    assert response.status_code == 400


async def test_imports_post_iso_8601_ok(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()


async def test_imports_post_offer_without_price(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_category_with_price(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                    'price': 100,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_category_with_price_str(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                    'price': '100',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_offer_price_neg(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id',
                    'price': -100,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_offer_price_zero_ok(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id',
                    'price': 0,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()


async def test_imports_post_offer_ok(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id',
                    'price': 100,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()


async def test_imports_post_category_ok(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()


async def test_imports_post_double_id(client):
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
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                },
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_double_id_diff(client):
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
                    'id': 'id',
                },
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_item_type_mismatch_cat_to_offer(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Категория',
                    'id': 'id',
                    'price': 100,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_item_type_mismatch_offer_to_cat(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id',
                    'price': 100,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_item_type_no_mismatch(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id',
                    'price': 100,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар 2',
                    'id': 'id',
                    'price': 150,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()


async def test_imports_post_parent_no_category(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id1',
                    'price': 100,
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар 2',
                    'id': 'id2',
                    'price': 150,
                    'parentId': 'id1',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_parent_no_category_update(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id_cat',
                },
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id1',
                    'price': 100,
                },
                {
                    'type': 'OFFER',
                    'name': 'Товар 2',
                    'id': 'id200',
                    'price': 200,
                    'parentId': 'id_cat',
                },
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар 2',
                    'id': 'id200',
                    'price': 200,
                    'parentId': 'id1',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400


async def test_imports_post_parent_ok(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id1',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'id2',
                    'price': 150,
                    'parentId': 'id1',
                }
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 200, response.json()


async def test_imports_post_error_in_last(client):
    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id1',
                },
                {
                    'type': 'OFFER',
                    'name': 'Товар неправильный',
                    'id': 'id2',
                },
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
    )
    assert response.status_code == 400

    response = await client.get('/nodes/id1')
    assert response.status_code == 404, response.json()

    response = await client.get('/nodes/id2')
    assert response.status_code == 404, response.json()
