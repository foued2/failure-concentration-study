"""dgp_counts_v2.py -- exact conditioned Dirichlet-multinomial family counts.

Repair basis: Revision B staging B + CLAUDE instructions (DGP family counts via
conditioned Dirichlet-multinomial P(f | k, sum f_j = k, 0 <= f_j <= 5) with
explicit normalizer Z; report within-k C spread/extreme frequencies at
k = 5, 10, 20). Stdlib only (no numpy in .venv). Deterministic: enumeration,
no randomness.

Model: alpha = (1,1,1,1,1,1); Dirichlet-multinomial
  P(f) = k! / prod(f_j!) * prod Gamma(alpha_j+f_j)/Gamma(alpha_j) * Gamma(A)/Gamma(A+k)
with A = 6.  With alpha_j = 1 this simplifies to a CONSTANT k! * 5! / (k+5)!,
so conditioned on feasibility (0 <= f_j <= 5) the law is UNIFORM over feasible
compositions.  Z(k) = number of feasible compositions; enumeration below
verifies the constant-weight claim numerically as a self-check.
"""
import math
import sys

FAMS = 6
PROBES_PER_FAM = 5  # f_j <= 5 (5 probes per family)


def compositions(k, parts, cap, prefix=()):
    """All tuples of length `parts` summing to k with each entry <= cap."""
    if parts == 1:
        if 0 <= k <= cap:
            yield prefix + (k,)
        return
    lo = max(0, k - cap * (parts - 1))
    hi = min(cap, k)
    for v in range(lo, hi + 1):
        yield from compositions(k - v, parts - 1, cap, prefix + (v,))


def dirichlet_multinomial_weight(f, alpha):
    """log unnormalized Dirichlet-multinomial weight (alpha tuple)."""
    k = sum(f)
    A = sum(alpha)
    w = math.lgamma(k + 1) - sum(math.lgamma(x + 1) for x in f)
    w += sum(math.lgamma(a + x) - math.lgamma(a) for a, x in zip(alpha, f))
    w += math.lgamma(A) - math.lgamma(A + k)
    return w


def analyze_k(k, alpha=(1,) * FAMS):
    comps = list(compositions(k, FAMS, PROBES_PER_FAM))
    if not comps:
        return None
    logs = [dirichlet_multinomial_weight(f, alpha) for f in comps]
    # self-check: with alpha = (1,)*6 all weights must be equal
    spread = max(logs) - min(logs)
    weights = [math.exp(x - max(logs)) for x in logs]
    Z = sum(weights)  # normalizer (enumerated)
    Cs = [max(f) / k if k > 0 else 0.0 for f in comps]
    p = [w / Z for w in weights]
    c_freq = {}
    for c, pi in zip(Cs, p):
        c_freq[c] = c_freq.get(c, 0.0) + pi
    return {
        "k": k,
        "Z": Z,
        "n_comps": len(comps),
        "weight_spread_log": spread,
        "C_min": min(c_freq),
        "C_max": max(c_freq),
        "P_Cmin": c_freq[min(c_freq)],
        "P_Cmax": c_freq[max(c_freq)],
        "E_C": sum(c * pi for c, pi in c_freq.items()),
        "Var_C": sum((c - sum(x * y for x, y in c_freq.items())) ** 2 * pi
                     for c, pi in c_freq.items()),
        "n_C_values": len(c_freq),
        "c_freq": c_freq,
    }


def main():
    print("Conditioned Dirichlet-multinomial, alpha=(1,)*6, f_j<=5, exact enumeration")
    print("Self-check (weight spread over compositions, log scale; must be ~0):")
    for k in [5, 10, 20, 24]:
        r = analyze_k(k)
        print("  k=%2d  spread=%.3e  Z=%d" % (k, r["weight_spread_log"], r["Z"]))
    print()
    print("Normalizer Z(k) = #feasible compositions (k=0..24):")
    Zs = [analyze_k(k)["Z"] if k > 0 else 1 for k in range(0, 25)]
    for i in range(0, 25, 6):
        print("  " + "  ".join("k=%d:Z=%d" % (j, Zs[j])
                               for j in range(i, min(i + 6, 25))))
    print()
    for k in (5, 10, 20, 24):
        r = analyze_k(k)
        print("k=%d: C support size=%d, C in [%.6f, %.6f] "
              "(=%.4f..%.4f), floor ceil(k/6)/k=%.6f"
              % (k, r["n_C_values"], r["C_min"], r["C_max"],
                 r["C_min"], r["C_max"], math.ceil(k / 6) / k))
        print("     P(C=C_min)=%.6f  P(C=C_max)=%.6f  E[C]=%.6f  Var(C)=%.6f"
              % (r["P_Cmin"], r["P_Cmax"], r["E_C"], r["Var_C"]))
        # top frequencies for transparency
        top = sorted(r["c_freq"].items(), key=lambda kv: -kv[1])[:6]
        print("     top C values: " + "  ".join(
            "C=%.4f:p=%.4f" % (c, p) for c, p in top))
    print()
    # pigeonhole floor check vs design §1: at k=24 min C = 4/24
    r24 = analyze_k(24)
    ok = abs(r24["C_min"] - 4 / 24) < 1e-12 and abs(r24["C_max"] - 5 / 24) < 1e-12
    print("Design §1 cross-check at k=24 (min 4/24, max 5/24): %s"
          % ("PASS" if ok else "FAIL"))
    # k=5 special: C in [1/5, 1]
    r5 = analyze_k(5)
    ok5 = abs(r5["C_min"] - 1 / 5) < 1e-12 and abs(r5["C_max"] - 1.0) < 1e-12
    print("Design §9.1 cross-check at k=5 (C in [1/5, 1]): %s"
          % ("PASS" if ok5 else "FAIL"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
