#!/usr/bin/env python

from cmdlinearguments import CmdLineArguments
from notes import Notes

if __name__ == '__main__':
    CmdLineArguments().handle(Notes())
