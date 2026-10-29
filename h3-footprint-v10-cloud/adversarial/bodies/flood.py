"""HOSTILE TEST BODY: bounded output floods. Every loop has a fixed upper bound (<= 8 MiB or 200 MiB of captured prints).
n=8 is a benign recovery probe."""
import os


def solve(n, edges, s, t):
    if n == 5:      # ordinary prints (captured by BoundedTextIO)
        for _ in range(200):
            print("x" * (1024 * 1024))
        return 1
    if n == 6:      # raw fd 1 flood, 8 MiB total
        chunk = b"A" * 65536
        for _ in range(128):
            os.write(1, chunk)
        return 1
    if n == 7:      # raw fd 2 flood, 8 MiB total
        chunk = b"B" * 65536
        for _ in range(128):
            os.write(2, chunk)
        return 1
    return 2
