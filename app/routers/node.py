import datetime as dt
import logging
from typing import Any, Union

from fastapi import APIRouter

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
async def nodes(
    item_id: str, date_start: dt.datetime, date_end: dt.datetime
) -> Union[ShopUnitStatisticResponseSchema, dict[str, Any]]:
    logger.debug(
        'Getting statistic for item %s from %s to %s',
        item_id,
        date_start,
        date_end,
    )
    return {}
