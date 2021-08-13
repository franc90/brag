import sys
from argparse import Namespace
from datetime import datetime, timedelta

from pyfzf import FzfPrompt

from datastore import DataStore


class Note:

    @staticmethod
    def __get_work_date():
        today = datetime.today()
        if today.time().hour < 6:  # is still yesterday by work standards (before 6am)
            return today - timedelta(days=1)
        else:
            return today

    @staticmethod
    def create(args: Namespace):
        file_name = Note.__get_work_date().strftime('%Y%m%d')
        if args.name:
            file_name = f'{file_name}_{"-".join(args.name)}'

        if DataStore.note_exists(file_name):
            sys.stdout.write(f'Note "{file_name}" already exist. Open? [y/n] ')
            choice = input().lower()
            if choice not in ['', 'y', 'ye', 'yes']:
                sys.exit(0)
        DataStore.edit_note(file_name)

    @staticmethod
    def show(args: Namespace):
        matching_notes = [
            note_file.name
            for note_file in DataStore.iter_notes()
            if not args.name or args.name in note_file.name
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
                print(f"WARN: Terminating because no note was selected.")
                sys.exit(1)
        else:
            note = matching_notes[0]

        DataStore.edit_note(note)
