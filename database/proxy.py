import logging
from typing import Any, Optional, Type, TypeVar

from sqlalchemy.orm import Session as SessionType

from database import create_session
from database.models import BaseModel, ShopUnit
from database.proxy_utils import update_delete_price, update_price
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

        if not update_price(False, cls, session, **kwargs):
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

        if not update_price(True, self, session, **kwargs):
            return False

        return super().update(session, **kwargs)

    def _update_now(
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
        if not update_delete_price(
            session,
            self,
            self.parentId,
            None,
            self.type == ShopUnitType.OFFER,
            self.offers_count,
            self.price,
        ):
            return False

        return super().delete(session)
