from argparse import Namespace
from datetime import datetime, timedelta
from typing import List

from brag.date import date_to_string


class Filter:
    def matches(self, name: str) -> bool:
        pass


class SinceFilter(Filter):
    def __init__(self, since: str):
        self.__since = since

    @staticmethod
    def create(yesterday: bool, since: str):
        if yesterday:
            return SinceFilter(date_to_string(datetime.today() - timedelta(days=1)))
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


class Filters:

    @staticmethod
    def create_filters(args: Namespace) -> List[Filter]:
        filters = [
            NameFilter.create(args.texts),
            SinceFilter.create(args.yesterday, args.since),
            ToFilter.create(args.yesterday, args.to),
        ]
        return list(filter(None, filters))
