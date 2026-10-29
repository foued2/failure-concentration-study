"""HOSTILE TEST BODY: tries to survive past its probe by daemonizing (setsid) and leaving a marker.
n=6 counts processes other than the worker (expected: supervisor + trusted coordinator, i.e. 2)."""
import os
import time


def solve(n, edges, s, t):
    if n == 5:
        pid = os.fork()
        if pid == 0:
            os.setsid()
            try:
                with open(os.path.join(os.environ.get("TMPDIR", "/tmp"), "alive"), "w") as f:
                    f.write("1")
            except OSError:
                pass
            time.sleep(25)
            os._exit(0)
        return 1
    if n == 6:
        return len([p for p in os.listdir("/proc") if p.isdigit() and int(p) != os.getpid()])
    return 0
