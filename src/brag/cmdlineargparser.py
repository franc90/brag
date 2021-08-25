from argparse import ArgumentParser


class CmdLineArgParser:

    def create_argument_parser(self) -> ArgumentParser:
        parser = ArgumentParser(prog='brag', description="Brag about work you've done today.")
        subparsers = parser.add_subparsers(dest='command')

        new_note_parser = subparsers.add_parser('new', aliases=['n'], help='create a new note')
        new_note_parser.add_argument('name', nargs='*', help='note name')

        list_parser = subparsers.add_parser('list', aliases=['l'], help='list selected note(s) content')
        list_parser.add_argument('texts', nargs='*', help='note name must contain these texts')
        list_parser.add_argument('-y', '--yesterday', dest='yesterday', action='store_true',
                                 help='show only yesterday notes')
        list_parser.add_argument('-s', '--since', dest='since', help='date (YYYY-MM-DD) since when to combine notes')
        list_parser.add_argument('-t', '--to', dest='to', help='date (YYYY-MM-DD) till when to combine notes')
        list_parser.add_argument('-o', '--output', dest='output', help='output file')

        edit_parser = subparsers.add_parser('edit', aliases=['e'], help='edit selected note')
        edit_parser.add_argument('texts', nargs='*', help='note name must contain these texts')
        edit_parser.add_argument('-y', '--yesterday', dest='yesterday', action='store_true',
                                 help='show only yesterday notes')
        edit_parser.add_argument('-s', '--since', dest='since', help='date (YYYY-MM-DD) since when to combine notes')
        edit_parser.add_argument('-t', '--to', dest='to', help='date (YYYY-MM-DD) till when to combine notes')
        edit_parser.add_argument('-o', '--output', dest='output', help='output file')

        search_parser = subparsers.add_parser('search', aliases=['s'], help='search notes with text')
        search_parser.add_argument('grep_args', nargs='*',
                                   help="args for grep; if using grep options, delimit them with '', e.g. brag s -- -i text")
        search_parser.add_argument('-v', '--invert-match', dest='invert_match', action="store_true",
                                   help='select not matching files')
        search_parser.add_argument('-s', '--since', dest='since', help='date (YYYY-MM-DD) since when to combine notes')
        search_parser.add_argument('-t', '--to', dest='to', help='date (YYYY-MM-DD) till when to combine notes')
        search_parser.add_argument('-o', '--output', dest='output', help='output file')

        subparsers.add_parser('data_dir', aliases=['dd'], help='open directory where notes are stored')

        return parser
