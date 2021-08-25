from brag.cmdlineargparser import CmdLineArgParser
from brag.notes import Notes


def main():
    """Entry point for the application script"""
    parser = CmdLineArgParser().create_argument_parser()
    args = parser.parse_args()
    notes = Notes(args)

    cmd = {
        'new': notes.create, 'n': notes.create,
        'list': notes.list, 'l': notes.list,
        'edit': notes.edit, 'e': notes.edit,
        'search': notes.search, 's': notes.search,
        'data_dir': notes.open_store, 'dd': notes.open_store,
    }.get(args.command, parser.print_help)
    cmd()
