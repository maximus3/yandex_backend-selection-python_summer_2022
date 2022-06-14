import logging

from fastapi import APIRouter

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
    for item in data.items:
        logger.debug('Got new import item: %s', item)
    return 200
