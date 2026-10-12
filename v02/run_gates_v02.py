"""v0.2 gates: G1 partition re-run, G2 input-level chain checks, G3 on pilot + dry seeds."""
from __future__ import annotations

import json
import math
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from models_v02 import build_pairs, loo_delta_pairs, shared_relabel_groups
from study.families import FAMILY_ORDER, PREDICATES
from study.instances import make_hidden_suite
from study.probes import make_probe_suite
from study.sssp import brute_force_min, dijkstra_ref


def g1() -> dict:
    seeds = [101, 102, 103, 301, 302, 303]
    total, exact, viol = 0, 0, []
    for seed in seeds:
        for p in make_probe_suite(seed):
            total += 1
            sat = [PREDICATES[f](p["n"], p["edges"], p["s"], p["t"]) for f in FAMILY_ORDER]
            ok = sat[FAMILY_ORDER.index(p["family"])] and sum(sat) == 1
            if ok:
                exact += 1
            else:
                viol.append(p["probe_id"])
    return {"name": "G1", "total": total, "exact_one": exact, "violations": viol, "pass": not viol}


def g2() -> dict:
    checks = []
    # Soft-label aggregation: pair with 15/20 successes, weight from 4 pairs in instance
    obs = [
        {"instance": 1, "k": 3, "C": 2 / 3, "fails": [True] * 3 + [False] * 27, "successes": 15},
        {"instance": 1, "k": 2, "C": 1 / 2, "fails": [True, True] + [False] * 28, "successes": 20},
        {"instance": 1, "k": 5, "C": 1.0, "fails": [True] * 5 + [False] * 25, "successes": 0},
        {"instance": 1, "k": 2, "C": 1 / 2, "fails": [True, True] + [False] * 28, "successes": 10},
    ]
    pairs = build_pairs(obs)
    checks.append({"case": "soft_label", "y": [p["y"] for p in pairs], "pass": [p["y"] for p in pairs] == [0.75, 1.0, 0.0, 0.5]})
    checks.append({"case": "instance_weight", "w": [p["w"] for p in pairs], "pass": all(abs(p["w"] - 0.25) < 1e-12 for p in pairs)})
    # LOIO machinery runs and returns finite deltas on a synthetic 3-instance set
    obs3 = []
    for inst in (1, 2, 3):
        for j, succ in enumerate([5, 10, 15, 20]):
            fails = [True] * (2 + j) + [False] * (28 - j)
            obs3.append({"instance": inst, "k": 2 + j, "C": 1.0 if j == 3 else 1 / (2 + j), "fails": fails, "successes": succ})
    pairs3 = build_pairs(obs3)
    deltas, mean = loo_delta_pairs(pairs3)
    checks.append({"case": "loo_runs", "deltas": deltas, "pass": len(deltas) == 3 and not math.isnan(mean)})
    # Shared relabel: same partition for a given r across calls
    g1r, g2r = shared_relabel_groups(7), shared_relabel_groups(7)
    checks.append({"case": "relabel_deterministic", "pass": g1r == g2r and sorted(x for g in g1r for x in g) == list(range(30))})
    return {"name": "G2", "checks": checks, "pass": all(c["pass"] for c in checks)}


def g3() -> dict:
    seeds = [101, 102, 103, 301, 302, 303, 304, 305]
    mism = []
    checked = 0
    for seed in seeds:
        for h in make_hidden_suite(seed):
            checked += 1
            if dijkstra_ref(h["n"], h["edges"], h["s"], h["t"]) != brute_force_min(h["n"], h["edges"], h["s"], h["t"]):
                mism.append({"seed": seed, "hid": h["hid"]})
    return {"name": "G3", "hidden_inputs_checked": checked, "mismatches": mism, "pass": not mism}


def main() -> None:
    report = {"timestamp": datetime.now(timezone.utc).isoformat(), "G1": g1(), "G2": g2(), "G3": g3()}
    report["all_pass"] = report["G1"]["pass"] and report["G2"]["pass"] and report["G3"]["pass"]
    out = ROOT / "gates"
    out.mkdir(exist_ok=True)
    (out / "gates_report_v02.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: (v["pass"] if isinstance(v, dict) and "pass" in v else v) for k, v in report.items()}, indent=2))
    sys.exit(0 if report["all_pass"] else 1)


if __name__ == "__main__":
    main()
