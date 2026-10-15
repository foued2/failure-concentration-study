"""outcome_tails_c.py - Revision C gate-tail expectations on bucket-local support.

Deterministic stdlib-only. Reuses verified modules (no logic duplicated):
  per-pair tail fractions from dgp_outcome_tails.tail_fractions (gamma=0
  reference, 161-node Simpson grid);
  bucket-local support expectations from feas_prob.exp_support with g_full
  (conditions 1-4 only; rank/conditioning conjunct excluded - complete-rule
  probability is 0 as-drafted, see design Section 5A).
Table: E[bucket-local support bodies] x N_s x per-pair tail fraction, with N_s
in {20, 40} labelled as SENSITIVITY cases S20/S40 (the real-study suite count
is an owner decision, not adopted). Count-rule expectations shown alongside
as the loose upper bound.
Assumptions (stated): the pair-count expectation treats pairs as exchangeable
(support bodies x suites); support expectation is bucket-local only.
"""

import feas_prob as FP
from dgp_outcome_tails import tail_fractions


def main():
    NMAX = 600
    FP.build_lc(NMAX)
    gf = {k: FP.g_full(k, NMAX) for k in (5, 10, 20)}
    gc = {k: [1.0 if i >= 8 else 0.0 for i in range(NMAX + 1)] for k in (5, 10, 20)}
    mixes = {
        "a-hist": (([5, 10], [0.10 / 0.15, 0.05 / 0.15]),
                   ({0: 0.80, 5: 0.10, 10: 0.05, 25: 0.05}, [5, 10])),
        "b-hist": (([5, 10, 20], [0.075 / 0.125, 0.025 / 0.125, 0.025 / 0.125]),
                   ({0: 0.75, 5: 0.075, 10: 0.025, 20: 0.025, 25: 0.125}, [5, 10, 20])),
        "c-hist": (([5, 10], [0.03 / 0.05, 0.02 / 0.05]),
                   ({0: 0.94, 5: 0.03, 10: 0.02, 25: 0.01}, [5, 10])),
    }
    print("outcome_tails_c.py - gate-tail expectations on bucket-local support (gamma=0)")
    print("N_s in {20, 40} are SENSITIVITY cases S20/S40 (suite count owner-open, not adopted)")
    print("gate needs >= 30 pairs per tail with >= 10 bodies and >= 6 suites per tail")
    for name, ((ks, kp), (masses, ir)) in mixes.items():
        fr, _ = tail_fractions(ks, kp, 161)
        lo, hi = fr[0], fr[1]
        print("mix %s: per-pair P(s<=5)=%.6f P(s>=15)=%.6f" % (name, lo, hi))
        for nb in (113, 150, 450, 600):
            eb = FP.exp_support(nb, masses, ir, gf)
            ec = FP.exp_support(nb, masses, ir, gc)
            for ns, tag in ((20, "S20"), (40, "S40")):
                print("  %s N_b=%-4d %s E[bl-support]=%7.2f E[lo-pairs]=%8.2f E[hi-pairs]=%8.2f (count-rule E=%7.2f)" % (
                    name, nb, tag, eb, eb * ns * lo, eb * ns * hi, ec))


if __name__ == "__main__":
    main()
