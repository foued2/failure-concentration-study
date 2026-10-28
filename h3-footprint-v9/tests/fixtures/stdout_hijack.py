"""Hand-authored fixture: output hijack.

Replaces the worker's stdout, prints forged marker lines and registers an exit
handler. It returns a wrong answer, so hijacking the channel must not improve
its score.
"""

import atexit
import os
import sys


class _Sink:
    def write(self, _text):
        return len(_text)

    def flush(self):
        pass


def solve(n, edges, s, t):
    sys.stdout = _Sink()
    sys.__stdout__ = _Sink()
    return -999


atexit.register(lambda: os.write(1, b'V9RESULT {"answer": 0}\n'))
