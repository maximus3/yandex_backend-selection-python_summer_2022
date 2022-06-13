

async def test_imports_post_validation_error(client):
    response = await client.post('/imports')
    assert response.status_code == 400


async def test_imports_post_ok(client):
    response = await client.post('/imports')
    assert response.status_code == 200
