import logging
from typing import Any, Union

from fastapi import APIRouter, HTTPException

from app.utils import iso_8601_to_datetime
from database.proxy import ShopUnitStatisticUnitProxy
from database.schemas import ErrorScheme, ShopUnitStatisticResponseSchema

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/sales',
    tags=['sales'],
    responses={
        404: ErrorScheme(message='Not found', code=404).dict(),
        400: ErrorScheme(message='Validation Failed', code=400).dict(),
    },
)


@router.get('', response_model=ShopUnitStatisticResponseSchema)
async def sales(
    date: str,
) -> Union[ShopUnitStatisticResponseSchema, list[dict[str, Any]]]:
    try:
        dt_date = iso_8601_to_datetime(date)
    except ValueError as exc:
        raise HTTPException(status_code=400) from exc

    logger.debug('Getting sales for %s', date)

    items = ShopUnitStatisticUnitProxy.get_last_modified(dt_date)
    return ShopUnitStatisticResponseSchema(items=items)
