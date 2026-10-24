from __future__ import annotations

import argparse
import gzip
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Iterator, Sequence

MATH_DIR = Path(__file__).resolve().parent
DEFAULT_OUTDIR = MATH_DIR / "results" / "three_world"
sys.path.insert(0, str(MATH_DIR))

import simulate_worlds as sim


def case_from_record(record: dict[str, object]) -> sim.Case:
    return sim.Case(
        f=tuple(int(value) for value in record["F"]),
        e=tuple(int(value) for value in record["E"]),
        bits=tuple(int(value) for value in str(record["diag_bits"])),
        f_alt=tuple(int(value) for value in record["F_alt"]),
        k=int(record["k"]),
        c=float(record["C"]) if record["C"] is not None else None,
        c_alt=float(record["C_alt"]) if record["C_alt"] is not None else None,
        carrier=int(record["carrier"]),
        home_counts=tuple(int(value) for value in record["home_counts"]),
        defects=int(record["defects"]),
        world=str(record["world"]),
        s_domain=float(record["S_domain"]),
        s_equal=float(record["S_equal"]),
    )


def iter_trials(path: Path) -> Iterator[tuple[int, list[dict[str, object]]]]:
    current_trial: int | None = None
    records: list[dict[str, object]] = []
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            trial = int(record["trial"])
            if current_trial is None:
                current_trial = trial
            if trial != current_trial:
                yield current_trial, records
                current_trial = trial
                records = []
            records.append(record)
    if current_trial is not None:
        yield current_trial, records


def interval(values: Sequence[float]) -> dict[str, float]:
    if not values:
        return {
            "mean": float("nan"),
            "low": float("nan"),
            "high": float("nan"),
            "positive_fraction": float("nan"),
        }
    return {
        "mean": sum(values) / len(values),
        "low": sim.quantile(values, 0.025),
        "high": sim.quantile(values, 0.975),
        "positive_fraction": sum(1 for value in values if value > 0) / len(values),
    }


def trial_sensitivity(
    eligible_by_fold: list[dict[int, sim.ZStat]],
) -> dict[str, object]:
    categories = sorted({k for mapping in eligible_by_fold for k in mapping})
    width = len(sim.ELIGIBLE_FEATURES)
    model_features = {
        "M0fam": sim.FAM_INDICES,
        "M1fam": (sim.C_INDEX,) + sim.FAM_INDICES,
    }
    totals: dict[str, dict[str, dict[str, float]]] = {
        subset: {score: {model: 0.0 for model in model_features} for score in ("domain", "equal")}
        for subset in ("all", "represented", "omitted")
    }
    counts = {subset: 0 for subset in totals}
    for fold in range(sim.FOLDS):
        train_stats = sim.merge_z_stats(
            eligible_by_fold[other] for other in range(sim.FOLDS) if other != fold
        )
        train_k = set(train_stats)
        train, _, _ = sim.assemble_design(train_stats, categories, width)
        test_stats = eligible_by_fold[fold]
        subsets = {
            "all": test_stats,
            "represented": {k: stat for k, stat in test_stats.items() if k in train_k},
            "omitted": {k: stat for k, stat in test_stats.items() if k not in train_k},
        }
        for subset_name, subset in subsets.items():
            subset_n = sum(stat.n for stat in subset.values())
            if subset_n == 0:
                continue
            test, test_y2_domain, test_y2_equal = sim.assemble_design(subset, categories, width)
            counts[subset_name] += subset_n
            for model, feature_indices in model_features.items():
                columns = sim.model_columns(categories, feature_indices)
                for score in ("domain", "equal"):
                    test_y2 = test_y2_domain if score == "domain" else test_y2_equal
                    sse, _ = sim.subset_sse(train, test, test_y2, columns, score)
                    totals[subset_name][score][model] += sse
    output: dict[str, object] = {"n_cases": counts}
    for subset_name in totals:
        output[subset_name] = {}
        for score in ("domain", "equal"):
            denominator = counts[subset_name]
            m0 = totals[subset_name][score]["M0fam"] / denominator if denominator else float("nan")
            m1 = totals[subset_name][score]["M1fam"] / denominator if denominator else float("nan")
            output[subset_name][score] = {
                "M0fam": m0,
                "M1fam": m1,
                "delta": m0 - m1,
            }
    return output


