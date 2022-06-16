import datetime as dt
import json
import logging
from typing import Any, Optional, Type, TypeVar

from sqlalchemy.orm import Session as SessionType

from app.utils import iso_8601_to_datetime
from database import create_session
from database.models import BaseModel, ShopUnit, ShopUnitStatisticUnit
from database.schemas import BaseModel as SchemaBaseModel
from database.schemas import (
    ShopUnitImportSchema,
    ShopUnitSchema,
    ShopUnitStatisticUnitSchema,
)
from database.shop_unit_type import ShopUnitType
from database.utils import UpdateSet

logger = logging.getLogger(__name__)

BaseProxyType = TypeVar('BaseProxyType', bound='BaseProxy')


class BaseProxy:
    BASE_MODEL: Type[BaseModel] = BaseModel
    SCHEMA_MODEL: Type[SchemaBaseModel] = SchemaBaseModel

    def __init__(self, model: BaseModel):
        self.uuid = model.uuid
        self.created_at = model.created_at
        self.updated_at = model.updated_at

    def __eq__(self: BaseProxyType, other: object) -> bool:
        if not isinstance(other, BaseProxy):
            return NotImplemented
        return self.uuid == other.uuid

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(uuid={self.uuid!r})>'

    @classmethod
    def get(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> Optional[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                return cls.get(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one_or_none()
        if model:
            return cls(model)
        return None

    @classmethod
    def get_expect(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> BaseProxyType:
        if session is None:
            with create_session() as new_session:
                return cls.get_expect(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one()
        return cls(model)

    @classmethod
    def get_model(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> BaseModel:
        if session is None:
            with create_session() as new_session:
                return cls.get_model(new_session, **kwargs)
        return session.query(cls.BASE_MODEL).filter_by(**kwargs).one()

    @classmethod
    def get_schema_model(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> SchemaBaseModel:
        if session is None:
            with create_session() as new_session:
                return cls.get_schema_model(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one()
        return cls.SCHEMA_MODEL.from_orm(model)

    @classmethod
    def get_all(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> list[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                return cls.get_all(new_session, **kwargs)
        data = []
        for model in session.query(cls.BASE_MODEL).filter_by(**kwargs).all():
            data.append(cls(model))
        return data

    @classmethod
    def get_or_create(
        cls: Type[BaseProxyType], session: SessionType = None, **kwargs: Any
    ) -> Optional[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                model = cls.get(new_session, **kwargs)
                if model:
                    logger.debug('%s already exists', cls.__name__)
                    return model
            with create_session() as new_session:
                if not cls.create(new_session, **kwargs):
                    logger.debug(
                        'Failed to create %s with %s', cls.__name__, kwargs
                    )
                    return None
            with create_session() as new_session:
                return cls.get(new_session, **kwargs)
        logger.debug('session is not None')
        return None

    @classmethod
    def create(
        cls: Type[BaseProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            with create_session() as new_session:
                return cls.create(new_session, **kwargs)
        model = cls.BASE_MODEL(**kwargs)
        session.add(model)
        return True

    def update(
        self: BaseProxyType,
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            with create_session() as new_session:
                return self.update(new_session, **kwargs)
        model = (
            session.query(self.BASE_MODEL)
            .filter_by(uuid=self.uuid)
            .one_or_none()
        )
        if model is None:
            return False
        for key, value in kwargs.items():
            if hasattr(model, key) and hasattr(self, key):
                setattr(model, key, value)
                setattr(self, key, value)
            else:
                return False
        session.add(model)
        return True

    def delete(self: BaseProxyType, session: SessionType = None) -> bool:
        if session is None:
            with create_session() as new_session:
                return self.delete(new_session)
        model = self.get_me(session)
        session.delete(model)
        return True

    def get_me(self: BaseProxyType, session: SessionType) -> BaseModel:
        return session.query(self.BASE_MODEL).get(self.uuid)


ShopUnitProxyType = TypeVar('ShopUnitProxyType', bound='ShopUnitProxy')


class ShopUnitProxy(BaseProxy):
    BASE_MODEL = ShopUnit
    SCHEMA_MODEL = ShopUnitSchema

    def __init__(self, shop_unit: ShopUnit) -> None:
        super().__init__(shop_unit)
        self.id = shop_unit.id
        self.name = shop_unit.name
        self.type = shop_unit.type
        self.price = shop_unit.price
        self.parentId = shop_unit.parentId
        self.date = shop_unit.date
        self.offers_count = shop_unit.offers_count

        self.children = [ShopUnitProxy(unit) for unit in shop_unit.children]

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def _create_statistics(
        cls: Type[ShopUnitProxyType],
        session: SessionType,
        updated_models: UpdateSet,
    ) -> bool:
        for model in updated_models:
            if isinstance(model, ShopUnitProxy):
                kwargs = {
                    'id': model.id,
                    'name': model.name,
                    'date': iso_8601_to_datetime(model.date),
                    'type': model.type,
                    'price': model.price,
                    'parentId': model.parentId,
                }
            else:
                model_kwargs = json.loads(model)
                kwargs = {
                    'id': model_kwargs['id'],
                    'name': model_kwargs['name'],
                    'date': iso_8601_to_datetime(model_kwargs['date']),
                    'type': model_kwargs['type'],
                    'price': model_kwargs.get('price'),
                    'parentId': model_kwargs.get('parentId'),
                }

            if not ShopUnitStatisticUnitProxy.create(session, **kwargs):
                logger.debug(
                    'ShopUnitStatisticUnitProxy.create(session=%s, kwargs=%s) failed',
                    session,
                    kwargs,
                )
                return False

        return True

    @classmethod
    def create(
        cls: Type[ShopUnitProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            logger.debug('session is None')
            with create_session() as new_session:
                return cls.create(new_session, **kwargs)
        updated_models = kwargs.get('updated_models')
        if updated_models is None:
            updated_models = UpdateSet()
        else:
            kwargs.pop('updated_models')
        if not cls._create(session, updated_models, **kwargs):
            return False
        logger.debug('_create ok')
        return True

    @classmethod
    def _create(
        cls: Type[ShopUnitProxyType],
        session: SessionType,
        updated_models: UpdateSet,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            raise ValueError('session is None')
        logger.debug('creating %s with %s', cls.__name__, kwargs)
        if kwargs.get('parentId') is not None:
            parent_model = cls.get_expect(session, id=kwargs['parentId'])
            if parent_model.type == ShopUnitType.OFFER:
                logger.debug('parent_model type is OFFER')
                return False

        kwargs['offers_count'] = (
            1 if kwargs['type'] == ShopUnitType.OFFER else 0
        )
        if not cls._update_price_in_tree(session, updated_models, kwargs):
            logger.debug('_update_price_in_tree failed')
            return False
        logger.debug('_update_price_in_tree ok')

        updated_models.add(json.dumps(kwargs))

        return super().create(session, **kwargs)

    def update(
        self: ShopUnitProxyType,
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            logger.debug('session is None')
            with create_session() as new_session:
                return self.update(new_session, **kwargs)
        updated_models = kwargs.get('updated_models')
        if updated_models is None:
            updated_models = UpdateSet()
        else:
            kwargs.pop('updated_models')
        if not self._update(session, updated_models, **kwargs):
            return False
        return True

    def _update(
        self: ShopUnitProxyType,
        session: SessionType,
        updated_models: UpdateSet,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            raise ValueError('session is None')

        if kwargs.get('parentId') is not None:
            parent_model = self.get(session, id=kwargs['parentId'])
            if parent_model is None:
                return False
            if parent_model.type == ShopUnitType.OFFER:
                return False

        kwargs['offers_count'] = self.offers_count
        cur_kwargs_dict = {
            'parentId': self.parentId,
            'offers_count': self.offers_count,
            'price': self.price,
        }
        if not self._update_price_in_tree(
            session, updated_models, kwargs, cur_kwargs_dict
        ):
            return False

        updated_models.add(self)

        return super().update(session, **kwargs)

    def update_now(
        self: ShopUnitProxyType,
        session: SessionType,
        updated_models: UpdateSet,
        **kwargs: Any,
    ) -> bool:
        updated_models.add(self)
        return super().update(session, **kwargs)

    def delete(self: ShopUnitProxyType, session: SessionType = None) -> bool:
        if session is None:
            with create_session() as new_session:
                if not self._delete(new_session):
                    return False
            return True
        logger.debug('session is not None')
        return False

    def _delete(self: ShopUnitProxyType, session: SessionType) -> bool:
        if session is None:
            raise ValueError('session is None')
        kwargs_dict = {
            'parentId': self.parentId,
            'offers_count': self.offers_count,
            'price': self.price,
        }
        if not self._update_delete_price(session, UpdateSet(), kwargs_dict):
            return False
        # TODO: delete stats by children

        return super().delete(session)

    @classmethod
    def _update_delete_price(
        cls: Type[ShopUnitProxyType],
        session: SessionType,
        updated_models: UpdateSet,
        was_kwargs: dict[str, Any],
        date: Optional[str] = None,
    ) -> bool:
        parent_id = was_kwargs['parentId']
        offers_count = was_kwargs['offers_count']
        price = was_kwargs['price']

        while parent_id:
            parent_model = cls.get_expect(session, id=parent_id)

            new_offers_count = parent_model.offers_count - offers_count
            was_price = parent_model.price
            new_avg_price = None
            if new_offers_count > 0:
                new_avg_price = (
                    was_price * parent_model.offers_count
                    - price * offers_count
                ) / new_offers_count
            if not parent_model.update_now(
                session,
                updated_models,
                price=new_avg_price,
                offers_count=new_offers_count,
            ):
                logger.debug(
                    'parent_model._update_now(%s, price=%s, offers_count=%s) failed',
                    session,
                    new_avg_price,
                    new_offers_count,
                )
                return False
            if date:
                if not parent_model.update_now(
                    session, updated_models, date=date
                ):
                    logger.debug(
                        'parent_model._update_now(%s, date=%s) failed',
                        session,
                        date,
                    )
                    return False
            parent_id = parent_model.parentId

        return True

    @classmethod
    def _update_price_in_tree(
        cls: Type[ShopUnitProxyType],
        session: SessionType,
        updated_models: UpdateSet,
        new_kwargs: dict[str, Any],
        was_kwargs: Optional[dict[str, Any]] = None,
    ) -> bool:
        parent_id = new_kwargs.get('parentId')
        if was_kwargs and parent_id != was_kwargs.get('parentId'):
            if not cls._update_delete_price(
                session, updated_models, was_kwargs, new_kwargs['date']
            ):
                logger.debug('_update_delete_price failed')
                return False
            was_kwargs = None

        is_update = was_kwargs is not None

        while parent_id:
            parent_model = cls.get_expect(session, id=parent_id)
            if not parent_model.update_now(
                session, updated_models, date=new_kwargs['date']
            ):
                logger.debug(
                    'parent_model.update_now(%s, date=%s) failed',
                    session,
                    new_kwargs['date'],
                )
                return False
            parent_id = parent_model.parentId

            if new_kwargs['offers_count'] <= 0:
                continue

            was_offers_count = parent_model.offers_count or 0
            new_offers_count = (
                was_offers_count
                if is_update
                else was_offers_count + new_kwargs['offers_count']
            )

            was_price = parent_model.price or 0
            new_sum_price = was_price * was_offers_count
            if new_kwargs['type'] == ShopUnitType.OFFER:
                new_sum_price += (
                    new_kwargs['price'] * new_kwargs['offers_count']
                )
                if was_kwargs is not None:
                    new_sum_price -= (
                        was_kwargs['price'] * was_kwargs['offers_count']
                    )
                new_avg_price = new_sum_price / new_offers_count
            else:
                if was_kwargs is not None:
                    new_sum_price += (
                        was_kwargs['price'] * was_kwargs['offers_count']
                    )
                    new_avg_price = new_sum_price / new_offers_count
                else:
                    new_avg_price = was_price

            if not parent_model.update_now(
                session,
                updated_models,
                price=new_avg_price,
                offers_count=new_offers_count,
            ):
                logger.debug(
                    'parent_model.update_now(%s, price=%s, offers_count=%s) failed',
                    session,
                    new_avg_price,
                    new_offers_count,
                )
                return False

        return True

    @classmethod
    def create_batch(
        cls, date: str, batch: list[ShopUnitImportSchema]
    ) -> bool:
        try:
            with create_session() as session:
                updated_models = UpdateSet()
                for item in batch:
                    logger.debug('Got new import item: %s', item)
                    model = ShopUnitProxy.get(session, id=item.id)
                    if model is None:
                        if ShopUnitProxy.create(
                            session,
                            updated_models=updated_models,
                            **item.dict(),
                            date=date,
                        ):
                            logger.debug('Created new import item: %s', item)
                            continue
                        logger.debug('Failed to create new item: %s', item)
                        raise TypeError('Failed to create item')

                    if model.type != item.type:
                        logger.debug('Item type mismatch: %s', item)
                        raise TypeError('Item type mismatch')
                    if model.update(
                        session,
                        updated_models=updated_models,
                        **item.dict(),
                        date=date,
                    ):
                        logger.debug('Updated import item: %s', item)
                        continue
                    logger.debug('Failed to update item: %s', item)
                    raise TypeError('Failed to update item')
                if not cls._create_statistics(session, updated_models):
                    raise TypeError('Failed _create_statistics')
        except TypeError:
            logger.exception('Failed to import')
            return False
        return True


ShopUnitStatisticUnitProxyType = TypeVar(
    'ShopUnitStatisticUnitProxyType', bound='ShopUnitStatisticUnitProxy'
)


class ShopUnitStatisticUnitProxy(BaseProxy):
    BASE_MODEL = ShopUnitStatisticUnit
    SCHEMA_MODEL = ShopUnitStatisticUnitSchema
    ATTRS = ['id', 'name', 'type', 'price', 'parentId', 'date']

    def __init__(
        self, shop_unit_statistic_unit: ShopUnitStatisticUnit
    ) -> None:
        super().__init__(shop_unit_statistic_unit)
        self.id = shop_unit_statistic_unit.id
        self.name = shop_unit_statistic_unit.name
        self.type = shop_unit_statistic_unit.type
        self.price = shop_unit_statistic_unit.price
        self.parentId = shop_unit_statistic_unit.parentId
        self.date = shop_unit_statistic_unit.date

    @classmethod
    def get_all_filter(
        cls,
        item_id: str,
        date_start: dt.datetime,
        date_end: dt.datetime,
        session: SessionType = None,
    ) -> list['ShopUnitStatisticUnitProxy']:
        if session is None:
            with create_session() as new_session:
                return cls.get_all_filter(
                    item_id, date_start, date_end, new_session
                )
        data = []
        for model in (
            session.query(cls.BASE_MODEL)
            .filter(
                cls.BASE_MODEL.id == item_id,
                cls.BASE_MODEL.date >= date_start,
                cls.BASE_MODEL.date < date_end,
            )
            .all()
        ):
            data.append(cls(model))
        return data

    @classmethod
    def delete_all_by_id(cls, session: SessionType, item_id: str) -> bool:
        if session is None:
            with create_session() as new_session:
                return cls.delete_all_by_id(new_session, item_id)
        session.query(cls.BASE_MODEL).filter_by(id=item_id).delete()
        return True
