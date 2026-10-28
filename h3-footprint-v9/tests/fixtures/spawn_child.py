"""Hand-authored fixture: process-tree escape attempt.

Spawns a grandchild that outlives a sleep, records its pid, then blocks.
Used to prove the Job Object kills descendants and that termination is
verified before any further job is published.
"""

import os
import subprocess
import sys
import time

GRANDCHILD = (
    "import os,time;"
    "open('grandchild.pid','w').write(str(os.getpid()));"
    "time.sleep(120)"
)


def solve(n, edges, s, t):
    child = subprocess.Popen([sys.executable, "-c", GRANDCHILD])
    with open("grandchild.pid", "w", encoding="utf-8") as fh:
        fh.write(str(child.pid))
    time.sleep(120)
    return -1
