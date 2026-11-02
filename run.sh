#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ "$#" -eq 0 ]; then
    set -- --help
fi
exec python3 academia.py "$@"
