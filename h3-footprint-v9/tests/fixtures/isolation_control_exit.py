"""Normal-exit control for the process-tree probe.

The response must be ``ok`` with ``tree_empty: true``. Without this control a
tree check that failed for an unrelated reason could be mistaken for successful
containment.
"""

import json

MARKER = "V9PROBE"


def solve_job(payload):
    report = {
        "probe": "control_exit",
        "exited_normally": True,
        "paths": dict(payload.get("paths") or {}),
    }
    print(MARKER + " " + json.dumps(report, sort_keys=True))
    return 1
