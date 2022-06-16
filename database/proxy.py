import logging
from typing import Any, Optional, Type, TypeVar

from sqlalchemy.orm import Session as SessionType

from database import create_session
from database.models import BaseModel, ShopUnit
from database.schemas import BaseModel as SchemaBaseModel
from database.schemas import ShopUnitSchema
from database.shop_unit_type import ShopUnitType

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
            if not cls.create(**kwargs):
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

    @classmethod
    def create(
        cls: Type[ShopUnitProxyType],
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            with create_session() as new_session:
                logger.debug('_create with %s', kwargs)
                if not cls._create(new_session, **kwargs):
                    return False
            return True
        logger.debug('session is not None')
        return False

    @classmethod
    def _create(
        cls: Type[ShopUnitProxyType],
        session: SessionType,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            raise ValueError('session is None')
        logger.debug('creating %s with %s', cls.__name__, kwargs)
        if kwargs.get('parentId') is not None:
            parent_model = cls.get(session, id=kwargs['parentId'])
            if parent_model is None:
                return False
            if parent_model.type == ShopUnitType.OFFER:
                return False

        kwargs['offers_count'] = (
            1 if kwargs['type'] == ShopUnitType.OFFER else 0
        )
        if not cls._update_price_in_tree(session, kwargs):
            return False

        return super().create(session, **kwargs)

    def update(
        self: ShopUnitProxyType,
        session: SessionType = None,
        **kwargs: Any,
    ) -> bool:
        if session is None:
            with create_session() as new_session:
                if not self._update(new_session, **kwargs):
                    return False
            return True
        logger.debug('session is not None')
        return False

    def _update(
        self: ShopUnitProxyType,
        session: SessionType,
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
        if not self._update_price_in_tree(session, kwargs, cur_kwargs_dict):
            return False

        return super().update(session, **kwargs)

    def update_now(
        self: ShopUnitProxyType,
        session: SessionType,
        **kwargs: Any,
    ) -> bool:
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
        if not self._update_delete_price(session, kwargs_dict):
            return False

        return super().delete(session)

    @classmethod
    def _update_delete_price(
        cls: Type[ShopUnitProxyType],
        session: SessionType,
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
                if not parent_model.update_now(session, date=date):
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
        new_kwargs: dict[str, Any],
        was_kwargs: Optional[dict[str, Any]] = None,
    ) -> bool:
        parent_id = new_kwargs['parentId']
        if was_kwargs and parent_id != was_kwargs['parentId']:
            if not cls._update_delete_price(
                session, was_kwargs, new_kwargs['date']
            ):
                logger.debug('_update_delete_price failed')
                return False
            was_kwargs = None

        is_update = was_kwargs is not None

        while parent_id:
            parent_model = cls.get_expect(session, id=parent_id)
            if not parent_model.update_now(session, date=new_kwargs['date']):
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
                session, price=new_avg_price, offers_count=new_offers_count
            ):
                logger.debug(
                    'parent_model.update_now(%s, price=%s, offers_count=%s) failed',
                    session,
                    new_avg_price,
                    new_offers_count,
                )
                return False

        return True
