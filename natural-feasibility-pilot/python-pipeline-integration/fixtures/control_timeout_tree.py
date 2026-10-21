import os, subprocess, sys, time
def solve(n, edges, s, t):
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
    with open(os.environ["FC_CHILD_PID_FILE"], "w", encoding="ascii") as f: f.write(str(child.pid))
    time.sleep(120)
    return 0
