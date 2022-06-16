import datetime as dt
from typing import Any, Optional, Union

from pydantic import BaseModel, validator

from database import validators
from database.shop_unit_type import ShopUnitType


class ShopUnitSchema(BaseModel):
    id: str
    name: str
    date: str
    parentId: Optional[str]
    type: ShopUnitType
    price: Optional[int]
    children: Optional[list['ShopUnitSchema']]

    @validator('children', always=True)
    def validate_children(
        cls, value: Optional[list['ShopUnitSchema']], values: dict[str, Any]
    ) -> Optional[list['ShopUnitSchema']]:
        obj_type = values['type']

        if obj_type == ShopUnitType.OFFER:
            return None

        return value or []

    class Config:
        orm_mode = True


class ShopUnitImportSchema(BaseModel):
    id: str
    name: str
    parentId: Optional[str]
    type: ShopUnitType
    price: Optional[int]

    @validator('price', always=True)
    def validate_price(
        cls, value: Optional[int], values: dict[str, Any]
    ) -> Optional[int]:
        return validators.validate_price(value, values)


class ShopUnitImportRequestSchema(BaseModel):
    items: list[ShopUnitImportSchema]
    updateDate: str

    @validator('updateDate')
    def dvalidator_date(cls, value: str) -> str:
        return validators.date_must_be_iso_8601(value)


class ShopUnitStatisticUnitSchema(BaseModel):
    id: str
    name: str
    date: Union[str, dt.datetime]
    parentId: Optional[str]
    type: ShopUnitType
    price: Optional[int]

    @validator('date')
    def dvalidator_date(cls, value: Union[str, dt.datetime]) -> str:
        return validators.date_to_iso_8601(value)

    class Config:
        orm_mode = True


class ShopUnitStatisticResponseSchema(BaseModel):
    items: list[ShopUnitStatisticUnitSchema]


class ErrorScheme(BaseModel):
    message: str
    code: int
