@echo off
pipenv sync
pipenv run python twremover.py %*
