"""ABORTED 2026-10-12 per integrity directive (GPT): do NOT re-execute to export the
full relabel vector. The full 200-draw vector was not persisted by the completed
frozen run; only p95 and mean are reported (disclosed as a record limitation in
REPORT_V02.md). This script was started, aborted mid-relabel, produced no output
files, and is retained for history only. Must not be run.

Prior docstring:
Complete the v0.2 record (2026-10-12).

Part A/B: EXPLORATORY post-hoc summaries (labeled as such in REPORT_V02.md).
Part C: full randomized-label vector export — deterministic re-execution of the
frozen relabel_control (same seeds, same code, same obs); identity is proven by
asserting p95/mean match the terminal report already written by the frozen runner.
Does not change the terminal outcome, which is already recorded.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from models_v02 import relabel_control
from study.features import _norm_ref, concentration, load_solver, run_probes
from study.instances import make_hidden_suite
from study.probes import make_probe_suite
from study.sssp import dijkstra_ref

CONF = ROOT / "v02" / "confirmatory_v02"


def confirmatory_seeds(proto_hash16: str) -> list[int]:
    import hashlib
    seeds = []
    for i in range(40):
        s = int.from_bytes(hashlib.sha256(f"{proto_hash16}:confirmatory:{i}".encode()).digest()[:4], "big") % 10**7
        while s in {101, 102, 103}:
            s += 1
        seeds.append(s)
    return seeds


def score_all() -> list[dict]:
    pack = sorted((ROOT / "generation_v02" / "pack").glob("solver_*.py"))
    solvers = [(p.stem, load_solver(p)) for p in pack]
    report = json.loads((CONF / "confirmatory_v02_report.json").read_text(encoding="utf-8"))
    obs = []
    for seed in confirmatory_seeds(report["proto_hash16"]):
        probes, hidden = make_probe_suite(seed), make_hidden_suite(seed)
        for name, fn in solvers:
            fails = run_probes(fn, probes)
            k, c = concentration(fails)
            if k < 2:
                continue
            succ = 0
            for h in hidden:
                exp = _norm_ref(dijkstra_ref(h["n"], h["edges"], h["s"], h["t"]))
                try:
                    out = fn(h["n"], h["edges"], h["s"], h["t"])
                    ok = not isinstance(out, bool) and isinstance(out, int) and out == exp
                except Exception:
                    ok = False
                succ += 1 if ok else 0
            obs.append({"instance": seed, "solver": name, "k": k, "C": c,
                        "successes": succ, "fails": fails})
    return obs


def summaries(obs: list[dict]) -> dict:
    by_inst: dict[int, list[dict]] = {}
    for o in obs:
        by_inst.setdefault(o["instance"], []).append(o)
    eligible_counts = {str(i): len(v) for i, v in by_inst.items()}

    solver_inst: dict[str, int] = {}
    for o in obs:
        solver_inst[o["solver"]] = solver_inst.get(o["solver"], 0) + 1
    always = sum(1 for v in solver_inst.values() if v == 40)

    signatures = {tuple(o["fails"]) for o in obs}

    k_group: dict[int, list[float]] = {}
    for o in obs:
        k_group.setdefault(o["k"], []).append(o["successes"] / 20.0)

    def _stats(vals: list[float]) -> dict:
        m = sum(vals) / len(vals)
        sd = math.sqrt(sum((v - m) ** 2 for v in vals) / max(len(vals) - 1, 1))
        return {"n": len(vals), "mean": m, "sd": sd, "min": min(vals), "max": max(vals)}

    k_stratified = {str(k): _stats(v) for k, v in sorted(k_group.items())}

    within_k_var = 0
    for inst, rows in by_inst.items():
        g: dict[int, list[float]] = {}
        for r in rows:
            g.setdefault(r["k"], []).append(r["successes"])
        for k, v in g.items():
            if len(v) > 1 and max(v) != min(v):
                within_k_var += 1

    return {
        "eligible_pairs_per_instance": {
            "min": min(eligible_counts.values()), "max": max(eligible_counts.values()),
            "mean": sum(eligible_counts.values()) / len(eligible_counts)},
        "distinct_solvers_ever_eligible": len(solver_inst),
        "solvers_eligible_in_all_40_instances": always,
        "distinct_fail_signatures": len(signatures),
        "k_stratified_success_rate": k_stratified,
        "instance_k_cells_with_within_cell_variation": within_k_var,
    }


def main() -> None:
    report = json.loads((CONF / "confirmatory_v02_report.json").read_text(encoding="utf-8"))
    print("scoring (deterministic re-execution of frozen pipeline)...", flush=True)
    obs = score_all()
    print(f"obs: {len(obs)} eligible pairs", flush=True)

    sup = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "labels": {
            "summaries": "exploratory post-hoc",
            "relabel_vector": "deterministic re-execution of frozen relabel_control; identity asserted vs terminal report",
        },
        "exploratory_summaries": summaries(obs),
    }

    print("relabel vector export R=200 (~54 min)...", flush=True)
    rel = relabel_control(obs, r_max=200)
    rel_finite = sorted(x for x in rel if x == x)
    p95 = rel_finite[int(0.95 * len(rel_finite))]
    mean = sum(rel_finite) / len(rel_finite)
    assert abs(p95 - report["relabel_p95"]) < 1e-15, (p95, report["relabel_p95"])
    assert abs(mean - report["relabel_mean"]) < 1e-15, (mean, report["relabel_mean"])
    sup["relabel_vector"] = {
        "R": len(rel), "values": rel,
        "min": rel_finite[0], "max": rel_finite[-1], "p95": p95, "mean": mean,
        "identity_asserted_vs_terminal_report": True,
    }
    out = CONF / "record_supplements_v02.json"
    out.write_text(json.dumps(sup, indent=2), encoding="utf-8")
    print(json.dumps({
        "p95": p95, "mean": mean, "identity_ok": True,
        "signatures": sup["exploratory_summaries"]["distinct_fail_signatures"],
        "always_eligible": sup["exploratory_summaries"]["solvers_eligible_in_all_40_instances"],
    }, indent=2), flush=True)
    print(f"written: {out}", flush=True)


if __name__ == "__main__":
    main()
