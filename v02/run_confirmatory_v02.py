"""v0.2 confirmatory: 40 instances, LOIO, real vs 200 relabelings, terminal classification."""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from models_v02 import bootstrap_ci, build_pairs, classify, loo_delta_pairs, relabel_control
from study.features import _norm_ref, load_solver
from study.instances import make_hidden_suite, make_instance
from study.probes import make_probe_suite
from study.sssp import dijkstra_ref

DELTA = 0.01
R = 200
PILOT_SEEDS = {101, 102, 103}
CONF_N = 40


def confirmatory_seeds(proto_hash16: str) -> list[int]:
    seeds = []
    for i in range(CONF_N):
        s = int.from_bytes(hashlib.sha256(f"{proto_hash16}:confirmatory:{i}".encode()).digest()[:4], "big") % 10**7
        while s in PILOT_SEEDS:
            s += 1
        seeds.append(s)
    return seeds


def main() -> None:
    freeze = (ROOT / "v02" / "FREEZE_V02.md").read_text(encoding="utf-8")
    proto_hash16 = freeze.split("**v0.2 protocol hash:** `")[1][:16]
    seeds = confirmatory_seeds(proto_hash16)
    print(f"confirmatory seeds (first 5): {seeds[:5]}")

    pack = sorted((ROOT / "generation_v02" / "pack").glob("solver_*.py"))
    solvers = [load_solver(p) for p in pack]
    print(f"pack: {len(solvers)}")

    # G3 on all confirmatory hidden sets
    from study.sssp import brute_force_min
    mism = 0
    for seed in seeds:
        for h in make_hidden_suite(seed):
            if dijkstra_ref(h["n"], h["edges"], h["s"], h["t"]) != brute_force_min(h["n"], h["edges"], h["s"], h["t"]):
                mism += 1
    print(f"G3 confirmatory hidden sets: {mism} mismatches")
    assert mism == 0

    obs = []
    for si, seed in enumerate(seeds):
        probes, hidden = make_probe_suite(seed), make_hidden_suite(seed)
        for name, fn in solvers:
            from study.features import concentration, run_probes
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
            obs.append({"instance": seed, "k": k, "C": c, "successes": succ, "fails": fails})
        if (si + 1) % 10 == 0:
            print(f"  scored {si + 1}/{len(seeds)} instances; eligible pairs so far: {len(obs)}")

    pairs = build_pairs(obs)
    delta_i, delta = loo_delta_pairs(pairs)
    ci_lo, ci_hi = bootstrap_ci(delta_i)
    print(f"real delta={delta:.6f} CI=({ci_lo:.6f},{ci_hi:.6f}); running {R} relabelings...")
    t0 = time.time()
    rel = relabel_control(obs, r_max=R)
    rel_sorted = sorted(x for x in rel if x == x)
    p95 = rel_sorted[int(0.95 * len(rel_sorted))]
    print(f"relabel done in {time.time() - t0:.0f}s; p95={p95:.6f}")

    outcome = classify(delta, ci_lo, ci_hi, p95, DELTA)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(), "proto_hash16": proto_hash16,
        "n_confirmatory_instances": len(seeds), "eligible_pairs": len(obs),
        "delta": delta, "delta_i": delta_i, "ci": [ci_lo, ci_hi],
        "relabel_p95": p95, "relabel_mean": sum(rel_sorted) / len(rel_sorted),
        "threshold": DELTA, "outcome": outcome,
    }
    out = ROOT / "v02" / "confirmatory_v02"
    out.mkdir(exist_ok=True)
    (out / "confirmatory_v02_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (out / "RESULT_V02.md").write_text(
        f"# v0.2 Terminal Result\n\n**Outcome: {outcome}**\n\n"
        f"- Δ = {delta:.6f} nats/hidden-input (threshold {DELTA})\n"
        f"- 95% CI: [{ci_lo:.6f}, {ci_hi:.6f}]\n"
        f"- Relabel p95: {p95:.6f}\n"
        f"- Confirmatory instances: {len(seeds)}; eligible pairs: {len(obs)}\n\n"
        f"Terminal per protocol §6. No follow-up authorized.\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["delta", "ci", "relabel_p95", "outcome"]}, indent=2))


if __name__ == "__main__":
    main()
