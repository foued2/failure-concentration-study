"""tail_support_d.py - Revision D per-bucket gate-tail expectations (gamma=0 reference).

Deterministic stdlib-only. Same-directory imports only (run from v03p/scripts/).
Reuses verified modules without duplicating logic:
  per-k tail fractions from dgp_outcome_tails.tail_fractions;
  bucket-local pass tables from feas_prob.g_full;
  Simpson/binomial helpers from dgp_outcome_tails.

For each scenario mix, body count N and tail (lower s<=5, upper s>=15):
  E[B_{k,support}] per in-range bucket k (exact: E[n_k * g_k(n_k)]);
  q_{tail,k} per-pair tail probability at fixed k (exact Simpson quadrature;
    C plays no role at gamma=0);
  expected tail pairs = N_s * sum_k E[B_{k,support}] * q_{tail,k} (exact);
  expected distinct bodies = sum_k E[B_{k,support}] * h_k (exact at gamma=0;
    h_k = P(one k-body has >=1 tail pair) by 1-D quadrature);
  expected distinct suites = N_s * (1 - P(no tail pair in one suite)) (exact:
    latent quadrature over v times multinomial count sums).
N_s in {20, 40} are SENSITIVITY cases S20/S40 (suite count owner-open).
Omissions (stated): joint gate-pass probability P(>=M pairs AND >=D bodies
  AND >=S suites) needs latent-scale joint integration = Phase-1 simulation
  scope, not pre-freeze arithmetic. At gamma != 0 the tail rate depends on
  (k, C), so the formula additionally needs the supported C-distribution
  (requirement stated, not computed here).
"""

import math

import feas_prob as FP
from dgp_outcome_tails import tail_fractions, simpson_weights, grid_points, binom_tails

CUT = -46.0
SCEN = {
    "a-hist": ({0: 0.80, 5: 0.10, 10: 0.05, 25: 0.05}, [5, 10], [113, 150, 450, 600]),
    "b-hist": ({0: 0.75, 5: 0.075, 10: 0.025, 20: 0.025, 25: 0.125}, [5, 10, 20], [113, 150, 450, 600]),
    "c-hist": ({0: 0.94, 5: 0.03, 10: 0.02, 25: 0.01}, [5, 10], [113, 150, 450, 600]),
    "a50": ({0: 0.80, 5: 0.075, 10: 0.075, 25: 0.05}, [5, 10], [150, 600]),
    "b3": ({0: 0.75, 5: 0.125 / 3, 10: 0.125 / 3, 20: 0.125 / 3, 25: 0.125}, [5, 10, 20], [150, 600]),
    "c50": ({0: 0.94, 5: 0.025, 10: 0.025, 25: 0.01}, [5, 10], [150, 600]),
}
NU = 161


def sigmoid(eta):
    if eta >= 0:
        return 1.0 / (1.0 + math.exp(-eta))
    e = math.exp(eta)
    return e / (1.0 + e)


def per_k_support(N, masses, inrange, gf):
    out = {}
    for k in inrange:
        pk = masses[k]
        lpk = math.log(pk)
        l1m = math.log1p(-pk)
        tot = 0.0
        for n in range(N + 1):
            lg = FP.LC[N + 1] - FP.LC[n + 1] - FP.LC[N - n + 1] + n * lpk + (N - n) * l1m
            g = gf[k][n]
            if g and lg > -745.0:
                tot += n * g * math.exp(lg)
        out[k] = tot
    return out


def qbar_u(k, nU=NU, nV=NU):
    xs_v = grid_points(nV, -6.0, 6.0)
    ws_v = simpson_weights(nV, -6.0, 6.0)
    xs_u = grid_points(nU, -6.0, 6.0)
    ws_u = simpson_weights(nU, -6.0, 6.0)
    base = -math.log(1 + k)
    qlo = []
    qhi = []
    for u in xs_u:
        slo = 0.0
        shi = 0.0
        for v, wv in zip(xs_v, ws_v):
            lo, hi, _, _, _ = binom_tails(sigmoid(base + u + v))
            slo += wv * lo
            shi += wv * hi
        qlo.append(slo)
        qhi.append(shi)
    return xs_u, ws_u, qlo, qhi


def h_hit(ws_u, qbar, Ns):
    tot = 0.0
    for wu, q in zip(ws_u, qbar):
        c = 1.0 - q
        if c < 0.0:
            c = 0.0
        tot += wu * (1.0 - c ** Ns)
    return tot


def abar_v(k, nV, nU=NU):
    xs_v = grid_points(nV, -6.0, 6.0)
    xs_u = grid_points(nU, -6.0, 6.0)
    ws_u = simpson_weights(nU, -6.0, 6.0)
    base = -math.log(1 + k)
    alo = []
    ahi = []
    for v in xs_v:
        slo = 0.0
        shi = 0.0
        for u, wu in zip(xs_u, ws_u):
            lo, hi, _, _, _ = binom_tails(sigmoid(base + u + v))
            slo += wu * (1.0 - lo)
            shi += wu * (1.0 - hi)
        alo.append(min(max(slo, 0.0), 1.0))
        ahi.append(min(max(shi, 0.0), 1.0))
    return alo, ahi


