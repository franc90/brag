#!/bin/bash

readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

[ ! -d "$SCRIPT_DIR/venv" ] && python3 -m venv "$SCRIPT_DIR/venv"
source "$SCRIPT_DIR/venv/bin/activate"
pip3 install "$SCRIPT_DIR"
[ ! -L ~/.local/bin/brag ] && ln -s "$SCRIPT_DIR/bin/brag" ~/.local/bin/brag
