import subprocess
from datetime import datetime, timedelta
from typing import List

from brag.date import date_to_string, get_previous_work_day


class Filter:
    def matches(self, name: str) -> bool:
        pass


class SinceFilter(Filter):
    def __init__(self, since: str):
        self.__since = since

    @staticmethod
    def create(yesterday: bool, since: str):
        if yesterday:
            return SinceFilter(date_to_string(get_previous_work_day(datetime.today())))
        elif since:
            return SinceFilter(since)
        else:
            return None

    def matches(self, name: str) -> bool:
        return name >= self.__since


class ToFilter(Filter):
    def __init__(self, to: str):
        self.__to = f'{to}z'

    @staticmethod
    def create(yesterday: bool, to: str):
        if yesterday:
            return ToFilter(date_to_string(datetime.today() - timedelta(days=1)))
        elif to:
            return ToFilter(to)
        else:
            return None

    def matches(self, name: str) -> bool:
        return name <= self.__to


class NameFilter(Filter):
    def __init__(self, texts: List[str]):
        self.__texts = texts

    @staticmethod
    def create(texts: List[str]):
        if texts:
            return NameFilter(texts)
        return None

    def matches(self, name: str) -> bool:
        for text in self.__texts:
            if text not in name:
                return False
        return True


class ContentFilter(Filter):
    def __init__(self, patterns: List[str], invert_match: bool, data_store):
        self.__patterns = patterns
        self.__invert_match = invert_match
        self.__data_store = data_store

    @staticmethod
    def create(patterns: List[str], invert_match: bool, data_store):
        if patterns:
            return ContentFilter(patterns, invert_match, data_store)
        return None

    def matches(self, name: str) -> bool:
        args = ['grep', '-q'] + self.__patterns + [self.__data_store / name]
        if subprocess.call(args) == 1:
            return self.__invert_match  # True if filter out matching
        return not self.__invert_match  # False if filter out matching


class Filters:

    @staticmethod
    def create_filters(*filters) -> List[Filter]:
        return list(filter(None, filters))
