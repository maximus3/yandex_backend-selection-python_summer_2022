import datetime as dt


def iso_8601_to_datetime(date_str: str) -> dt.datetime:
    date_str = date_str.lower()
    if date_str[-1] == 'z':
        date_str = date_str[:-1] + '+00:00'
    return dt.datetime.fromisoformat(date_str)


def datetime_to_iso_8601(date_obj: dt.datetime) -> str:
    date_str = date_obj.isoformat()
    if date_str.endswith('+00:00'):
        date_str = date_str[:-6]
    return date_str + '.000Z'
