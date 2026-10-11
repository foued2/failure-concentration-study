"""Run gates G1 (partition), G2 (measurement chain), G3 (oracle chain). Writes gates/gates_report.json."""
from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from study.families import FAMILY_ORDER, PREDICATES
from study.features import concentration, family_counts, run_hidden, run_probes
from study.probes import make_probe_suite
from study.sssp import brute_force_min, dijkstra_ref

OUT = Path(__file__).resolve().parents[1] / "gates"


def g1_partition() -> dict:
    seeds = [101, 102, 103, 201, 202, 203, 204, 205]
    total, exact, violations = 0, 0, []
    for seed in seeds:
        for p in make_probe_suite(seed):
            total += 1
            sat = [PREDICATES[f](p["n"], p["edges"], p["s"], p["t"]) for f in FAMILY_ORDER]
            expected = FAMILY_ORDER.index(p["family"])
            ok = sat[expected] and sum(sat) == 1
            if ok:
                exact += 1
            else:
                violations.append({"seed": seed, "probe": p["probe_id"], "sat": sat})
    return {"name": "G1", "seeds": seeds, "total": total, "exact_one": exact, "violations": violations, "pass": not violations}


def g2_chain() -> dict:
    checks = []

    # Hand-computed case: 30 probes, mock fail pattern on instance 101 suite
    probes = make_probe_suite(101)
    fails = [False] * 30
    fails[0] = True   # F1_0
    fails[3] = True   # F1_3
    fails[12] = True  # F3_2
    k, c = concentration(fails)
    counts = family_counts(fails)
    checks.append({"case": "k_C_hand", "got": {"k": k, "C": c, "counts": counts}, "want": {"k": 3, "C": 2 / 3, "counts_F1": 2, "counts_F3": 1},
                   "pass": k == 3 and abs(c - 2 / 3) < 1e-12 and counts["F1"] == 2 and counts["F3"] == 1})

    # Eligibility boundary: k=1 ineligible, k=2 eligible (Y present)
    fails1 = [False] * 30
    fails1[0] = True
    k1, _ = concentration(fails1)
    checks.append({"case": "eligibility_k1", "k": k1, "pass": k1 == 1 and k1 < 2})
    fails2 = [False] * 30
    fails2[0] = fails2[5] = True
    k2, _ = concentration(fails2)
    checks.append({"case": "eligibility_k2", "k": k2, "pass": k2 == 2 and k2 >= 2})

    # Y hand case: mock solvers over hidden suite of seed 101
    from study.instances import make_hidden_suite

    hidden = make_hidden_suite(101)

    def always_right(n, edges, s, t):
        return dijkstra_ref(n, edges, s, t) if dijkstra_ref(n, edges, s, t) is not None else -1

    def wrong_on_first(n, edges, s, t):
        d = always_right(n, edges, s, t)
        return d + 1 if d != -1 else -1

    y_ok = run_hidden(always_right, hidden)
    y_bad = run_hidden(wrong_on_first, hidden)
    checks.append({"case": "Y_hand", "y_right": y_ok, "y_wrong": y_bad, "pass": y_ok == 1 and y_bad == 0})

    # Crash on probe counts as failure
    def crashy(n, edges, s, t):
        raise RuntimeError("boom")

    rk = sum(run_probes(crashy, probes))
    checks.append({"case": "crash_is_failure", "k": rk, "pass": rk == 30})

    # Output identity: C from family_counts path == naive contiguous-group path
    fails_t = [True if i % 7 == 0 else False for i in range(30)]
    _, c1 = concentration(fails_t)
    groups = [list(range(i * 5, (i + 1) * 5)) for i in range(6)]
    naive = max(sum(fails_t[i] for i in g) for g in groups) / sum(fails_t)
    checks.append({"case": "output_identity", "c1": c1, "c2": naive, "pass": abs(c1 - naive) < 1e-15})

    return {"name": "G2", "checks": checks, "pass": all(c["pass"] for c in checks)}


def g3_oracle() -> dict:
    rng = random.Random(20261011)
    mismatches = []
    for i in range(60):
        n = rng.randint(2, 7)
        m = rng.randint(0, min(10, n * (n - 1)))
        edges = []
        seen = set()
        for _ in range(m):
            u = rng.randrange(n)
            v = rng.randrange(n)
            if v == u or (u, v) in seen:
                continue
            seen.add((u, v))
            edges.append((u, v, rng.randint(0, 9)))
        s, t = rng.randrange(n), rng.randrange(n)
        d_ref = dijkstra_ref(n, edges, s, t)
        d_bf = brute_force_min(n, edges, s, t)
        if d_ref != d_bf:
            mismatches.append({"i": i, "n": n, "edges": edges, "s": s, "t": t, "ref": d_ref, "bf": d_bf})
    return {"name": "G3", "cases": 60, "mismatches": mismatches, "pass": not mismatches}


def main() -> None:
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "G1": g1_partition(),
        "G2": g2_chain(),
        "G3": g3_oracle(),
    }
    report["all_pass"] = report["G1"]["pass"] and report["G2"]["pass"] and report["G3"]["pass"]
    OUT.mkdir(exist_ok=True)
    (OUT / "gates_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: (v["pass"] if isinstance(v, dict) and "pass" in v else v) for k, v in report.items()}, indent=2))
    if not report["all_pass"]:
        print("GATES FAILED")
        sys.exit(1)
    print("ALL GATES PASS")


if __name__ == "__main__":
    main()
