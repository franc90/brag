import os
import subprocess
from pathlib import Path
from typing import Iterator

from brag.store.filters import Filter


class FileDataStore:

    def __init__(self):
        self.__open = os.getenv('BRAG_OPEN', 'xdg-open')
        self.__editor = os.getenv('BRAG_EDITOR', 'subl')
        data_home = Path(os.getenv('XDG_DATA_HOME', Path.home()))
        self.store = data_home / 'brag' / 'userdata'
        self.store.mkdir(parents=True, exist_ok=True)

    def find_matching_note_names(self, filters: Iterator[Filter]):
        return [
            note_name
            for note_name in self.__iter_note_names()
            if all(note_filter.matches(note_name) for note_filter in filters)
        ]

    def __iter_note_names(self) -> Iterator[str]:
        for file in self.store.iterdir():
            if file.is_file():
                yield file.name

    def note_exists(self, filename: str) -> bool:
        file = self.store / filename
        return file.exists()

    def edit_note(self, filename: str):
        file = self.store / filename
        subprocess.call([self.__editor, file])

    def load_note(self, filename: str) -> str:
        file = self.store / filename
        return file.read_text()

    def open_store(self):
        subprocess.call([self.__open, self.store])
