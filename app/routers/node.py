import datetime as dt

from fastapi import APIRouter

from database.schemas import ErrorScheme, ShopUnitStatisticResponseSchema

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
async def nodes(item_id: str, dateStart: dt.datetime, dateEnd: dt.datetime):
    return {}
