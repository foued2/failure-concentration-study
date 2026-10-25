"""Offline power planning for the next natural-solver study.

The script simulates a stratified C-score contrast under a prespecified null
and prespecified alternatives. It uses no repository outcome data and makes no
network or model calls.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

N_EVAL = 200
K_LEVELS = (2, 6, 12, 24)
ALPHA = 0.05
PERMUTATIONS = 199
BASE_SEED = 20261022
BETA_GRID = (0.03, 0.06, 0.10, 0.15, 0.20)
N_GRID = (2, 3, 5, 8, 12, 20, 30, 40)
RHO_GRID = (0.0, 0.01, 0.05)
NULL_N = (2, 5, 10, 20, 40)
YIELD_BETAS = (0.06, 0.10)
YIELD_RHOS = (0.01, 0.05)
YIELD_N_REQUESTED = (8, 12, 20)
YIELD_SCENARIOS = (
    (0.0, 0.0),
    (0.25, 0.0),
    (0.50, 0.0),
    (0.0, 0.20),
    (0.0, 0.40),
    (0.25, 0.20),
    (0.50, 0.40),
    (0.50, 0.50),
)
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "next-task" / "power_simulation" / "results"


def c_bounds(k: int) -> tuple[float, float]:
    return math.ceil(k / 6) / k, 1.0


def baseline_probability(k: int) -> float:
    return 0.90 - 0.0125 * k


def score(rng: random.Random, probability: float, rho: float) -> float:
    probability = min(0.995, max(0.005, probability))
    if rho <= 0.0:
        successes = rng.binomialvariate(N_EVAL, probability)
    else:
        phi = (1.0 - rho) / rho
        body_probability = rng.betavariate(probability * phi, (1.0 - probability) * phi)
        successes = rng.binomialvariate(N_EVAL, body_probability)
    return successes / N_EVAL


def stratified_slope_test(
    rows: list[tuple[int, float, float]],
    permutations: int,
    rng: random.Random,
) -> tuple[float | None, int]:
    groups: dict[int, list[tuple[float, float]]] = defaultdict(list)
    for k, concentration, value in rows:
        groups[k].append((concentration, value))
    centered: list[tuple[list[float], list[float]]] = []
    for values in groups.values():
        counts = Counter(concentration for concentration, _ in values)
        if len(counts) < 2 or min(counts.values()) < 2:
            continue
        n = len(values)
        c_mean = sum(concentration for concentration, _ in values) / n
        s_mean = sum(value for _, value in values) / n
        c_centered = [concentration - c_mean for concentration, _ in values]
        s_centered = [value - s_mean for _, value in values]
        if sum(value * value for value in c_centered) <= 1e-15:
            continue
        centered.append((c_centered, s_centered))
    if not centered:
        return None, 0
    observed = sum(
        sum(a * b for a, b in zip(c_values, s_values))
        for c_values, s_values in centered
    )
    hits = 0
    for _ in range(permutations):
        permuted = 0
        for c_values, s_values in centered:
            shuffled = s_values[:]
            rng.shuffle(shuffled)
            permuted += sum(a * b for a, b in zip(c_values, shuffled))
        if abs(permuted) >= abs(observed) - 1e-15:
            hits += 1
    return (1 + hits) / (permutations + 1), len(centered)


def simulate(
    beta: float,
    n_cell: int,
    rho: float,
    replicates: int,
    permutations: int,
    seed: int,
    requested_cell: int | None = None,
    yield_rate: float = 1.0,
) -> dict:
    rng = random.Random(seed)
    rejections = 0
    estimable = 0
    analyzed_bodies: list[int] = []
    usable_k_levels: list[int] = []
    for _ in range(replicates):
        rows: list[tuple[int, float, float]] = []
        for k in K_LEVELS:
            low, high = c_bounds(k)
            c_mid = (low + high) / 2.0
            count = n_cell
            if requested_cell is not None:
                count = rng.binomialvariate(requested_cell, yield_rate)
            for concentration in (low, high):
                probability = baseline_probability(k) + beta * (concentration - c_mid)
                for _ in range(count):
                    rows.append((k, concentration, score(rng, probability, rho)))
        p_value, usable_k = stratified_slope_test(rows, permutations, rng)
        analyzed_bodies.append(len(rows))
        usable_k_levels.append(usable_k)
        if p_value is not None:
            estimable += 1
            if p_value <= ALPHA:
                rejections += 1
    return {
        "beta": beta,
        "rho": rho,
        "n_cell": n_cell,
        "requested_cell": requested_cell,
        "yield_rate": yield_rate,
        "replicates": replicates,
        "permutations": permutations,
        "rejections": rejections,
        "conditional_power": rejections / estimable if estimable else None,
        "operational_power": rejections / replicates,
        "estimable_rate": estimable / replicates,
        "mean_analyzed_bodies": sum(analyzed_bodies) / len(analyzed_bodies),
        "mean_usable_k_levels": sum(usable_k_levels) / len(usable_k_levels),
    }


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total == 0:
        return (0.0, 0.0)
    p = successes / total
    denominator = 1.0 + z * z / total
    center = (p + z * z / (2.0 * total)) / denominator
    margin = z * math.sqrt(p * (1.0 - p) / total + z * z / (4.0 * total * total)) / denominator
    return max(0.0, center - margin), min(1.0, center + margin)


def run_power_grid(replicates: int, permutations: int) -> list[dict]:
    rows: list[dict] = []
    for rho in RHO_GRID:
        for beta in BETA_GRID:
            for n_cell in N_GRID:
                result = simulate(
                    beta=beta,
                    n_cell=n_cell,
                    rho=rho,
                    replicates=replicates,
                    permutations=permutations,
                    seed=BASE_SEED + int(rho * 1000) * 10000 + int(beta * 1000) * 100 + n_cell,
                )
                result["total_planned_bodies"] = len(K_LEVELS) * 2 * n_cell
                result["kind"] = "power"
                rows.append(result)
    return rows


def run_null_calibration(replicates: int, permutations: int) -> list[dict]:

    rows: list[dict] = []
    for rho in RHO_GRID:
        for n_cell in NULL_N:
            result = simulate(
                beta=0.0,
                n_cell=n_cell,
                rho=rho,
                replicates=replicates,
                permutations=permutations,
                seed=BASE_SEED + 700000 + int(rho * 1000) * 10000 + n_cell,
            )
            low, high = wilson_interval(result["rejections"], replicates)
            result.update({
                "kind": "null",
                "fpr": result["rejections"] / replicates,
                "fpr_wilson_low": low,
                "fpr_wilson_high": high,
                "total_planned_bodies": len(K_LEVELS) * 2 * n_cell,
            })
            rows.append(result)
    return rows


def required_cells(power_rows: list[dict]) -> list[dict]:
    result: list[dict] = []
    for rho in RHO_GRID:
        for beta in BETA_GRID:
            candidates = [
                row for row in power_rows
                if row["rho"] == rho and row["beta"] == beta
                and row["conditional_power"] is not None
                and row["conditional_power"] >= 0.80
            ]
            if not candidates:
                result.append({
                    "rho": rho,
                    "beta": beta,
                    "required_n_cell": None,
                    "total_bodies": None,
                    "note": f"not reached through n_cell={max(N_GRID)}",
                })
                continue
            best = min(candidates, key=lambda row: row["n_cell"])
            result.append({
                "rho": rho,
                "beta": beta,
                "required_n_cell": best["n_cell"],
                "total_bodies": best["total_planned_bodies"],
                "conditional_power": best["conditional_power"],
                "note": "",
            })
    return result


def run_yield_sensitivity(replicates: int, permutations: int) -> list[dict]:
    rows: list[dict] = []
    for rho in YIELD_RHOS:
        for beta in YIELD_BETAS:
            for requested in YIELD_N_REQUESTED:
                for duplicate_rate, ineligible_rate in YIELD_SCENARIOS:
                    yield_rate = (1.0 - duplicate_rate) * (1.0 - ineligible_rate)
                    result = simulate(
                        beta=beta,
                        n_cell=requested,
                        rho=rho,
                        replicates=replicates,
                        permutations=permutations,
                        seed=(
                            BASE_SEED + 900000
                            + int(rho * 1000) * 100000
                            + int(beta * 1000) * 1000
                            + requested * 10
                            + int(duplicate_rate * 100)
                            + int(ineligible_rate * 1000)
                        ),
                        requested_cell=requested,
                        yield_rate=yield_rate,
                    )
                    result.update({
                        "kind": "yield",
                        "duplicate_rate": duplicate_rate,
                        "ineligible_rate": ineligible_rate,
                        "planned_requests_per_condition": requested * len(K_LEVELS) * 2,
                    })
                    rows.append(result)
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: Iterable[dict]) -> None:
    rows = list(rows)
    if not rows:
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=400)
    parser.add_argument("--null-replicates", type=int, default=1000)
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--null-permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--yield-permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)
    counts = (args.replicates, args.null_replicates, args.permutations,
              args.null_permutations, args.yield_permutations)
    if any(count < 1 for count in counts):
        raise SystemExit("all replicate and permutation counts must be positive")
    args.out.mkdir(parents=True, exist_ok=True)
    power_rows = run_power_grid(args.replicates, args.permutations)
    null_rows = run_null_calibration(args.null_replicates, args.null_permutations)
    yield_rows = run_yield_sensitivity(args.replicates, args.yield_permutations)
    required = required_cells(power_rows)
    metadata = {
        "status": "OFFLINE_SIMULATION_COMPLETE_NO_GENERATION",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "code_sha256": sha256_file(Path(__file__).resolve()),
        "seed": BASE_SEED,
        "n_eval": N_EVAL,
        "k_levels": list(K_LEVELS),
        "alpha": ALPHA,
        "permutations": args.permutations,
        "null_permutations": args.null_permutations,
        "yield_permutations": args.yield_permutations,
        "power_replicates": args.replicates,
        "null_replicates": args.null_replicates,
        "baseline_probability": "0.90 - 0.0125*k",
        "c_low": "ceil(k/6)/k",
        "c_high": "1.0",
        "alternative": "p(k,C) = baseline(k) + beta*(C - midpoint(C_low,C_high))",
        "score_model": "Binomial(200,p); rho>0: p_i~Beta(mean=p, ICC=rho), X~Binomial(200,p_i)",
        "duplicate_or_execution_loss": "Binomial thinning with yield=(1-duplicate_rate)*(1-ineligible_rate)",
        "yield_model_limit": "Thinning approximates loss of independent bodies; it is not a clustered-duplicate model.",
    }
    combined = {
        "metadata": metadata,
        "required_n": required,
        "null": null_rows,
        "power_grid": power_rows,
        "yield": yield_rows,
    }
    (args.out / "POWER_SIMULATION_RESULTS.json").write_text(
        json.dumps(combined, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(args.out / "POWER_SIMULATION_GRID.csv", power_rows)
    write_csv(args.out / "POWER_SIMULATION_NULL.csv", null_rows)
    write_csv(args.out / "POWER_SIMULATION_YIELD.csv", yield_rows)
    (args.out / "POWER_SIMULATION_METADATA.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": metadata["status"],
        "code_sha256": metadata["code_sha256"],
        "power_rows": len(power_rows),
        "null_rows": len(null_rows),
        "yield_rows": len(yield_rows),
        "required": required,
        "out": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
