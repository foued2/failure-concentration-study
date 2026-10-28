"""Harmless system fixture: return the number the job gave it.

Used by the two-token rendezvous test. The token is carried in ``n``, so the
answer the host receives proves which job the candidate actually saw. It never
touches the reference data and it is not a solver candidate.
"""


def solve(n, edges, s, t):
    return n
