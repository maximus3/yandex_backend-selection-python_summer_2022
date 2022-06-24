import logging
from typing import Any, Union

from fastapi import APIRouter, HTTPException

from app.utils import iso_8601_to_datetime
from database.proxy import ShopUnitProxy, ShopUnitStatisticUnitProxy
from database.schemas import ErrorScheme, ShopUnitStatisticResponseSchema

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/node',
    tags=['node'],
    responses={
        404: ErrorScheme(message='Item not found', code=404).dict(),
        400: ErrorScheme(message='Validation Failed', code=400).dict(),
    },
)


@router.get(
    '/{item_id}/statistic', response_model=ShopUnitStatisticResponseSchema
)
async def statistic(
    item_id: str, dateStart: str, dateEnd: str
) -> Union[ShopUnitStatisticResponseSchema, list[dict[str, Any]]]:
    try:
        dt_date_start = iso_8601_to_datetime(dateStart)
        dt_date_end = iso_8601_to_datetime(dateEnd)
    except ValueError as exc:
        raise HTTPException(status_code=400) from exc
    logger.debug(
        'Getting statistic for item %s from %s to %s',
        item_id,
        dateStart,
        dateEnd,
    )
    model = ShopUnitProxy.get(id=item_id)
    if model is None:
        logger.debug('Item %s not found', item_id)
        raise HTTPException(status_code=404)

    items: list[
        ShopUnitStatisticUnitProxy
    ] = ShopUnitStatisticUnitProxy.get_all_filter(
        item_id, dt_date_start, dt_date_end
    )
    return ShopUnitStatisticResponseSchema(items=items)
