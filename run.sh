#!/bin/bash

readonly SCRIPT_LOCATION="$(dirname "$(readlink -f "$(which brag)")")"

source "$SCRIPT_LOCATION/venv/bin/activate"

python -m brag.brag $*