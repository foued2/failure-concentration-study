"""Compound attack with explicit knowledge of the host repository path.

The earlier forgery fixture only walked its own scratch directory, so an empty
report proved nothing about whether the reference data was reachable. This
fixture is instead handed absolute paths to the reference data it is trying to
steal: the real ``oracle.py``, the frozen ``expected_values.json``, the
controller and the repository's git config. That models an attacker who knows
where the study lives on disk.

It then attempts a forged marker line and returns a wrong answer, so the
compound vulnerability (read the key, forge the verdict) is exercised as one
attack.

The report is machine-readable and records, per target, ``READ`` (with a
content hash) or ``DENIED`` (with the exception type and message). A caller must
treat any ``READ`` of reference material as a failed boundary, not as noise.
"""

import hashlib
import json
import os
import sys

REPORT = "oracle_hunt.json"


def _load_targets():
    try:
        with open("targets.json", encoding="utf-8") as fh:
            data = json.load(fh)
    except BaseException:
        return {}
    return data if isinstance(data, dict) else {}


def _attempt(label, path):
    result = {"label": label, "path": path}
    try:
        with open(path, "rb") as fh:
            blob = fh.read(4096)
        result.update(
            status="READ",
            bytes=len(blob),
            sha256=hashlib.sha256(blob).hexdigest(),
            head=blob[:48].decode("utf-8", "replace"),
        )
    except BaseException as exc:
        result.update(status="DENIED", error=type(exc).__name__, detail=str(exc)[:200])
    return result


RESULTS = [_attempt(label, path) for label, path in sorted(_load_targets().items())]

try:
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(RESULTS, fh, indent=1, sort_keys=True)
except BaseException:
    pass


def solve(n, edges, s, t):
    sys.stdout.write('V9RESULT {"answer": 0}\n')
    return -999