def suite_no_tail(N, masses, inrange, gf, abar_lo, abar_hi):
    M = sum(masses[k] for k in inrange)
    lcond = {k: math.log(masses[k] / M) for k in inrange}
    logM = math.log(M)
    log1m = math.log1p(-M)
    use3 = len(inrange) == 3
    LC = FP.LC
    G = len(abar_lo[inrange[0]])
    sno_lo = [0.0] * G
    sno_hi = [0.0] * G

    def iter_vecs(m):
        if use3:
            for t in range(m + 1):
                r = m - t
                for u in range(r + 1):
                    yield (t, u, r - u)
        else:
            for t in range(m + 1):
                yield (t, m - t)

    for m in range(N + 1):
        logpm = LC[N + 1] - LC[m + 1] - LC[N - m + 1] + m * logM + (N - m) * log1m
        if logpm < CUT:
            continue
        for vec in iter_vecs(m):
            logmult = LC[m + 1]
            for v in vec:
                logmult -= LC[v + 1]
            for i, k in enumerate(inrange):
                if vec[i]:
                    logmult += vec[i] * lcond[k]
            lt = logpm + logmult
            if lt < CUT:
                continue
            w = math.exp(lt)
            gs = [gf[k][vec[i]] for i, k in enumerate(inrange)]
            for iv in range(G):
                plo = 1.0
                phi = 1.0
                for i, k in enumerate(inrange):
                    g = gs[i]
                    if g:
                        plo *= (1.0 - g) + g * abar_lo[k][iv] ** vec[i]
                        phi *= (1.0 - g) + g * abar_hi[k][iv] ** vec[i]
                sno_lo[iv] += w * plo
                sno_hi[iv] += w * phi
    return sno_lo, sno_hi


def main():
    NMAX = 600
    FP.build_lc(NMAX)
    gf = {k: FP.g_full(k, NMAX) for k in (5, 10, 20)}
    print("tail_support_d.py - per-bucket gate-tail expectations, bucket-local support, gamma=0")
    print("N_s in {20, 40} are SENSITIVITY cases S20/S40 (suite count owner-open, not adopted)")
    print("gate needs >= 30 pairs, >= 10 distinct bodies, >= 6 distinct suites per tail")
    qk = {}
    for k in (5, 10, 20):
        fr, _ = tail_fractions([k], [1.0], 161)
        qk[k] = (fr[0], fr[1])
    print("per-k tail fractions: " + "; ".join("k=%d lo=%.6f hi=%.6f" % (k, qk[k][0], qk[k][1]) for k in (5, 10, 20)))
    _, wsU, _, _ = qbar_u(5)
    qbu = {}
    for k in (5, 10, 20):
        _, _, qlo, qhi = qbar_u(k)
        qbu[k] = (qlo, qhi)
    for name, (masses, inrange, Ns) in SCEN.items():
        for N in Ns:
            eb = per_k_support(N, masses, inrange, gf)
            tot = FP.exp_support(N, masses, inrange, gf)
            diff = abs(sum(eb.values()) - tot)
            print("mix %s N_b=%d E[Bk]=%s sum=%.4f crosscheck-diff=%.2e %s" % (
                name, N, ", ".join("k=%d:%.2f" % (k, eb[k]) for k in inrange),
                sum(eb.values()), diff, "OK" if diff < 1e-9 else "MISMATCH"))
            for Ns_, tag in ((20, "S20"), (40, "S40")):
                plo = sum(eb[k] * qk[k][0] for k in inrange) * Ns_
                phi = sum(eb[k] * qk[k][1] for k in inrange) * Ns_
                blo = sum(eb[k] * h_hit(wsU, qbu[k][0], Ns_) for k in inrange)
                bhi = sum(eb[k] * h_hit(wsU, qbu[k][1], Ns_) for k in inrange)
                print("  %s N_b=%d %s E[pairs] lo=%.2f hi=%.2f | E[bodies] lo=%.2f hi=%.2f" % (
                    name, N, tag, plo, phi, blo, bhi))
    print("suite-quadrature convergence check on (a-hist)@150:")
    masses, inrange, _ = SCEN["a-hist"]
    pnos = []
    for G in (31, 61):
        alo = {}
        ahi = {}
        for k in inrange:
            a, b = abar_v(k, G)
            alo[k] = a
            ahi[k] = b
        sno_lo, sno_hi = suite_no_tail(150, masses, inrange, gf, alo, ahi)
        ws_v = simpson_weights(G, -6.0, 6.0)
        pnos.append((sum(w * s for w, s in zip(ws_v, sno_lo)),
                     sum(w * s for w, s in zip(ws_v, sno_hi))))
    print("  P(no-tail-suite) lo: G31=%.9f G61=%.9f | hi: G31=%.9f G61=%.9f maxdiff=%.2e" % (
        pnos[0][0], pnos[1][0], pnos[0][1], pnos[1][1],
        max(abs(pnos[0][0] - pnos[1][0]), abs(pnos[0][1] - pnos[1][1]))))
    print("exact distinct suites (bucket-local support, gamma=0):")
    for name, (masses, inrange, Ns) in SCEN.items():
        for N in Ns:
            alo = {}
            ahi = {}
            for k in inrange:
                a, b = abar_v(k, 41)
                alo[k] = a
                ahi[k] = b
            xs_v = grid_points(41, -6.0, 6.0)
            ws_v = simpson_weights(41, -6.0, 6.0)
            sno_lo, sno_hi = suite_no_tail(N, masses, inrange, gf, alo, ahi)
            pno_lo = sum(w * s for w, s in zip(ws_v, sno_lo))
            pno_hi = sum(w * s for w, s in zip(ws_v, sno_hi))
            for Ns_, tag in ((20, "S20"), (40, "S40")):
                print("  %s N_b=%d %s E[suites] lo=%.2f hi=%.2f" % (
                    name, N, tag, Ns_ * (1.0 - pno_lo), Ns_ * (1.0 - pno_hi)))


if __name__ == "__main__":
    main()
