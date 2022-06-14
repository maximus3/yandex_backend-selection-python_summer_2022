import datetime as dt


def iso_8601_to_datetime(date_str: str) -> dt.datetime:
    return dt.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')


def datetime_to_iso_8601(date_obj: dt.datetime) -> str:
    return date_obj.isoformat() + '.000Z'
