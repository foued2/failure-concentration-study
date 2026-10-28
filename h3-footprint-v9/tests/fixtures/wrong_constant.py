"""Hand-authored fixture: constant-wrong solver.

Used to prove the oracle controls: a solver that never solves must produce
exactly 30 failures, never an eligible row.
"""


def solve(n, edges, s, t):
    return -999
