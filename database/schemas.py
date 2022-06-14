import datetime as dt
from enum import Enum, unique
from typing import Optional

from pydantic import BaseModel

# class User(UserBase):
#     class Config:
#         orm_mode = True


@unique
class ShopUnitType(Enum):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'


class ShopUnitSchema(BaseModel):
    id: str
    name: str
    date: dt.datetime
    parentId: Optional[str]
    type: ShopUnitType
    price: Optional[int]
    children: Optional[list['ShopUnitSchema']]

    class Config:
        orm_mode = True


class ShopUnitImportSchema(BaseModel):
    id: str
    name: str
    parentId: Optional[str]
    type: ShopUnitType
    price: Optional[int]


class ShopUnitImportRequestSchema(BaseModel):
    items: list[ShopUnitImportSchema]
    updateDate: dt.datetime


class ShopUnitStatisticUnitSchema(BaseModel):
    id: str
    name: str
    date: dt.datetime
    parentId: Optional[str]
    type: ShopUnitType
    price: Optional[int]


class ShopUnitStatisticResponseSchema(BaseModel):
    items: list[ShopUnitStatisticUnitSchema]


class ErrorScheme(BaseModel):
    message: str
    code: int
