import logging

from fastapi import APIRouter, HTTPException

from database.proxy import ShopUnitProxy
from database.schemas import ErrorScheme, ShopUnitImportRequestSchema

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/imports',
    tags=['imports'],
    responses={
        200: {'description': 'Success'},
        404: ErrorScheme(message='Not found', code=404).dict(),
        400: ErrorScheme(message='Validation Failed', code=400).dict(),
    },
)


@router.post('')
async def imports(data: ShopUnitImportRequestSchema) -> int:
    list_of_id = [item.id for item in data.items]
    if len(list_of_id) != len(set(list_of_id)):
        logger.debug('Duplicate ids')
        raise HTTPException(
            status_code=400,
            detail='Duplicate id in items',
        )
    for item in data.items:
        logger.debug('Got new import item: %s', item)
        model = ShopUnitProxy.get(id=item.id)
        if model is None:
            if ShopUnitProxy.create(**item.dict(), date=data.updateDate):
                logger.debug('Created new import item: %s', item)
                continue
            logger.debug('Failed to create new item: %s', item)
            raise HTTPException(status_code=400, detail='Item creation failed')

        if model.type != item.type:
            logger.debug('Item type mismatch: %s', item)
            raise HTTPException(status_code=400, detail='Item type mismatch')
        if model.update(date=data.updateDate, **item.dict()):
            logger.debug('Updated import item: %s', item)
            continue
        logger.debug('Failed to update item: %s', item)
        raise HTTPException(status_code=400, detail='Item update failed')
    return 200
