"""Run the pilot: 3 instances (seeds 101-103), 20-solver pack, yield gate, variance, N_c."""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from study.features import evaluate_pair, load_solver
from study.instances import make_hidden_suite, make_instance
from study.models import bootstrap_ci, loo_delta, relabel_control_deltas
from study.probes import make_probe_suite

ROOT = Path(__file__).resolve().parents[1]
PILOT_SEEDS = [101, 102, 103]
MIN_ELIGIBLE = 15
DELTA = 0.01
CHI2_UB80_DF2 = 0.44628710813971216


def main() -> None:
    pack_dir = ROOT / "generation" / "pilot_pack"
    solver_paths = sorted(pack_dir.glob("solver_*.py"))
    print(f"pack: {len(solver_paths)} submissions")

    solvers, format_failures = [], []
    for p in solver_paths:
        try:
            solvers.append((p.stem, load_solver(p)))
        except Exception as e:
            format_failures.append({"file": p.name, "error": str(e)})

    format_rate = len(format_failures) / max(len(solver_paths), 1)
    results = {"instances": {}, "format_failures": format_failures, "format_rate": format_rate}

    all_pairs = []
    for seed in PILOT_SEEDS:
        probes = make_probe_suite(seed)
        hidden = make_hidden_suite(seed)
        inst = make_instance(seed)
        rows = []
        for name, fn in solvers:
            r = evaluate_pair(fn, probes, hidden)
            rows.append({"solver": name, "k": r["k"], "C": r["C"], "Y": r["Y"], "eligible": r["eligible"]})
            if r["eligible"]:
                all_pairs.append(
                    {"instance": seed, "solver": name, "k": r["k"], "C": r["C"], "Y": r["Y"], "fails": r["fails"]}
                )
        results["instances"][str(seed)] = {
            "anchor": {"n": inst["n"], "m": len(inst["edges"])},
            "eligible": sum(r["eligible"] for r in rows),
            "total": len(rows),
            "rows": rows,
        }
        print(f"seed {seed}: eligible {results['instances'][str(seed)]['eligible']}/{len(rows)}")

    gate_pass = all(results["instances"][str(s)]["eligible"] >= MIN_ELIGIBLE for s in PILOT_SEEDS)
    format_ok = format_rate <= 0.20

    # LOIO Δ on pilot instances (variance input only)
    obs = [{"instance": p["instance"], "k": p["k"], "C": p["C"], "Y": p["Y"]} for p in all_pairs]
    delta_i, delta_mean = loo_delta(obs) if obs else ([], float("nan"))
    ci_lo, ci_hi = bootstrap_ci(delta_i) if delta_i else (float("nan"), float("nan"))

    finite = [d for d in delta_i if not math.isnan(d)]
    if len(finite) >= 2:
        mean = sum(finite) / len(finite)
        s2 = sum((d - mean) ** 2 for d in finite) / (len(finite) - 1)
        s2_ub = (len(finite) - 1) * s2 / CHI2_UB80_DF2
        n_c = math.ceil((1.96 * math.sqrt(s2_ub) / DELTA) ** 2) if s2_ub > 0 else 1
    else:
        s2 = s2_ub = float("nan")
        n_c = None

    # Relabel control on pilot (descriptive)
    inst_seeds = {p["instance"]: p["instance"] for p in all_pairs}
    relabel_deltas = relabel_control_deltas(all_pairs, inst_seeds, r_max=100) if all_pairs else []
    relabel_sorted = sorted(d for d in relabel_deltas if not math.isnan(d))
    p95 = relabel_sorted[int(0.95 * len(relabel_sorted))] if relabel_sorted else float("nan")

    feasible = gate_pass and format_ok and n_c is not None and n_c <= 20

    results.update(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gate_pass": gate_pass,
            "format_ok": format_ok,
            "delta_i_pilot": delta_i,
            "delta_mean_pilot": delta_mean,
            "bootstrap_ci_pilot": [ci_lo, ci_hi],
            "between_instance_var": s2,
            "var_upper80": s2_ub,
            "N_c_required": n_c,
            "resource_ceiling": 20,
            "relabel_delta_mean": sum(relabel_deltas) / len(relabel_deltas) if relabel_deltas else float("nan"),
            "relabel_p95": p95,
            "decision": "FEASIBLE — proceed to confirmatory generation" if feasible else "INFEASIBLE — stop",
        }
    )
    out = ROOT / "pilot"
    out.mkdir(exist_ok=True)
    (out / "pilot_report.json").write_text(json.dumps(results, indent=2))
    print(json.dumps({k: results[k] for k in ["gate_pass", "format_ok", "N_c_required", "decision", "delta_i_pilot", "relabel_p95"]}, indent=2))


if __name__ == "__main__":
    main()
