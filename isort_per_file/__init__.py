"""Precommit hook that runs flake8 on one file at a time.

This allows isort to properly find the .isort.cfg for each subpackage.

Clone of the flake8 handling system, but without the manual .cfg detection

Extremely badly written; does not expect any arguments other than files
to run isort on. Could likely run on all files from a given subpackage
 but this is simpler.
"""

import os.path
import pathlib
import subprocess
import sys



def main():
    my_isort = os.path.join(os.path.dirname(sys.argv[0]), 'isort')

    all_output = ''
    returncode = 0
    isort_args = [arg for arg in sys.argv[1:] if not pathlib.Path(arg).exists() and arg not in ('-', '--filename')]
    filenames = [arg for arg in sys.argv[1:] if pathlib.Path(arg).exists()]
    for filename in filenames:
        sp_result = subprocess.run(
            [my_isort, *isort_args, filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf8',
        )
        returncode = max(sp_result.returncode, returncode)
        all_output += sp_result.stdout

    sys.stdout.write(all_output)
    sys.exit(returncode)