def analyze_setting(
    key: str,
    raw_path: Path,
    per_trial_records: dict[int, dict[str, object]],
    do_sensitivity: bool,
) -> dict[str, object]:
    eligible_by_fold: list[dict[int, sim.ZStat]] = [
        defaultdict(lambda: sim.ZStat(len(sim.ELIGIBLE_FEATURES))) for _ in range(sim.FOLDS)
    ]
    all_k_by_fold: list[Counter] = [Counter() for _ in range(sim.FOLDS)]
    overlap_counts: Counter = Counter()
    total_cases = 0
    eligible_cases = 0
    k0_cases = 0
    folds_with_unseen = 0
    affected_cases = 0
    unseen_k_instances = 0
    unseen_k_global: set[int] = set()
    unseen_cases_by_k: Counter = Counter()
    unseen_by_trial: list[dict[str, object]] = []
    full_scored = 0
    full_omitted = 0
    full_omitted_k0 = 0
    full_omitted_unseen_eligible = 0
    sensitivity_trials: list[dict[str, object]] = []
    reproduction_errors: list[float] = []

    for trial, records in iter_trials(raw_path):
        trial_total = 0
        trial_eligible = 0
        trial_k0 = 0
        trial_folds_with_unseen = 0
        trial_affected = 0
        trial_unseen_instances = 0
        trial_unseen_levels: set[int] = set()
        trial_fold_details: list[dict[str, object]] = []
        for record in records:
            case = case_from_record(record)
            fold = int(record["fold"])
            trial_total += 1
            all_k_by_fold[fold][case.k] += 1
            if case.k == 0:
                trial_k0 += 1
                continue
            trial_eligible += 1
            eligible_by_fold[fold][case.k].add(sim.eligible_features(case), case)
            c_value = Fraction(max(case.f), case.k)
            overlap_counts[(case.world, case.k, c_value)] += 1

        for fold in range(sim.FOLDS):
            train_k = set().union(
                *(eligible_by_fold[other].keys() for other in range(sim.FOLDS) if other != fold)
            )
            test_stats = eligible_by_fold[fold]
            unseen = sorted(set(test_stats) - train_k)
            fold_affected = sum(test_stats[k].n for k in unseen)
            trial_fold_details.append(
                {
                    "fold": fold,
                    "unseen_k_levels": unseen,
                    "affected_cases": fold_affected,
                }
            )
            if unseen:
                trial_folds_with_unseen += 1
                trial_unseen_instances += len(unseen)
                trial_unseen_levels.update(unseen)
                trial_affected += fold_affected
                for k in unseen:
                    unseen_cases_by_k[k] += test_stats[k].n

        for fold in range(sim.FOLDS):
            train_k = set().union(
                *(all_k_by_fold[other].keys() for other in range(sim.FOLDS) if other != fold)
            )
            test_counts = all_k_by_fold[fold]
            scored = sum(count for k, count in test_counts.items() if k in train_k)
            omitted = sum(count for k, count in test_counts.items() if k not in train_k)
            full_scored += scored
            full_omitted += omitted
            if 0 not in train_k:
                full_omitted_k0 += test_counts.get(0, 0)
            full_omitted_unseen_eligible += sum(
                count for k, count in test_counts.items() if k > 0 and k not in train_k
            )

        folds_with_unseen += trial_folds_with_unseen
        affected_cases += trial_affected
        unseen_k_instances += trial_unseen_instances
        unseen_k_global.update(trial_unseen_levels)
        unseen_by_trial.append(
            {
                "trial": trial,
                "folds_with_unseen_k": trial_folds_with_unseen,
                "affected_eligible_cases": trial_affected,
                "unseen_k_instances": trial_unseen_instances,
                "unseen_k_levels": sorted(trial_unseen_levels),
                "folds": trial_fold_details,
            }
        )

        if do_sensitivity:
            trial_result = trial_sensitivity(eligible_by_fold)
            expected = per_trial_records.get(trial)
            if expected is None:
                raise RuntimeError(f"missing per-trial record for {key} trial {trial}")
            for score in ("domain", "equal"):
                observed = float(trial_result["all"][score]["delta"])
                expected_delta = float(expected["delta_pred"][score])
                reproduction_errors.append(abs(observed - expected_delta))
            trial_result["trial"] = trial
            sensitivity_trials.append(trial_result)

        total_cases += trial_total
        eligible_cases += trial_eligible
        k0_cases += trial_k0
        eligible_by_fold = [
            defaultdict(lambda: sim.ZStat(len(sim.ELIGIBLE_FEATURES))) for _ in range(sim.FOLDS)
        ]
        all_k_by_fold = [Counter() for _ in range(sim.FOLDS)]

    output: dict[str, object] = {
        "setting": key,
        "total_cases": total_cases,
        "eligible_cases": eligible_cases,
        "k0_cases": k0_cases,
        "fold_fits": sim.TRIALS * sim.FOLDS,
        "folds_with_unseen_k": folds_with_unseen,
        "affected_eligible_cases": affected_cases,
        "affected_fraction": affected_cases / eligible_cases if eligible_cases else float("nan"),
        "unseen_k_instances": unseen_k_instances,
        "unseen_k_global_levels": sorted(unseen_k_global),
        "affected_cases_by_k": {
            str(k): unseen_cases_by_k[k] for k in sorted(unseen_cases_by_k)
        },
        "unseen_by_trial": unseen_by_trial,
        "per_trial_rank_warnings": {
            model: sum(
                int(record["rank_warnings"].get(model, 0))
                for record in per_trial_records.values()
            )
            for model in sorted(next(iter(per_trial_records.values()))["rank_warnings"])
        },
        "full_baseline": {
            "scored_cases": full_scored,
            "omitted_cases": full_omitted,
            "omitted_k0_cases": full_omitted_k0,
            "omitted_unseen_eligible_cases": full_omitted_unseen_eligible,
            "scored_fraction": full_scored / total_cases if total_cases else float("nan"),
            "omitted_fraction": full_omitted / total_cases if total_cases else float("nan"),
        },
        "overlap_by_k_c": [
            {
                "world": world,
                "k": k,
                "C": f"{value.numerator}/{value.denominator}",
                "C_decimal": float(value),
                "cases": count,
            }
            for (world, k, value), count in sorted(
                overlap_counts.items(), key=lambda item: (item[0][0], item[0][1], item[0][2])
            )
        ],
    }
    if do_sensitivity:
        if reproduction_errors and max(reproduction_errors) > 1e-8:
            raise RuntimeError(
                f"{key} sensitivity did not reproduce per-trial deltas; max error "
                f"{max(reproduction_errors):.3e}"
            )
        output["sensitivity"] = {
            "method": (
                "Original folds and training data; M0fam and M1fam are fitted once per fold "
                "and scored on the same held-out subset. 'represented' keeps only eligible "
                "test cases whose k occurs in that fold's training data; 'omitted' keeps the "
                "complement. The original estimate is unchanged and reported separately."
            ),
            "reproduction_max_abs_error": max(reproduction_errors) if reproduction_errors else 0.0,
            "trials": sensitivity_trials,
        }
        for subset_name in ("all", "represented", "omitted"):
            subset_output: dict[str, object] = {
                "n_trials": sum(
                    1 for trial in sensitivity_trials if int(trial["n_cases"][subset_name]) > 0
                ),
                "n_cases": sum(int(trial["n_cases"][subset_name]) for trial in sensitivity_trials),
            }
            for score in ("domain", "equal"):
                values = [
                    float(trial[subset_name][score]["delta"])
                    for trial in sensitivity_trials
                    if int(trial["n_cases"][subset_name]) > 0
                ]
                baselines = [
                    float(trial[subset_name][score]["M0fam"])
                    for trial in sensitivity_trials
                    if int(trial["n_cases"][subset_name]) > 0
                ]
                subset_output[score] = {
                    "delta": interval(values),
                    "baseline": interval(baselines),
                }
            output["sensitivity"][subset_name] = subset_output
    return output


