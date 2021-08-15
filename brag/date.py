from datetime import datetime


def date_to_string(date: datetime) -> str:
    return date.strftime('%Y%m%d')