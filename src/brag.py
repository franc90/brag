from argparse import ArgumentParser

from notes import Notes


class Brag:

    def __init__(self):
        self.__notes = Notes()
        self.__parser = self.__create_argument_parser()
        self.__args = self.__parser.parse_args()
        self.__commands = {
            'new': self.__notes.create, 'n': self.__notes.create,
            'list': self.__notes.show, 'l': self.__notes.show,
            'combine': self.__notes.combine, 'c': self.__notes.combine,
            'data_dir': self.__notes.open_store, 'dd': self.__notes.open_store,
        }

    @staticmethod
    def __new_note_parser(parser):
        parser.add_argument('name', nargs='*', help='note name')

    @staticmethod
    def __show_note_parser(parser):
        parser.add_argument('text', nargs='?', help='note name must contain this text')

    @staticmethod
    def __combine_notes_parser(parser):
        parser.add_argument('text', nargs='?', help='note name must contain this text')
        parser.add_argument('-o', '--output', dest='output', help='output file')
        parser.add_argument('-s', '--since', dest='since', help='date (YYYYMMDD) since when to combine notes')
        parser.add_argument('-t', '--to', dest='to', help='date (YYYYMMDD) till when to combine notes')

    def __create_argument_parser(self) -> ArgumentParser:
        parser = ArgumentParser(prog='brag', description="Brag about work you've done today.")
        subparsers = parser.add_subparsers(dest='command')

        self.__new_note_parser(subparsers.add_parser('new', aliases=['n'], help='create a new note'))
        self.__show_note_parser(subparsers.add_parser('list', aliases=['l'], help='list specific note content'))
        self.__combine_notes_parser(
            subparsers.add_parser('combine', aliases=['c'], help='combine notes into one big note'))
        subparsers.add_parser('data_dir', aliases=['dd'], help='open directory where data is stored')

        return parser

    def run(self):
        if self.__args.command:
            self.__commands[self.__args.command](self.__args)
        else:
            self.__parser.print_help()


if __name__ == '__main__':
    Brag().run()