def write_overlap_markdown(path: Path, settings: dict[str, dict[str, object]]) -> None:
    lines = [
        "# Overlap case counts by k and C",
        "",
        "Counts are eligible cases (k > 0) pooled over the 500 original trials. C is exact",
        "max(F)/k; the decimal column is display only. These are synthetic cases.",
        "",
    ]
    for setting, data in settings.items():
        lines.extend([f"## {setting}", "", "| World | k | C | C decimal | Cases |", "| --- | ---: | ---: | ---: | ---: |"])
        for entry in data["overlap_by_k_c"]:
            lines.append(
                f"| {entry['world']} | {entry['k']} | {entry['C']} | "
                f"{entry['C_decimal']:.12g} | {entry['cases']} |"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def load_manifest(outdir: Path) -> dict[str, object]:
    return json.loads((outdir / "manifest.json").read_text(encoding="utf-8"))


def verify_raw_hashes(outdir: Path, manifest: dict[str, object]) -> None:
    for key, info in manifest["raw"].items():
        path = outdir / str(info["path"]).replace("\\", "/")
        observed = sim.sha256_file(path)
        if observed != info["sha256"]:
            raise RuntimeError(f"raw hash mismatch for {key}: {observed} != {info['sha256']}")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--overlap-markdown", type=Path, default=None)
    parser.add_argument("--verify-hashes", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    outdir = args.outdir
    manifest = load_manifest(outdir)
    if args.verify_hashes:
        verify_raw_hashes(outdir, manifest)
    per_trial = json.loads((outdir / "per_trial.json").read_text(encoding="utf-8"))
    per_trial_by_setting: dict[str, dict[int, dict[str, object]]] = defaultdict(dict)
    for record in per_trial:
        per_trial_by_setting[str(record["setting"])][int(record["trial"])] = record
    settings: dict[str, dict[str, object]] = {}
    for key in manifest["settings"]:
        key = str(key)
        raw_path = outdir / str(manifest["raw"][key]["path"]).replace("\\", "/")
        print(f"analyzing {key}", file=sys.stderr)
        settings[key] = analyze_setting(
            key,
            raw_path,
            per_trial_by_setting[key],
            key == "W1",
        )
    output = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "outdir": str(outdir),
            "raw_hashes_verified": bool(args.verify_hashes),
            "trials": int(manifest["trials"]),
            "cases": int(manifest["cases"]),
            "base_seed": int(manifest["base_seed"]),
        },
        "settings": settings,
    }
    output_path = args.output or outdir / "12_review_correction_metrics.json"
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    overlap_path = args.overlap_markdown or outdir / "12_overlap_by_k_c.md"
    write_overlap_markdown(overlap_path, settings)
    print(f"wrote {output_path}", file=sys.stderr)
    print(f"wrote {overlap_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
