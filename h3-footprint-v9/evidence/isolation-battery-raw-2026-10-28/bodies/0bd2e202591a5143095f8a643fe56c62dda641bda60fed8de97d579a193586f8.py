"""Attempt to write into the mapped inbox and outbox; control with scratch.

The child runs at low integrity. The inbox is a read-only mapping and the outbox
is a medium-integrity writable mapping, so both writes should be denied. The
scratch directory is on the guest's local disk and was labelled low integrity by
the supervisor, so the same write there must succeed -- otherwise a denial would
prove nothing about the boundary.
"""

import json
import os

MARKER = "V9PROBE"


def _write(path):
    try:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("probe\n")
        return True, None
    except OSError as exc:
        return False, type(exc).__name__


def _valid(paths):
    """Three distinct absolute guest paths are required. No relative fallback.

    The previous fixture derived ``../staging`` and ``../response`` from its
    working directory, which is the guest-local scratch folder; that tested
    look-alike siblings instead of the mapped directories. A probe that cannot
    state the real paths must not write anywhere.
    """
    keys = ("inbox", "outbox", "scratch")
    values = [paths.get(key) for key in keys]
    if not all(isinstance(value, str) and os.path.isabs(value) for value in values):
        return False
    return len({os.path.normcase(os.path.normpath(value)) for value in values}) == 3


def solve_job(payload):
    paths = dict(payload.get("paths") or {})
    if not _valid(paths):
        print(MARKER + " " + json.dumps({
            "probe": "inbox_write",
            "paths_error": "missing_or_relative_paths",
            "paths": paths,
        }, sort_keys=True))
        return 1

    inbox = paths["inbox"]
    outbox = paths["outbox"]
    scratch = paths["scratch"]

    inbox_allowed, inbox_error = _write(os.path.join(inbox, "probe-write.txt"))
    outbox_allowed, outbox_error = _write(os.path.join(outbox, "probe-write.txt"))
    scratch_allowed, scratch_error = _write(os.path.join(scratch, "probe-write.txt"))

    report = {
        "probe": "inbox_write",
        "inbox_write_allowed": inbox_allowed,
        "inbox_write_error": inbox_error,
        "outbox_write_allowed": outbox_allowed,
        "outbox_write_error": outbox_error,
        "scratch_write_allowed": scratch_allowed,
        "scratch_write_error": scratch_error,
        "paths": paths,
    }
    print(MARKER + " " + json.dumps(report, sort_keys=True))
    return 1
