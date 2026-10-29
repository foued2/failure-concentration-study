"""HOSTILE TEST BODY: bounded process creation (at most 30 attempts, 30-second sleepers).
Children are killed and reaped before returning so the started-count survives the supervisor's leak check.
Returns how many children were actually started; the container PID cap is 8."""
import subprocess
import sys


def solve(n, edges, s, t):
    if n == 5:
        kids = []
        for _ in range(30):
            try:
                kids.append(subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"],
                                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
            except OSError:
                break
        started = len(kids)
        for k in kids:
            k.kill()
            k.wait()
        return started
    return 1
