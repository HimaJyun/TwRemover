#!/bin/bash -eu
pipenv sync
exec pipenv run python twremover.py "$@"
