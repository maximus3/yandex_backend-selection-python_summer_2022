from fastapi import APIRouter

from database.schemas import ErrorScheme, ShopUnitSchema

router = APIRouter(
    prefix='/nodes',
    tags=['nodes'],
    responses={
        404: ErrorScheme(message='Item not found', code=404).dict(),
        400: ErrorScheme(message='Validation Failed', code=400).dict(),
    },
)


@router.get('/{item_id}', response_model=ShopUnitSchema)
async def nodes(item_id: str):
    return {}
