from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"
PROFILES = ROOT / "profiles" / "selected_profiles.json"
TRIALS = 20_000
SEED = 20261023
DELTA = 0.10
SIGMAS = (0.10, 0.15, 0.20, 0.25)
HIGH_SLOTS = 120
LOW_SLOTS = 30
CRITICAL = 1.6448536269514722
POWER_Z = 0.8416212335729143


def design() -> tuple[list[float], list[float]]:
    selected = json.loads(PROFILES.read_text(encoding="utf-8"))
    high: list[float] = []
    low: list[float] = []
    for target in selected["targets"]:
        if target["C"] == 1.0:
            high.extend([1.0] * int(target["assigned_slots"]))
        elif target["C"] == 0.2:
            low.extend([0.0] * int(target["assigned_slots"]))
    if len(high) != HIGH_SLOTS or len(low) != LOW_SLOTS:
        raise AssertionError((len(high), len(low)))
    return high, low


def fit_power(sigma: float, rng: random.Random, delta: float) -> float:
    high, low = design()
    se = sigma * math.sqrt(1.0 / len(high) + 1.0 / len(low))
    hits = 0
    for _ in range(TRIALS):
        high_mean = sum(0.5 + delta + rng.gauss(0.0, sigma) for _ in high) / len(high)
        low_mean = sum(0.5 + rng.gauss(0.0, sigma) for _ in low) / len(low)
        if (high_mean - low_mean) / se > CRITICAL:
            hits += 1
    return hits / TRIALS


def analytic_mde(sigma: float) -> float:
    return (CRITICAL + POWER_Z) * sigma * math.sqrt(1.0 / HIGH_SLOTS + 1.0 / LOW_SLOTS)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    design()
    rng = random.Random(SEED)
    rows = []
    for sigma in SIGMAS:
        power = fit_power(sigma, rng, DELTA)
        null = fit_power(sigma, rng, 0.0)
        rows.append({
            "residual_sd": sigma,
            "power_at_delta_0_10": power,
            "null_rejection_rate": null,
            "mde_at_80_percent": analytic_mde(sigma),
            "n_high": HIGH_SLOTS,
            "n_low": LOW_SLOTS,
        })
        print(json.dumps(rows[-1]), flush=True)
    identification_failures = [
        "the six C=1 targets use six different carrier families, so C is not separated from carrier family",
        "there is no within-carrier fixed-k contrast between high and low C",
        "the only C=0.2 target is one spread pattern, not a family-balanced low-C design",
    ]
    power_failures = [
        f"power {row['power_at_delta_0_10']:.5f} below 0.80 at residual SD {row['residual_sd']:.2f}"
        for row in rows
        if row["power_at_delta_0_10"] < 0.80
    ]
    result = {
        "schema": 1,
        "status": "OFFLINE_POWER_AND_IDENTIFICATION_ANALYSIS",
        "model_calls": 0,
        "generated_solvers": 0,
        "task": "paren7_min_insertions",
        "trials": TRIALS,
        "seed": SEED,
        "delta": DELTA,
        "estimator": "difference of mean S between high-C and low-C slots (high-minus-low coded 1/0); one-sided normal test",
        "design": {
            "high_C_slots": HIGH_SLOTS,
            "low_C_slots": LOW_SLOTS,
            "k": 5,
            "C_high": 1.0,
            "C_low": 0.2,
            "effect_coding": "high C=1, low C=0; delta is the high-minus-low difference",
            "generator_identity": "not included in this planning model; the study model adds it as a fixed effect",
        },
        "table": rows,
        "identification_failures": identification_failures,
        "power_failures": power_failures,
        "verdict": "HOLD",
        "gate2_authorized": False,
        "notes": [
            "No empirical residual-SD estimate exists. The table is a sensitivity analysis, not validation.",
            "Calibration controls are hand-built and do not estimate the study population variance.",
            "The MDE is analytic for the two-group design and is reported alongside the simulation.",
        ],
    }
    (OUT / "power_analysis.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (OUT / "power_table.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["residual_sd", "power_at_delta_0_10", "null_rejection_rate", "mde_at_80_percent"])
        for row in rows:
            writer.writerow([row["residual_sd"], row["power_at_delta_0_10"], row["null_rejection_rate"], row["mde_at_80_percent"]])
    print(json.dumps({"verdict": "HOLD", "identification_failures": identification_failures, "power_failures": power_failures}, indent=2))


if __name__ == "__main__":
    main()
