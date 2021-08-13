from argparse import ArgumentParser

from notes import Notes


class CmdLineArguments:

    def __init__(self):
        self.__parser = self.__create_argument_parser()
        self.__args = self.__parser.parse_args()

    @staticmethod
    def __new_note_parser(parser):
        parser.add_argument('name', nargs='*', help="note name")

    @staticmethod
    def __show_note_parser(parser):
        parser.add_argument('text', nargs='?', help="note name must contain this text")

    def __create_argument_parser(self) -> ArgumentParser:
        parser = ArgumentParser(prog="brag", description="Brag about work you've done today.")
        subparsers = parser.add_subparsers(dest='command')

        self.__new_note_parser(subparsers.add_parser('n', help='new note'))
        self.__show_note_parser(subparsers.add_parser('s', help='show note'))

        return parser

    def print_help(self):
        self.__parser.print_help()

    def handle(self, notes: Notes):
        if self.__args.command:
            notes.exec(self.__args)
        else:
            self.__parser.print_help()
