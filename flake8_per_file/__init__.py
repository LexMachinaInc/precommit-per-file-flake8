"""Precommit hook that runs flake8 on one file at a time.

This allows flake8 to properly find the setup.cfg for each subpackage.

Extremely badly written; does not expect any arguments other than files
to run flake8 on. Could likely run on all files from a given subpackage
 but this is simpler.
"""

import os.path
import subprocess
import sys


def main():
    my_flake8 = os.path.join(os.path.dirname(sys.argv[0]), 'flake8')

    all_output = ''
    returncode = 0
    for arg in sys.argv[1:]:
        sp_result = subprocess.run(
            [my_flake8, arg],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf8',
        )
        returncode = sp_result.returncode
        all_output += sp_result.stdout

    sys.stderr.write(all_output)
    sys.exit(returncode)
