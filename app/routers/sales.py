from fastapi import APIRouter
import datetime as dt

from database.schemas import ErrorScheme, ShopUnitStatisticResponseSchema


router = APIRouter(
    prefix='/sales',
    tags=['sales'],
    responses={
        404: ErrorScheme(message='Not found', code=404).dict(),
        400: ErrorScheme(message='Validation Failed', code=400).dict(),
    },
)


@router.get('', response_model=ShopUnitStatisticResponseSchema)
async def sales(date: dt.datetime):
    return {}
