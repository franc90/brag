import sys
from argparse import Namespace
from datetime import datetime, timedelta

from pyfzf import FzfPrompt

from datastore import DataStore


class Notes:

    def __init__(self):
        self.data_store = DataStore()

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
            fzf = FzfPrompt()
            try:
                matching_notes.sort(reverse=True)
                choosen = fzf.prompt(choices=matching_notes)
                note = choosen[0]
            except:
                print(f"WARN: Terminating because no note was selected.")
                sys.exit(1)
        else:
            note = matching_notes[0]

        self.data_store.edit_note(note)
