import sys
from argparse import Namespace
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator, List

from brag.date import date_to_string
from brag.store.filedatastore import FileDataStore
from brag.store.filters import Filters
from pyfzf import FzfPrompt


class Notes:

    def __init__(self, args: Namespace):
        self.args = args
        self.data_store = FileDataStore()

    def open_store(self):
        self.data_store.open_store()

    def create(self):
        file_name = date_to_string(self.__get_work_date())
        if self.args.name:
            file_name = f'{file_name}_{"-".join(self.args.name)}'

        if self.data_store.note_exists(file_name):
            self.__confirm_or_exit(f'Note "{file_name}" already exist. Open? [y/n] ')
        self.data_store.edit_note(file_name)

    @staticmethod
    def __get_work_date() -> datetime:
        today = datetime.today()
        if today.time().hour < 6:  # is still yesterday by work standards (before 6am)
            return today - timedelta(days=1)
        else:
            return today

    def list(self):
        filters = Filters.create_filters(self.args)
        matching_notes = self.data_store.find_matching_note_names(filters)

        if len(matching_notes) == 0:
            print('No matching note found. :(')
            sys.exit(1)
        elif self.args.combine:
            notes = self.__combine_notes(matching_notes)
            self.print_notes(notes)
        elif len(matching_notes) > 1:
            try:
                matching_notes.sort(reverse=True)
                chosen = FzfPrompt().prompt(
                    choices=matching_notes,
                    fzf_options='-m --layout=reverse --bind ctrl-a:select-all,ctrl-d:deselect-all,ctrl-t:toggle-all'
                )
                notes = self.__combine_notes(chosen)
                self.print_notes(notes)
            except:
                print('WARN: Terminating because no note was selected.')
                sys.exit(1)
        else:
            note = self.data_store.load_note(matching_notes[0])
            self.print_notes([note])

    def print_notes(self, notes: List[str]):
        if self.args.output:
            out_file = Path(self.args.output)
            if out_file.exists():
                self.__confirm_or_exit(f'File "{self.args.output}" already exist. Override? [y/n] ')
            with out_file.open(mode='w') as f:
                for note in notes:
                    f.write(note)
        else:
            for note in notes:
                print(note)

    def __combine_notes(self, matching_notes: List[str]) -> Iterator[str]:
        matching_notes.sort()
        for file_name in matching_notes:
            note = self.data_store.load_note(file_name).strip()
            if len(note) == 0:
                continue
            yield f'###### {file_name}:\n{note}\n\n'

    def edit(self):
        filters = Filters.create_filters(self.args)
        matching_notes = self.data_store.find_matching_note_names(filters)

        if len(matching_notes) == 0:
            print('No matching note found. :(')
            sys.exit(1)
        elif len(matching_notes) == 1:
            self.data_store.edit_note(matching_notes[0])
        else:
            try:
                matching_notes.sort(reverse=True)  # show youngest first
                chosen = FzfPrompt().prompt(choices=matching_notes, fzf_options='--layout=reverse')
                self.data_store.edit_note(chosen[0])
            except:
                print('WARN: Terminating because no note was selected.')
                sys.exit(1)

    @staticmethod
    def __confirm_or_exit(msg: str):
        sys.stdout.write(msg)
        choice = input().lower()
        if choice not in ['', 'y', 'ye', 'yes']:
            sys.exit(0)
