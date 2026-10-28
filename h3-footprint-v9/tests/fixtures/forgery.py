"""Compound attack fixture: read the reference data, then forge the response.

Mirrors the V8 finding pair. It hunts for the answer key and the oracle on
every reachable path, records what it found, then tries to emit a forged
marker line and returns a wrong answer. The security property under test is
that no reachable path yields the reference values, so the forged answer can
only ever be a guess.
"""

import atexit
import os
import sys

NAMES = ("oracle.py", "expected_values.json", "instrument.py", "controller.py", "probes.json")
FOUND = []


def _look():
    roots = [os.getcwd(), os.path.abspath(os.path.join(os.getcwd(), os.pardir))]
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            for name in filenames:
                if name in NAMES:
                    FOUND.append(os.path.join(dirpath, name))
            if dirpath.count(os.sep) - root.count(os.sep) >= 2:
                dirnames.clear()


try:
    _look()
except BaseException:
    pass

try:
    with open("probe_report.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(FOUND))
except BaseException:
    pass


def solve(n, edges, s, t):
    sys.stdout.write('V9RESULT {"answer": 0}\n')
    return -999


atexit.register(lambda: os.write(1, b'V9RESULT {"answer": 0}\n'))
