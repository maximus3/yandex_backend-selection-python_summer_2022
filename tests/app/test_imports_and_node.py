import datetime as dt

from app.utils import datetime_to_iso_8601, iso_8601_to_datetime
from tests.utils import print_diff, sort_items


async def test_statistic_offer(
    prepare_db_shop_unit_env, client, import_batches_data, expected_statistic
):
    item_id = import_batches_data[1]['items'][1]['id']
    date_start = import_batches_data[0]['updateDate']
    date_end = datetime_to_iso_8601(
        iso_8601_to_datetime(import_batches_data[-1]['updateDate'])
        + dt.timedelta(1)
    )
    result_1 = {
        'items': [
            {
                'type': 'OFFER',
                'name': 'jPhone 13',
                'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                'price': 79999,
                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'date': '2022-02-02T12:00:00.000Z',
            }
        ]
    }
    result_2 = {
        'items': [
            result_1['items'][0],
            {
                'type': 'OFFER',
                'name': 'jPhone 13',
                'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                'price': 123456,
                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'date': '2022-02-04T15:00:00.000Z',
            },
        ]
    }

    response = await client.get(
        f'/node/{item_id}/statistic?'
        f'date_start={date_start}&'
        f'date_end={date_end}'
    )
    assert response.status_code == 200

    statistic = response.json()
    assert statistic == result_1, f'see {print_diff(result_1, statistic)}'

    response = await client.post(
        '/imports',
        json={
            'items': [
                {
                    'id': result_2['items'][1]['id'],
                    'price': result_2['items'][1]['price'],
                    'type': result_2['items'][1]['type'],
                    'parentId': result_2['items'][1]['parentId'],
                    'name': result_2['items'][1]['name'],
                }
            ],
            'updateDate': date_end,
        },
    )
    assert response.status_code == 200, response.json()

    response = await client.get(
        f'/node/{item_id}/statistic?'
        f'date_start={date_start}&'
        f'date_end={date_end}'
    )
    assert response.status_code == 200

    statistic = response.json()
    assert statistic == result_1, f'see {print_diff(result_1, statistic)}'

    date_end = datetime_to_iso_8601(
        iso_8601_to_datetime(date_end) + dt.timedelta(1)
    )

    response = await client.get(
        f'/node/{item_id}/statistic?'
        f'date_start={date_start}&'
        f'date_end={date_end}'
    )
    assert response.status_code == 200

    statistic = response.json()
    sort_items(statistic)
    assert statistic == result_2, f'see {print_diff(result_2, statistic)}'
