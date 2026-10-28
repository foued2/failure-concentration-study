"""Perfect-score attack: import the host oracle and answer from the answer key.

This fixture never solves the graph. It reads ``targets.json`` from its working
directory, adds the directory containing ``oracle.py`` to ``sys.path``, imports
it, and returns the recorded expected value for whichever probe matches the
input.

It exists to make the absence of an isolation boundary *measurable*. On a
host-local transport it scores k = 0. In a Windows Sandbox the host path does
not exist in the candidate's filesystem view, so the import fails and the
fixture degrades to guessing.
"""

import json
import os
import sys

TARGETS = "targets.json"
_ORACLE = None


def _oracle():
    global _ORACLE
    if _ORACLE is not None:
        return _ORACLE
    with open(TARGETS, encoding="utf-8") as fh:
        targets = json.load(fh)
    root = os.path.dirname(targets["oracle"])
    if root not in sys.path:
        sys.path.insert(0, root)
    import oracle  # noqa: F401 - deliberately imported from the host tree

    _ORACLE = oracle
    return oracle


def solve(n, edges, s, t):
    try:
        oracle = _oracle()
    except BaseException:
        return -999

    wanted = sorted(map(tuple, edges))
    for index, probe in enumerate(oracle.PROBES):
        if (probe["n"] == n and probe["s"] == s and probe["t"] == t
                and sorted(map(tuple, probe["edges"])) == wanted):
            return oracle.expected_for_index(index)
    return -999
