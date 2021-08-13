import subprocess
from pathlib import Path
from typing import Iterator

from common import BRAG_DATA_DIR, EDITOR


class DataStore:

    @staticmethod
    def iter_notes() -> Iterator[Path]:
        for file in BRAG_DATA_DIR.iterdir():
            if file.is_file():
                yield file

    @staticmethod
    def note_exists(filename: str) -> bool:
        file = BRAG_DATA_DIR / filename
        return file.exists()

    @staticmethod
    def edit_note(filename: str):
        file = BRAG_DATA_DIR / filename
        subprocess.call([EDITOR, file])
