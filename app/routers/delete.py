import logging

from fastapi import APIRouter

from database.schemas import ErrorScheme

logger = logging.getLogger(__name__)

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
async def delete(item_id: str) -> int:
    logger.debug('Deleting item %s', item_id)
    return 200
