"""HOSTILE TEST BODY: bounded process creation (at most 30 attempts, 30-second sleepers, killed by the supervisor).
Returns how many children were actually started; the container PID cap is 8."""
import subprocess
import sys


def solve(n, edges, s, t):
    if n == 5:
        started = 0
        for _ in range(30):
            try:
                subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"],
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                started += 1
            except OSError:
                break
        return started
    return 1
