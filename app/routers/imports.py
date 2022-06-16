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
    if not ShopUnitProxy.create_batch(data.updateDate, data.items):
        raise HTTPException(status_code=400, detail='Items creation failed')
    return 200
