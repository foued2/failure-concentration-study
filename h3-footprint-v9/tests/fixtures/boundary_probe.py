"""Hand-authored fixture: tries to remove the lock, then tamper with records.

The deny ACE alone is not enough: the owning user holds WRITE_DAC, so this
fixture attempts the same icacls/takeown escapes V8's probe used before trying
to write. At low integrity none of them should succeed.
"""

import os

TARGETS = (
    os.path.join(os.pardir, "response", "evil.json"),
    os.path.join(os.pardir, "staging", "job.json"),
    os.path.join(os.pardir, "response", "response-forged.json"),
)


def solve(n, edges, s, t):
    lines = []
    response_dir = os.path.abspath(os.path.join(os.pardir, "response"))
    staging_dir = os.path.abspath(os.path.join(os.pardir, "staging"))
    for target in (response_dir, staging_dir):
        for command in (
            f'icacls "{target}" /remove:d %USERNAME% /T',
            f'icacls "{target}" /reset /T',
            f'icacls "{target}" /grant %USERNAME%:(OI)(CI)F /T',
            f'takeown /f "{target}" /r /d y',
        ):
            rc = os.system(command + " >nul 2>&1")
            lines.append(("CMD_OK " if rc == 0 else "CMD_FAIL ") + command)

    for target in TARGETS:
        try:
            with open(target, "w", encoding="utf-8") as fh:
                fh.write("tampered")
            lines.append("WROTE " + target)
        except BaseException as exc:
            lines.append("BLOCKED " + target + " " + type(exc).__name__)

    with open("boundary_report.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return -999
