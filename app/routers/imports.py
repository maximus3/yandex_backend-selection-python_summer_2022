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
    logger.debug('Got new import request: %s', data.json())
    return 200
