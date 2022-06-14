from fastapi import APIRouter

from database.schemas import ErrorScheme

router = APIRouter(
    prefix='/delete',
    tags=['delete'],
    responses={
        200: {'description': 'Success'},
        404: ErrorScheme(message='Item not found', code=404).dict(),
        400: ErrorScheme(message='Validation Failed', code=400).dict(),
    },
)


@router.delete('/{item_id}')
async def delete(item_id: str):
    return 200
