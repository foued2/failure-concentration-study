"""Report whether this guest can open a host-repository file.

The probe opens the path and closes it immediately. It never reads, prints or
returns the file's bytes, so a permitted access is reported as a boolean and an
error class only. The positive control is the probe's own body file, which the
host explicitly mapped read-only into the inbox.

The target path is a constant: the host does not send it, and the guest never
receives host data through this probe.
"""

import json
import os

HOST_REPO = r"C:\Users\Foued\PycharmProjects\failure-concentration-study-v9\h3-footprint-v9"
HOST_ORACLE = os.path.join(HOST_REPO, "oracle.py")

MARKER = "V9PROBE"


def _openable(path):
    """True when the process may open the path; never reads any bytes."""
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0))
    except OSError as exc:
        return False, type(exc).__name__
    else:
        os.close(fd)
        return True, None


def solve_job(payload):
    paths = dict(payload.get("paths") or {})
    oracle_allowed, oracle_error = _openable(HOST_ORACLE)
    positive_allowed, positive_error = _openable(os.path.abspath(__file__))
    report = {
        "probe": "host_file_access",
        "oracle_allowed": oracle_allowed,
        "oracle_error": oracle_error,
        "host_repo_present": os.path.isdir(HOST_REPO),
        "positive_path": os.path.abspath(__file__),
        "positive_allowed": positive_allowed,
        "positive_error": positive_error,
        "paths": paths,
    }
    print(MARKER + " " + json.dumps(report, sort_keys=True))
    return 1
