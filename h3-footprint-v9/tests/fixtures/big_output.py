"""Hand-authored fixture: floods stdout to test the capture cap."""


def solve(n, edges, s, t):
    chunk = "x" * 65536
    for _ in range(64):
        print(chunk)
    return -999
