"""dgp_outcome_tails.py - deterministic Section 6 tail-scale evaluation.

Deterministic calculation only (stdlib; no sampling, no simulation).

Outcome DGP (candidate, Section 9.1): per (body, suite) pair,
  logit(p) = theta0 + theta1*log(1+k) + u + v, u ~ N(0,1) body, v ~ N(0,1) suite,
  s ~ Binomial(20, p); soft label s/20. Gate tails: lower s <= 5 (s/20 <= 0.25),
  upper s >= 15 (s/20 >= 0.75). Evaluated at gamma = 0 (reference); the gamma*
  calibration is a Phase 1 simulation-internal procedure and is not computed here.

Method: fixed Simpson quadrature over (u, v) on [-6, 6]^2 (node counts 81 and
161; the 161/81 comparison is printed as a convergence check); exact mixing
over C given k via the conditioned Dirichlet-multinomial law (uniform over
feasible compositions); exact Binomial(20, p) tail sums per grid point.
theta0 = 0, theta1 = -1, sigma_b = sigma_s = 1 are PROPOSED values: this
calculation either supports the tail-scale claim at the documented sizes or it
does not; it does not validate the parameters. Expected support-body counts
are count-rule expectations (upper; actual Section 5 support is at most this;
see feas_prob.py e_cnt/e_ful).
"""

import math

THETA0 = 0.0
THETA1 = -1.0
GRID_PAIRS = [(81, 161)]


def simpson_weights(n, a, b):
    h = (b - a) / (n - 1)
    w = [0.0] * n
    for i in range(n):
        c = 1.0 if i == 0 or i == n - 1 else (4.0 if i % 2 == 1 else 2.0)
        x = a + i * h
        w[i] = (h / 3.0) * c * math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    return w


def grid_points(n, a, b):
    h = (b - a) / (n - 1)
    return [a + i * h for i in range(n)]


def binom_tails(p):
    q = 1.0 - p
    pmf = [0.0] * 21
    pmf[0] = q ** 20
    r = p / q if q > 0 else 0.0
    for j in range(20):
        pmf[j + 1] = pmf[j] * (20 - j) / (j + 1) * r
    lo = sum(pmf[0:6])
    hi = sum(pmf[15:21])
    xlo = sum(pmf[0:3])
    xhi = sum(pmf[18:21])
    mean = sum(j * pmf[j] for j in range(21)) / 20.0
    return lo, hi, xlo, xhi, mean


def c_dist(k):
    from collections import Counter
    counts = Counter()
    total = [0]

    def rec(idx, rem, mx):
        if idx == 6:
            if rem == 0:
                counts[mx] += 1
                total[0] += 1
            return
        hi = 5 if rem > 5 else rem
        for f in range(hi + 1):
            rec(idx + 1, rem - f, mx if mx > f else f)

    rec(0, k, 0)
    return [(c, n / total[0]) for c, n in sorted(counts.items())]


def tail_fractions(ks, kprobs, ngrid):
    xs = grid_points(ngrid, -6.0, 6.0)
    ws = simpson_weights(ngrid, -6.0, 6.0)
    wsum = sum(ws)
    acc = [0.0, 0.0, 0.0, 0.0, 0.0]
    for k, kp in zip(ks, kprobs):
        xk = math.log(1 + k)
        base = THETA0 + THETA1 * xk
        for _, cp in c_dist(k):
            for iu in range(ngrid):
                u = xs[iu]
                wu = ws[iu]
                for iv in range(ngrid):
                    eta = base + u + xs[iv]
                    if eta >= 0:
                        p = 1.0 / (1.0 + math.exp(-eta))
                    else:
                        e = math.exp(eta)
                        p = e / (1.0 + e)
                    lo, hi, xlo, xhi, mean = binom_tails(p)
                    w = kp * cp * wu * ws[iv]
                    acc[0] += w * lo
                    acc[1] += w * hi
                    acc[2] += w * xlo
                    acc[3] += w * xhi
                    acc[4] += w * mean
    return acc, wsum


def exp_count_support(n, masses, inrange):
    tot = 0.0
    for k in inrange:
        pk = masses[k]
        lpk = math.log(pk)
        l1m = math.log1p(-pk)
        for nn in range(8, n + 1):
            lg = math.lgamma(n + 1) - math.lgamma(nn + 1) - math.lgamma(n - nn + 1)
            lg += nn * lpk + (n - nn) * l1m
            if lg > -745.0:
                tot += nn * math.exp(lg)
    return tot


def main():
    print("dgp_outcome_tails.py - deterministic Section 6 tail-scale evaluation")
    print("theta0=%g theta1=%g sigma_b=sigma_s=1 (PROPOSED, gamma=0 reference)" % (THETA0, THETA1))
    print()
    n1, n2 = GRID_PAIRS[0]
    mixes = {
        "a-hist": ([5, 10], [0.10 / 0.15, 0.05 / 0.15]),
        "b-hist": ([5, 10, 20], [0.075 / 0.125, 0.025 / 0.125, 0.025 / 0.125]),
        "c-hist": ([5, 10], [0.03 / 0.05, 0.02 / 0.05]),
        "a-50:50": ([5, 10], [0.5, 0.5]),
        "b-thirds": ([5, 10, 20], [1 / 3, 1 / 3, 1 / 3]),
        "c-50:50": ([5, 10], [0.5, 0.5]),
    }
    print("Per-pair fractions: P(s<=5) P(s>=15) P(s<=2) P(s>=18) E[s/20]; grids %d/%d:" % (n1, n2))
    fr = {}
    for name, (ks, kp) in mixes.items():
        a1, w1 = tail_fractions(ks, kp, n1)
        a2, w2 = tail_fractions(ks, kp, n2)
        fr[name] = a2
        conv = max(abs(a1[i] - a2[i]) for i in range(5))
        print("  %-8s grid%d: lo=%.6f hi=%.6f xlo=%.6f xhi=%.6f mean=%.6f (wsum=%.9f)" % (
            name, n1, a1[0], a1[1], a1[2], a1[3], a1[4], w1))
        print("  %-8s grid%d: lo=%.6f hi=%.6f xlo=%.6f xhi=%.6f mean=%.6f (wsum=%.9f) maxdiff=%.2e" % (
            name, n2, a2[0], a2[1], a2[2], a2[3], a2[4], w2, conv))
    print()
    scen = {
        "a-hist": ({0: 0.80, 5: 0.10, 10: 0.05, 25: 0.05}, [5, 10]),
        "b-hist": ({0: 0.75, 5: 0.075, 10: 0.025, 20: 0.025, 25: 0.125}, [5, 10, 20]),
        "c-hist": ({0: 0.94, 5: 0.03, 10: 0.02, 25: 0.01}, [5, 10]),
    }
    print("Expected tail-pair counts = E[count-support bodies] x N_s x per-pair fraction")
    print("(count-rule support = upper; gate needs >= 30 pairs per tail):")
    for name, (masses, ir) in scen.items():
        lo, hi = fr[name][0], fr[name][1]
        for nb in (113, 150, 450, 600):
            es = exp_count_support(nb, masses, ir)
            for ns in (20, 40):
                print("  %-7s N_b=%-4d N_s=%-3d E[support]=%7.2f E[lo-pairs]=%8.2f E[hi-pairs]=%8.2f" % (
                    name, nb, ns, es, es * ns * lo, es * ns * hi))


if __name__ == "__main__":
    main()
