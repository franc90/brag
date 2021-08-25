from datetime import datetime, timedelta


def date_to_string(date: datetime) -> str:
    return date.strftime('%Y-%m-%d')


def get_previous_work_day(date: datetime) -> datetime:
    if date.weekday() == 0:  # is it Monday
        return date - timedelta(days=3)
    else:
        return date - timedelta(days=1)
