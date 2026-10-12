"""v0.2 pilot: 3 instances, apply frozen gate (yield + outcome variation)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from study.features import evaluate_pair, load_solver
from study.instances import make_hidden_suite, make_instance
from study.probes import make_probe_suite

PILOT_SEEDS = [101, 102, 103]
MIN_ELIGIBLE = 15
MIN_CORR = 0.10
MIN_INCORR = 0.10
HIDDEN_M = 20


def main() -> None:
    pack = sorted((ROOT / "generation_v02" / "pack").glob("solver_*.py"))
    print(f"pack: {len(pack)} submissions")
    solvers, fmt = [], []
    for p in pack:
        try:
            solvers.append((p.stem, load_solver(p)))
        except Exception as e:
            fmt.append({"file": p.name, "error": str(e)})
    fmt_rate = len(fmt) / max(len(pack), 1)

    results = {"instances": {}, "format_failures": fmt, "format_rate": fmt_rate, "pack_size": len(pack)}
    obs_all = []
    for seed in PILOT_SEEDS:
        probes, hidden = make_probe_suite(seed), make_hidden_suite(seed)
        inst = make_instance(seed)
        rows, corr, incorr = [], 0, 0
        for name, fn in solvers:
            r = evaluate_pair(fn, probes, hidden)
            k = r["k"]
            # recompute hidden successes (input-level)
            from study.features import _norm_ref
            from study.sssp import dijkstra_ref as dr
            succ = 0
            for h in hidden:
                exp = _norm_ref(dr(h["n"], h["edges"], h["s"], h["t"]))
                try:
                    out = fn(h["n"], h["edges"], h["s"], h["t"])
                    ok = not isinstance(out, bool) and isinstance(out, int) and out == exp
                except Exception:
                    ok = False
                succ += 1 if ok else 0
            elig = k >= 2
            rows.append({"solver": name, "k": k, "C": r["C"], "successes": succ, "eligible": elig})
            if elig:
                corr += succ
                incorr += (HIDDEN_M - succ)
                obs_all.append({"instance": seed, "k": k, "C": r["C"], "successes": succ, "fails": r["fails"]})
        elig_n = sum(1 for r_ in rows if r_["eligible"])
        tot = corr + incorr
        c_rate = corr / tot if tot else 0.0
        i_rate = incorr / tot if tot else 0.0
        results["instances"][str(seed)] = {
            "anchor_n": inst["n"], "eligible_pairs": elig_n, "total_pairs": len(rows),
            "hidden_correct_rate": c_rate, "hidden_incorrect_rate": i_rate, "rows": rows,
        }
        print(f"seed {seed}: eligible={elig_n}  corr_rate={c_rate:.3f}  incorr_rate={i_rate:.3f}")

    gate1 = all(results["instances"][str(s)]["eligible_pairs"] >= MIN_ELIGIBLE for s in PILOT_SEEDS)
    gate2 = all(
        results["instances"][str(s)]["hidden_correct_rate"] >= MIN_CORR
        and results["instances"][str(s)]["hidden_incorrect_rate"] >= MIN_INCORR
        for s in PILOT_SEEDS
    )
    fmt_ok = fmt_rate <= 0.20
    passed = gate1 and gate2 and fmt_ok
    results.update({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gate1_yield": gate1, "gate2_variation": gate2, "format_ok": fmt_ok,
        "eligible_observations": obs_all,
        "decision": "PASS -> confirmatory" if passed else "INFEASIBLE -> stop",
    })
    out = ROOT / "v02" / "pilot_v02"
    out.mkdir(exist_ok=True)
    (out / "pilot_v02_report.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps({k: results[k] for k in ["gate1_yield", "gate2_variation", "format_ok", "decision"]}, indent=2))


if __name__ == "__main__":
    main()
