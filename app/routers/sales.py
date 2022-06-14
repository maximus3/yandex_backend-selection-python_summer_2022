import datetime as dt
import logging
from typing import Any, Union

from fastapi import APIRouter

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
    date: dt.datetime,
) -> Union[ShopUnitStatisticResponseSchema, dict[str, Any]]:
    logger.debug('Getting sales for %s', date)
    return {}
