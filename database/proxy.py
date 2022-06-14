from typing import Any, Optional, Type, TypeVar

from sqlalchemy.orm import Session as SessionType

from database import create_session
from database.models import BaseModel, ShopUnit
from database.schemas import BaseModel as SchemaBaseModel
from database.schemas import ShopUnitSchema

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
        return self.id == other.id

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'

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
                    return model
                if not cls.create(new_session, **kwargs):
                    return None
            with create_session() as new_session:
                return cls.get(new_session, **kwargs)
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
    ) -> Optional[BaseProxyType]:
        if session is None:
            with create_session() as new_session:
                return self.update(new_session, **kwargs)
        model = (
            session.query(self.BASE_MODEL).filter_by(id=self.id).one_or_none()
        )
        if model is None:
            return None
        for key, value in kwargs.items():
            if hasattr(model, key) and hasattr(self, key):
                setattr(model, key, value)
                setattr(self, key, value)
            else:
                return None
        session.add(model)
        return self

    def get_me(self: BaseProxyType, session: SessionType) -> BaseModel:
        return session.query(self.BASE_MODEL).get(self.id)


class ShopUnitProxy(BaseProxy):
    BASE_MODEL = ShopUnit
    SCHEMA_MODEL = ShopUnitSchema

    def __init__(self, shop_unit: ShopUnit) -> None:
        super().__init__(shop_unit)
        self.id = shop_unit.id
        self.name = shop_unit.name
        self.type = shop_unit.type
        self.price = shop_unit.price
        self.parentId = shop_unit.id
        self.date = shop_unit.date

        self.children = [ShopUnitProxy(unit) for unit in shop_unit.children]
