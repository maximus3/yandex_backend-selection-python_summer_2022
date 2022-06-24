import datetime as dt

from app.utils import datetime_to_iso_8601, iso_8601_to_datetime
from database.proxy import ShopUnitProxy, ShopUnitStatisticUnitProxy


async def test_statistic_get_deleted_and_children_in_db(
    prepare_db_shop_unit_env, client, import_batches_data
):
    ShopUnitProxy.get(id=import_batches_data[0]['items'][0]['id']).delete()
    date_start = import_batches_data[0]['updateDate']
    date_end = datetime_to_iso_8601(
        iso_8601_to_datetime(import_batches_data[-1]['updateDate'])
        + dt.timedelta(1)
    )
    for batch in import_batches_data:
        for item in batch['items']:
            item_id = item['id']
            response = await client.get(
                f'/node/{item_id}/statistic?'
                f'dateStart={date_start}&'
                f'dateEnd={date_end}'
            )
            assert response.status_code == 404
            assert ShopUnitStatisticUnitProxy.get_all(id=item_id) == []
