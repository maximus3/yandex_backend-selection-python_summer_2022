import logging
from typing import Any, Optional

from sqlalchemy.orm import Session as SessionType

from database.shop_unit_type import ShopUnitType

logger = logging.getLogger(__name__)


def update_delete_price(
    session: SessionType,
    obj_getter: Any,
    parent_id: str,
    date: Optional[str],
    is_offer: bool,
    offers_count: int,
    price: int,
) -> bool:
    logger.debug(
        'Parameters: %s, %s, %s, %s, %s, %s, %s',
        session,
        obj_getter,
        parent_id,
        date,
        is_offer,
        offers_count,
        price,
    )
    if is_offer:
        logger.debug('is_offer, setting offers_count to 1')
        offers_count = 1

    while parent_id:
        parent_model = obj_getter.get(session, id=parent_id)
        if parent_model is None:
            logger.debug('parent_model by %s is None', parent_id)
            return False

        new_offers_count = parent_model.offers_count - offers_count
        was_price = parent_model.price
        new_avg_price = None
        if new_offers_count > 0:
            new_avg_price = (
                was_price * parent_model.offers_count - price * offers_count
            ) / new_offers_count
        if not parent_model._update_now(
            session, price=new_avg_price, offers_count=new_offers_count
        ):
            logger.debug(
                'parent_model._update_now(%s, price=%s, offers_count=%s) failed',
                session,
                new_avg_price,
                new_offers_count,
            )
            return False
        if date:
            if not parent_model._update_now(session, date=date):
                logger.debug(
                    'parent_model._update_now(%s, date=%s) failed',
                    session,
                    date,
                )
                return False
        parent_id = parent_model.parentId

    return True


def update_price(
    is_update: bool, obj: Any, session: SessionType, **kwargs: Any
) -> bool:
    logger.debug('Parameters: %s, %s, %s', is_update, obj, kwargs)
    obj_type = kwargs.get('type')
    if obj_type is None:
        logger.debug('obj_type is None')
        return False
    price = kwargs.get('price')
    if (price is None or price < 0) and obj_type == ShopUnitType.OFFER:
        logger.debug('price is not valid')
        return False
    date = kwargs.get('date')
    if date is None:
        logger.debug('date is None')
        return False

    is_offer = obj_type == ShopUnitType.OFFER

    if is_update:
        offers_count = obj.offers_count
    else:
        kwargs['offers_count'] = None if is_offer else 0
        offers_count = kwargs['offers_count']

    if is_offer:
        logger.debug('is_offer, setting offers_count to 1')
        offers_count = 1
    logger.debug('offers_count: %s', offers_count)

    parent_id = kwargs.get('parentId')
    if is_update and parent_id != obj.parentId:
        if not update_delete_price(
            session,
            obj,
            obj.parentId,
            date,
            is_offer,
            obj.offers_count,
            obj.price,
        ):
            logger.debug('update_delete_price failed')
            return False
        is_update = False
    while parent_id:
        parent_model = obj.get(session, id=parent_id)
        if parent_model is None:
            logger.debug('parent_model by %s is None', parent_id)
            return False
        if offers_count > 0:

            was_offers_count = parent_model.offers_count or 0
            new_offers_count = (
                was_offers_count
                if is_update
                else was_offers_count + offers_count
            )

            was_price = parent_model.price or 0
            if is_offer:
                new_sum_price = (
                    was_price * was_offers_count + price * offers_count
                )
                if is_update:
                    new_sum_price -= obj.price * offers_count
                new_avg_price = new_sum_price / new_offers_count
            else:
                if is_update:
                    new_sum_price = (
                        was_price * was_offers_count + obj.price * offers_count
                    )
                    new_avg_price = new_sum_price / new_offers_count
                else:
                    new_avg_price = was_price

            if not parent_model._update_now(
                session, price=new_avg_price, offers_count=new_offers_count
            ):
                logger.debug(
                    'parent_model._update_now(%s, price=%s, offers_count=%s) failed',
                    session,
                    new_avg_price,
                    new_offers_count,
                )
                return False

        if not parent_model._update_now(session, date=date):
            logger.debug(
                'parent_model._update_now(%s, date=%s) failed', session, date
            )
            return False
        parent_id = parent_model.parentId

    return True
