#!/usr/bin/env python

from arg_parser import create_argument_parser
from common import setup
from note import Note

COMMANDS = {
    'new': Note.create,
    'show': Note.show,
}

setup()
parser = create_argument_parser()
args = parser.parse_args()

if args.command:
    COMMANDS[args.command](args)
else:
    parser.print_help()
