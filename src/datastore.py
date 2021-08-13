import os
import subprocess
from pathlib import Path
from typing import Iterator


class DataStore:

    def __init__(self):
        self.__editor = os.getenv('BRAG_EDITOR', 'subl')
        data_home = Path(os.getenv('XDG_DATA_HOME', Path.home()))
        self.__data_dir = data_home / 'brag' / 'userdata'
        self.__data_dir.mkdir(parents=True, exist_ok=True)

    def iter_notes(self) -> Iterator[Path]:
        for file in self.__data_dir.iterdir():
            if file.is_file():
                yield file

    def note_exists(self, filename: str) -> bool:
        file = self.__data_dir / filename
        return file.exists()

    def edit_note(self, filename: str):
        file = self.__data_dir / filename
        subprocess.call([self.__editor, file])
