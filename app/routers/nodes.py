import logging
from typing import Any, Union

from fastapi import APIRouter, HTTPException

from database.proxy import ShopUnitProxy
from database.schemas import ErrorScheme, ShopUnitSchema

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/nodes',
    tags=['nodes'],
    responses={
        404: ErrorScheme(message='Item not found', code=404).dict(),
        400: ErrorScheme(message='Validation Failed', code=400).dict(),
    },
)


@router.get('/{item_id}', response_model=ShopUnitSchema)
async def nodes(
    item_id: str,
) -> Union[ShopUnitProxy, ShopUnitSchema, dict[str, Any]]:
    logger.debug('Getting item %s', item_id)
    model = ShopUnitProxy.get(id=item_id)
    if model is None:
        logger.debug('Item %s not found', item_id)
        raise HTTPException(status_code=404)
    return model
