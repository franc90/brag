import sys
from argparse import Namespace
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator

from pyfzf import FzfPrompt

from datastore import DataStore


class Notes:

    def __init__(self):
        self.data_store = DataStore()

    def open_store(self, _: Namespace):
        self.data_store.open_store()

    def create(self, args: Namespace):
        file_name = self.__get_work_date().strftime('%Y%m%d')
        if args.name:
            file_name = f'{file_name}_{"-".join(args.name)}'

        if self.data_store.note_exists(file_name):
            sys.stdout.write(f'Note "{file_name}" already exist. Open? [y/n] ')
            choice = input().lower()
            if choice not in ['', 'y', 'ye', 'yes']:
                sys.exit(0)
        self.data_store.edit_note(file_name)

    @staticmethod
    def __get_work_date():
        today = datetime.today()
        if today.time().hour < 6:  # is still yesterday by work standards (before 6am)
            return today - timedelta(days=1)
        else:
            return today

    def show(self, args: Namespace):
        matching_notes = [
            note_file.name
            for note_file in self.data_store.iter_notes()
            if not args.text or args.text in note_file.name
        ]

        if len(matching_notes) == 0:
            print(f"No note contains '{args.text}' in its name. :(")
            sys.exit(1)
        elif len(matching_notes) > 1:
            try:
                matching_notes.sort(reverse=True)
                chosen = FzfPrompt().prompt(choices=matching_notes)
                note = chosen[0]
            except:
                print(f"WARN: Terminating because no note was selected.")
                sys.exit(1)
        else:
            note = matching_notes[0]

        self.data_store.edit_note(note)

    def combine(self, args: Namespace):
        matching_notes = [
            note_file.name
            for note_file in self.data_store.iter_notes()
            if not args.text or args.text in note_file.name
        ]
        matching_notes.sort()

        if len(matching_notes) == 0:
            print(f"No note selected")
            sys.exit(0)

        with Path(args.output).open(mode='w') as f:
            for note in self.combine_notes(matching_notes):
                f.write(note)

    def combine_notes(self, matching_notes) -> Iterator[str]:
        for file_name in matching_notes:
            note = self.data_store.load_note(file_name).strip()
            if len(note) == 0:
                continue
            yield f"###### {file_name}:\n{note}\n\n"
