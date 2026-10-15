"""Independent check of g_full: brute-force enumeration vs pair-sum formula (small n),
plus g_k(n) curves to inspect monotonicity."""
import math

import feas_prob as F

F.build_lc(700)


def g_bruteforce(k, n):
    dist, _ = F.c_dist(k)
    probs = [p for _, p in dist]
    s = len(probs)
    tot = 0.0
    logp = [math.log(p) for p in probs]

    def rec(idx, rem, xs):
        nonlocal tot
        if idx == s - 1:
            xs.append(rem)
            lp = math.lgamma(n + 1)
            for i, x in enumerate(xs):
                lp -= math.lgamma(x + 1)
                if x:
                    lp += x * logp[i]
            present = [i for i, x in enumerate(xs) if x > 0]
            if len(present) >= 2:
                lo = min(present)
                hi = max(present)
                if xs[lo] >= 4 and xs[hi] >= 4:
                    tot += math.exp(lp)
            xs.pop()
            return
        for x in range(rem + 1):
            xs.append(x)
            rec(idx + 1, rem - x, xs)
            xs.pop()

    rec(0, n, [])
    return tot


print("brute-force vs pair-sum g_k(n):")
for k in (5, 10, 20):
    for n in (8, 9, 10, 12):
        gb = g_bruteforce(k, n)
        gp = F.g_full(k, 700)[n]
        print("  k=%d n=%d brute=%.10f pairs=%.10f %s" % (k, n, gb, gp, "OK" if abs(gb - gp) < 1e-9 else "MISMATCH"))

print()
print("g_k(n) curves:")
ns = list(range(8, 41, 2)) + list(range(40, 201, 10)) + list(range(200, 601, 50))
print("n " + " ".join("%8d" % x for x in ns))
for k in (5, 10, 20):
    g = F.g_full(k, 700)
    print("k=%d %s" % (k, " ".join("%8.5f" % g[x] for x in ns)))
