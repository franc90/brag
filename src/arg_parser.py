from argparse import ArgumentParser


def create_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="brag", description="Brag about work you've done today.")
    subparsers = parser.add_subparsers(dest='command')

    new_note_parser = subparsers.add_parser('new')
    new_note_parser.add_argument('name', nargs='*', )

    show_note_parse = subparsers.add_parser('show')
    show_note_parse.add_argument('name', nargs='?')

    return parser
