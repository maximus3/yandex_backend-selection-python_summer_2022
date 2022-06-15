from typing import Any, Optional

from app.utils import datetime_to_iso_8601, iso_8601_to_datetime
from database.shop_unit_type import ShopUnitType


def date_must_be_iso_8601(value: str) -> str:
    try:
        dt_format = iso_8601_to_datetime(value)
        if datetime_to_iso_8601(dt_format) != value:
            raise ValueError()
    except ValueError as exc:
        raise ValueError('date must be in ISO 8601 format') from exc
    return value


def validate_price(
    value: Optional[int], values: dict[str, Any]
) -> Optional[int]:
    obj_type = values['type']

    if obj_type == ShopUnitType.OFFER and value is None:
        raise ValueError('price is required for OFFER')
    if obj_type == ShopUnitType.CATEGORY and value is not None:
        raise ValueError('price is not required for CATEGORY')

    if value is not None and value < 0:
        raise ValueError('price must be >= 0')

    return value
