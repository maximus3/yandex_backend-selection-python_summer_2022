from enum import Enum, unique


@unique
class ShopUnitType(str, Enum):
    OFFER = 'OFFER'
    CATEGORY = 'CATEGORY'
