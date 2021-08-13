import os
from pathlib import Path

EDITOR = os.getenv('BRAG_EDITOR', 'subl')
DATA_HOME = Path(os.getenv('XDG_DATA_HOME', Path.home()))
BRAG_DATA_DIR = DATA_HOME / 'brag' / 'userdata'


def setup():
    BRAG_DATA_DIR.mkdir(parents=True, exist_ok=True)
