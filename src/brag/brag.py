from argparse import ArgumentParser

from brag.notes import Notes


class Brag:

    def __init__(self):
        self.__parser = self.__create_argument_parser()
        self.__args = self.__parser.parse_args()
        self.__notes = Notes(self.__args)
        self.__commands = {
            'new': self.__notes.create, 'n': self.__notes.create,
            'list': self.__notes.list, 'l': self.__notes.list,
            'edit': self.__notes.edit, 'e': self.__notes.edit,
            'data_dir': self.__notes.open_store, 'dd': self.__notes.open_store,
        }

    @staticmethod
    def __new_note_parser(parser):
        parser.add_argument('name', nargs='*', help='note name')

    @staticmethod
    def __list_notes_parser(parser):
        parser.add_argument('texts', nargs='*', help='note name must contain these texts')
        parser.add_argument('-c', '--combine', dest='combine', action='store_true',
                            help='combine selected notes into a single file')
        parser.add_argument('-y', '--yesterday', dest='yesterday', action='store_true',
                            help='show only yesterday notes')
        parser.add_argument('-s', '--since', dest='since', help='date (YYYYMMDD) since when to combine notes')
        parser.add_argument('-t', '--to', dest='to', help='date (YYYYMMDD) till when to combine notes')
        parser.add_argument('-o', '--output', dest='output', help='output file')

    def __create_argument_parser(self) -> ArgumentParser:
        parser = ArgumentParser(prog='brag', description="Brag about work you've done today.")
        subparsers = parser.add_subparsers(dest='command')

        self.__new_note_parser(subparsers.add_parser('new', aliases=['n'], help='create a new note'))
        self.__list_notes_parser(subparsers.add_parser('list', aliases=['l'], help='list selected note(s) content'))
        self.__list_notes_parser(subparsers.add_parser('edit', aliases=['e'], help='edit selected note'))
        subparsers.add_parser('data_dir', aliases=['dd'], help='open directory where notes are stored')

        return parser

    def run(self):
        if self.__args.command:
            self.__commands[self.__args.command]()
        else:
            self.__parser.print_help()
