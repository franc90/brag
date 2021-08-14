import os
import subprocess
from pathlib import Path
from typing import Iterator


class DataStore:

    def __init__(self):
        self.__open = os.getenv('BRAG_OPEN', 'xdg-open')
        self.__editor = os.getenv('BRAG_EDITOR', 'subl')
        data_home = Path(os.getenv('XDG_DATA_HOME', Path.home()))
        self.store = data_home / 'brag' / 'userdata'
        self.store.mkdir(parents=True, exist_ok=True)

    def iter_notes(self) -> Iterator[Path]:
        for file in self.store.iterdir():
            if file.is_file():
                yield file

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
