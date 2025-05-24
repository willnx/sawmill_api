"""
Functions to avoid "bad things" from user input.

"Bad things" includes, but is not limited to situations like:
    - Writing to any file
    - Creating files
    - Reading something outside the Sawmill root, like `/etc/passwd`

Bonus points for doing "good things" like:
    - Catching attempts to read non-existent files.
    - Having error messages that *mean something* to users.
    - Catching errors before having to run a command.
"""

import pathlib

from sawmill_api import utils


def sanitize_cat_path_args(arguments, current_working_directory, file_root_path):
    error = ""
    for argument in arguments:
        if argument.startswith("-"):
            continue
        else:
            path = utils.resolve_path(pathlib.Path(argument), current_working_directory)
            if not utils.path_is_valid(path, file_root_path):
                error = f"Invalid argument path: {argument}"
                break
            elif not path.exists():
                error = f"No such file exists: {argument}"
                break

    return error
