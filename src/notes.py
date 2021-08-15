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
        file_name = self.__date_to_string(self.__get_work_date())
        if args.name:
            file_name = f'{file_name}_{"-".join(args.name)}'

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

    def list(self, args: Namespace):
        matching_notes = self.__find_matching_notes(args)

        if len(matching_notes) == 0:
            print(f"No matching note found. :(")
            sys.exit(1)
        elif args.combine:
            matching_notes.sort()  # show oldest first
            notes = self.__combine_notes(matching_notes)
            if args.output:
                out_file = Path(args.output)
                if out_file.exists():
                    self.__confirm_or_exit(f'File "{args.output}" already exist. Override? [y/n] ')
                with out_file.open(mode='w') as f:
                    for note in notes:
                        f.write(note)
            else:
                for note in notes:
                    print(note)
        elif len(matching_notes) == 1:
            self.data_store.edit_note(matching_notes[0])
        else:
            try:
                matching_notes.sort(reverse=True)  # show youngest first
                chosen = FzfPrompt().prompt(choices=matching_notes)
                self.data_store.edit_note(chosen[0])
            except:
                print(f"WARN: Terminating because no note was selected.")
                sys.exit(1)

    def __find_matching_notes(self, args: Namespace):
        if args.yesterday:
            since = self.__date_to_string(datetime.today() - timedelta(days=1))
        elif args.since:
            since = args.since
        else:
            since = None

        if args.yesterday:
            to = f'{self.__date_to_string((datetime.today() - timedelta(days=1)))}Z'
        elif args.to:
            to = f'{args.to}Z'
        else:
            to = None

        return [
            note_file.name
            for note_file in self.data_store.iter_notes()
            if (self.__note_name_contains_all_texts(args, note_file)) and
               (not since or note_file.name >= since) and
               (not to or note_file.name <= to)
        ]

    @staticmethod
    def __note_name_contains_all_texts(args: Namespace, note_file: Path) -> bool:
        for text in args.texts:
            if text not in note_file.name:
                return False
        return True

    def __combine_notes(self, matching_notes) -> Iterator[str]:
        for file_name in matching_notes:
            note = self.data_store.load_note(file_name).strip()
            if len(note) == 0:
                continue
            yield f"###### {file_name}:\n{note}\n\n"

    @staticmethod
    def __confirm_or_exit(msg: str):
        sys.stdout.write(msg)
        choice = input().lower()
        if choice not in ['', 'y', 'ye', 'yes']:
            sys.exit(0)

    @staticmethod
    def __date_to_string(date: datetime) -> str:
        return date.strftime('%Y%m%d')
