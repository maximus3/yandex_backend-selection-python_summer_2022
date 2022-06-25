import datetime as dt

from app.utils import datetime_to_iso_8601, iso_8601_to_datetime
from tests_data.utils import print_diff, sort_items


async def test_statistics_no_data(client, import_batches_data):
    response = await client.get(
        f'/node/{import_batches_data[0]["items"][0]["id"]}/statistic'
    )
    assert response.status_code == 400


async def test_statistics_no_iso8601(
    prepare_db_shop_unit_env, client, import_batches_data
):
    response = await client.get(
        f'/node/{import_batches_data[0]["items"][0]["id"]}/statistic?dateStart=123&dateEnd=456'
    )
    assert response.status_code == 400


async def test_statistic_empty(
    prepare_db_shop_unit_env, client, import_batches_data
):
    date_start = datetime_to_iso_8601(
        iso_8601_to_datetime(import_batches_data[-1]['updateDate'])
        + dt.timedelta(1)
    )
    date_end = datetime_to_iso_8601(
        iso_8601_to_datetime(import_batches_data[-1]['updateDate'])
        + dt.timedelta(2)
    )
    response = await client.get(
        f'/node/{import_batches_data[0]["items"][0]["id"]}/statistic?'
        f'dateStart={date_start}&'
        f'dateEnd={date_end}'
    )
    assert response.status_code == 200

    statistic = response.json()
    assert statistic == {'items': []}


async def test_statistic_ok(
    prepare_db_shop_unit_env, client, import_batches_data, expected_statistic
):
    date_start = import_batches_data[0]['updateDate']
    date_end = datetime_to_iso_8601(
        iso_8601_to_datetime(import_batches_data[-1]['updateDate'])
        + dt.timedelta(1)
    )
    response = await client.get(
        f'/node/{import_batches_data[0]["items"][0]["id"]}/statistic?'
        f'dateStart={date_start}&'
        f'dateEnd={date_end}'
    )
    assert response.status_code == 200

    statistic = response.json()
    sort_items(statistic)
    sort_items(expected_statistic)
    assert (
        statistic == expected_statistic
    ), f'see {print_diff(expected_statistic, statistic)}'
