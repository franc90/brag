#!/usr/bin/env python

import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from pathlib import Path

from pyfzf.pyfzf import FzfPrompt

XDG_DATA_HOME = Path(os.getenv('XDG_DATA_HOME', Path.home()))
BRAG_DATA_DIR = XDG_DATA_HOME / 'brag' / 'userdata'
EDITOR = 'subl'

BRAG_DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_work_date():
    today = datetime.today()
    if today.time().hour < 6:  # if still yesterday by work standards (before 6am)
        return today - timedelta(days=1)
    else:
        return today


def create_new_note(args: Namespace):
    name = get_work_date().strftime('%Y%m%d')
    if args.name:
        name = f'{name}_{"-".join(args.name)}'
    note = BRAG_DATA_DIR / name
    if note.exists():
        print(f'Opening existing note {note}')
    else:
        note.touch()
        print(f'Created a new note: {note}')
    subprocess.call([EDITOR, note])


def show_note(args: Namespace):
    matching_notes = [
        file.name
        for file in BRAG_DATA_DIR.iterdir()
        if file.is_file()
        if not args.name or args.name in file.name
    ]

    if len(matching_notes) == 0:
        print(f"No note contains '{args.name}' in its name. :(")
        sys.exit(1)
    elif len(matching_notes) > 1:
        fzf = FzfPrompt()
        try:
            matching_notes.sort(reverse=True)
            choosen = fzf.prompt(choices=matching_notes)
            note = choosen[0]
        except:
            print(f"No note selected. Terminating.")
            sys.exit(1)
    else:
        note = matching_notes[0]

    subprocess.call([EDITOR, BRAG_DATA_DIR / note])


FUNCTIONS = {
    'new': create_new_note,
    'show': show_note,
}

parser = ArgumentParser(description="Brag about work you've done today.")
subparsers = parser.add_subparsers(dest='command')

new_note_parser = subparsers.add_parser('new')
new_note_parser.add_argument('name', nargs='*', )

show_note_parse = subparsers.add_parser('show')
show_note_parse.add_argument('name', nargs='?')

args = parser.parse_args()

if args.command:
    FUNCTIONS[args.command](args)
else:
    parser.print_help()
