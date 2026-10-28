"""Spawn a child that outlives its parent and return immediately.

The supervisor assigned this process to a Job Object and measures the job's
active-process count after the parent exits. A child that is still sleeping must
be terminated, and the response must report ``tree_empty: true``. If the job
object did not contain descendants, the child would survive the response.
"""

import json
import os
import subprocess
import sys

MARKER = "V9PROBE"


def solve_job(payload):
    child = subprocess.Popen(
        [sys.executable, "-I", "-c", "import time; time.sleep(120)"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    report = {
        "probe": "process_tree",
        "parent_pid": os.getpid(),
        "child_pid": child.pid,
        "child_spawned": True,
        "child_alive_at_return": child.poll() is None,
        "paths": dict(payload.get("paths") or {}),
    }
    print(MARKER + " " + json.dumps(report, sort_keys=True))
    return 1
