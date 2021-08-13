#!/bin/bash

[ ! -d venv ] && python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
ln -s $PWD/brag ~/.local/bin/brag
