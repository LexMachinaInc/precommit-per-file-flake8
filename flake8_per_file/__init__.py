"""Precommit hook that runs flake8 on one file at a time.

This allows flake8 to properly find the setup.cfg for each subpackage.

Extremely badly written; does not expect any arguments other than files
to run flake8 on. Could likely run on all files from a given subpackage
 but this is simpler.
"""

import os.path
import pathlib
import subprocess
import sys


def find_cfg(arg):
    arg_path = pathlib.Path(arg).expanduser().resolve()
    for i in range(len(arg_path.parts)):
        possible_cfg_path = pathlib.Path(*arg_path.parts[:i]) / 'setup.cfg'
        if possible_cfg_path.is_file():
            return ('--config', possible_cfg_path)

    return ()


def main():
    my_flake8 = os.path.join(os.path.dirname(sys.argv[0]), 'flake8')

    all_output = ''
    returncode = 0
    flake_args = []
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            flake_args.append(arg)
            continue

        sp_result = subprocess.run(
            [my_flake8, *flake_args, *find_cfg(arg), arg],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf8',
        )
        returncode = sp_result.returncode
        all_output += sp_result.stdout

    sys.stdout.write(all_output)
    sys.exit(returncode)
