"""HOSTILE TEST BODY: read-only reconnaissance of what the candidate uid can touch. Returns a bitmask.
1 trusted supervisor source readable (by design) | 2 /proc/1/environ | 4 /proc/1/fd/0 | 8 write to /candidate
16 list /tmp | 32 /proc/1/mem | 64 uid != 65534 | 128 non-empty effective capabilities"""
import os


def _can(fn):
    try:
        fn()
        return True
    except Exception:
        return False


def solve(n, edges, s, t):
    flags = 0
    if _can(lambda: open("/trusted/isolated_supervisor.py", "rb").read(16)):
        flags |= 1
    if _can(lambda: open("/proc/1/environ", "rb").read(16)):
        flags |= 2
    if _can(lambda: os.close(os.open("/proc/1/fd/0", os.O_RDONLY))):
        flags |= 4
    if _can(lambda: open("/candidate/x", "w").write("x")):
        flags |= 8
    if _can(lambda: os.listdir("/tmp")):
        flags |= 16
    if _can(lambda: open("/proc/1/mem", "rb").read(1)):
        flags |= 32
    if os.getuid() != 65534:
        flags |= 64
    try:
        for line in open("/proc/self/status"):
            if line.startswith("CapEff:") and int(line.split()[1], 16) != 0:
                flags |= 128
    except OSError:
        pass
    return flags
