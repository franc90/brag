from argparse import ArgumentParser


def new_note_parser(parser):
    parser.add_argument('name', nargs='*', help="note name")


def show_note_parser(parser):
    parser.add_argument('text', nargs='?', help="note name must contain this text")


def create_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="brag", description="Brag about work you've done today.")
    subparsers = parser.add_subparsers(dest='command')

    new_note_parser(subparsers.add_parser('n', help='new note'))
    show_note_parser(subparsers.add_parser('s', help='show note'))

    return parser
