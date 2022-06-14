import logging

from fastapi import APIRouter, HTTPException

from database.proxy import ShopUnitProxy
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
    model = ShopUnitProxy.get(id=item_id)
    if model is None:
        logger.debug('Item %s not found', item_id)
        raise HTTPException(status_code=404)
    if model.delete():
        logger.debug('Item %s deleted', item_id)
        return 200
    logger.debug('Item %s not deleted', item_id)
    raise HTTPException(status_code=400, detail='Failed to delete item')
