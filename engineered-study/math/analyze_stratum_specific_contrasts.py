#!/usr/bin/env python3
"""Saved-record-only descriptive contrasts of S by C within fixed-k/carrier strata.

Reads only the eight existing JSONL.gz files listed in manifest.json. Verifies
all byte counts, SHA-256 values, and record counts before writing outputs.
No generation, model fitting, tuning, or source-archive modification.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

EVAL_SIZES = (9, 9, 23, 23, 31, 3)
N_EVAL = sum(EVAL_SIZES)
TOL = 1e-12
EXPECTED_RECORDS = 2_500_000


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_atomic(path: Path, data: str) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(data, encoding="utf-8", newline="\n")
    temp.replace(path)


def fmt(x: float | None) -> str:
    return "NOT IDENTIFIABLE" if x is None else f"{x:.7f}"


def inputs_from_manifest(root: Path, manifest: dict[str, Any]) -> list[tuple[str, Path, dict[str, Any]]]:
    raw = manifest.get("raw")
    settings = manifest.get("settings")
    if not isinstance(raw, dict) or not isinstance(settings, list):
        raise ValueError("manifest.json lacks the expected raw/settings fields")
    result = []
    for setting in settings:
        spec = raw[setting]
        path = root / Path(str(spec["path"]).replace("\\", "/"))
        if not path.is_file():
            raise FileNotFoundError(f"Missing saved archive: {path}")
        if path.stat().st_size != int(spec["bytes"]):
            raise ValueError(f"Byte-count mismatch: {path}")
        actual = sha256(path)
        if actual.lower() != str(spec["sha256"]).lower():
            raise ValueError(f"SHA-256 mismatch: {path}")
        if int(spec["records"]) != EXPECTED_RECORDS:
            raise ValueError(f"Unexpected manifest record count for {setting}")
        result.append((setting, path, spec))
    return result


def analyze(root: Path, outdir: Path) -> dict[str, Any]:
    mpath = root / "manifest.json"
    raw_manifest = mpath.read_bytes()
    manifest = json.loads(raw_manifest.decode("utf-8"))
    inputs = inputs_from_manifest(root, manifest)

    # Key is (setting, realized world, carrier index, k, max family failures).
    # Value is (case count, sum S_domain, sum S_equal).
    sums: dict[tuple[str, str, int, int, int], list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])
    sw_counts: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"cases": 0, "k0": 0, "eligible": 0}
    )
    file_audit = []
    total_rows = eligible = k0_total = 0

    for setting, path, spec in inputs:
        print(f"Reading {setting}: {path.name}", file=sys.stderr)
        nrows = 0
        with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
            for lineno, line in enumerate(stream, start=1):
                if not line.strip():
                    raise ValueError(f"Blank row in {path}:{lineno}")
                row = json.loads(line)
                nrows += 1
                if row.get("setting") != setting:
                    raise ValueError(f"Setting mismatch in {path}:{lineno}")
                world = str(row.get("world"))
                if world not in {"W1", "W2", "W3"}:
                    raise ValueError(f"Unknown world label in {path}:{lineno}")
                fvec, evec = row.get("F"), row.get("E")
                if not isinstance(fvec, list) or len(fvec) != 6:
                    raise ValueError(f"Invalid F vector in {path}:{lineno}")
                if not isinstance(evec, list) or len(evec) != 6:
                    raise ValueError(f"Invalid E vector in {path}:{lineno}")
                if any(type(v) is not int or v < 0 or v > 5 for v in fvec):
                    raise ValueError(f"Invalid F value in {path}:{lineno}")
                if any(type(v) is not int or v < 0 or v > EVAL_SIZES[i] for i, v in enumerate(evec)):
                    raise ValueError(f"Invalid E value in {path}:{lineno}")
                k = row.get("k")
                if type(k) is not int or k != sum(fvec) or k < 0:
                    raise ValueError(f"k != sum(F) in {path}:{lineno}")
                carrier = row.get("carrier")
                if type(carrier) is not int or carrier not in range(6):
                    raise ValueError(f"Invalid carrier family in {path}:{lineno}")
                sd = float(row["S_domain"])
                se = float(row["S_equal"])
                sd_expected = 1.0 - sum(evec) / N_EVAL
                se_expected = 1.0 - sum(v / cap for v, cap in zip(evec, EVAL_SIZES)) / 6.0
                if not math.isfinite(sd) or abs(sd - sd_expected) > TOL:
                    raise ValueError(f"S_domain check failed in {path}:{lineno}")
                if not math.isfinite(se) or abs(se - se_expected) > TOL:
                    raise ValueError(f"S_equal check failed in {path}:{lineno}")

                sw = sw_counts[(setting, world)]
                sw["cases"] += 1
                if k == 0:
                    sw["k0"] += 1
                    k0_total += 1
                    if row.get("C") is not None:
                        raise ValueError(f"C must be undefined at k=0 in {path}:{lineno}")
                    continue

                eligible += 1
                sw["eligible"] += 1
                max_f = max(fvec)
                c = row.get("C")
                if c is None or abs(float(c) - max_f / k) > TOL:
                    raise ValueError(f"C != max(F)/k in {path}:{lineno}")
                key = (setting, world, carrier, k, max_f)
                agg = sums[key]
                agg[0] += 1
                agg[1] += sd
                agg[2] += se

        if nrows != int(spec["records"]):
            raise ValueError(f"Record count mismatch for {setting}: {nrows}")
        final_hash = sha256(path)
        if final_hash.lower() != str(spec["sha256"]).lower():
            raise ValueError(f"SHA-256 changed while reading {path}")
        file_audit.append({
            "setting": setting, "path": str(path), "records": nrows,
            "bytes": path.stat().st_size, "sha256": final_hash,
            "manifest_sha256": str(spec["sha256"]),
        })
        total_rows += nrows

    strata_levels: dict[tuple[str, str, int, int], list[tuple[int, list[float]]]] = defaultdict(list)
    for (setting, world, carrier, k, max_f), agg in sums.items():
        strata_levels[(setting, world, carrier, k)].append((max_f, agg))
    for v in strata_levels.values():
        v.sort(key=lambda pair: pair[0])

    strata, levels = [], []
    for (setting, world, carrier, k), vals in sorted(strata_levels.items()):
        n_total = int(sum(agg[0] for _, agg in vals))
        low_f, low = vals[0]
        high_f, high = vals[-1]
        has_contrast = len(vals) > 1
        low_n, high_n = int(low[0]), int(high[0])
        strata.append({
            "setting": setting, "world": world, "carrier_family": carrier + 1, "k": k,
            "n_cases": n_total, "n_distinct_C": len(vals), "has_within_stratum_contrast": has_contrast,
            "low_C": f"{low_f}/{k}", "low_C_n": low_n,
            "high_C": f"{high_f}/{k}", "high_C_n": high_n,
            "delta_S_domain_highC_minus_lowC": (high[1] / high_n - low[1] / low_n) if has_contrast else None,
            "delta_S_equal_highC_minus_lowC": (high[2] / high_n - low[2] / low_n) if has_contrast else None,
        })
        for max_f, agg in vals:
            n = int(agg[0])
            levels.append({
                "setting": setting, "world": world, "carrier_family": carrier + 1, "k": k,
                "C": f"{max_f}/{k}", "C_numerator": max_f, "C_denominator": k,
                "n_cases": n, "mean_S_domain": agg[1] / n, "mean_S_equal": agg[2] / n,
            })

    summaries = []
    for (setting, world), counts in sorted(sw_counts.items()):
        local_strata = [x for x in strata if x["setting"] == setting and x["world"] == world]
        usable = [x for x in local_strata if x["has_within_stratum_contrast"]]
        cases_in_usable = sum(x["n_cases"] for x in usable)
        summaries.append({
            "setting": setting, "world": world, **counts,
            "carrier_k_strata": len(local_strata),
            "strata_with_multiple_C": len(usable),
            "eligible_cases_in_usable_strata": cases_in_usable,
            "fraction_eligible_in_usable_strata": cases_in_usable / counts["eligible"] if counts["eligible"] else None,
        })

    return {
        "analysis": "descriptive fixed-k, within-carrier score contrasts using saved records",
        "scientific_disposition": "W1 FAILED unchanged; no model fitting or inference",
        "manifest_sha256": hashlib.sha256(raw_manifest).hexdigest(),
        "input_files_verified": file_audit,
        "total_records": total_rows, "eligible_k_positive": eligible, "k_zero": k0_total,
        "carrier_k_strata": len(strata),
        "carrier_k_strata_with_multiple_C": sum(x["has_within_stratum_contrast"] for x in strata),
        "summary_by_setting_world": summaries, "strata": strata, "C_level_means": levels,
    }


def render(result: dict[str, Any]) -> str:
    out = [
        "# Saved-record-only fixed-k, within-carrier C contrasts", "",
        "**Descriptive overlap audit only. The frozen W1 result remains FAILED.**",
        "The script verified the existing archives against manifest hashes and record counts.",
        "No cases were generated, no models were fitted, no hypothesis was tested, and no prior file was changed.", "",
        f"- Manifest SHA-256: {result['manifest_sha256']}",
        f"- Records read: {result['total_records']:,}",
        f"- Eligible cases (k > 0): {result['eligible_k_positive']:,}",
        f"- Cases with k = 0: {result['k_zero']:,}",
        f"- Carrier-family-by-k strata: {result['carrier_k_strata']:,}",
        f"- Strata with at least two C levels: {result['carrier_k_strata_with_multiple_C']:,}", "",
        "## Summary by setting and realized world", "",
        "| Setting | World | Cases | k=0 | Eligible | Carrier-k strata | Multiple-C strata | Eligible cases in multiple-C strata | Fraction |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for x in result["summary_by_setting_world"]:
        frac = "n/a" if x["fraction_eligible_in_usable_strata"] is None else f"{x['fraction_eligible_in_usable_strata']:.4f}"
        out.append(
            f"| {x['setting']} | {x['world']} | {x['cases']:,} | {x['k0']:,} | {x['eligible']:,} "
            f"| {x['carrier_k_strata']:,} | {x['strata_with_multiple_C']:,} "
            f"| {x['eligible_cases_in_usable_strata']:,} | {frac} |"
        )
    out += [
        "", "## Stratum-specific score contrasts", "",
        "A stratum is setting × realized world × anchor/carrier family × fixed k. The contrast is",
        "the unadjusted mean score at the highest observed C minus the mean score at the lowest",
        "observed C within that same stratum. It is descriptive, not adjusted, causal, or inferential.",
        "A stratum with one C value has no identifiable within-stratum contrast.", "",
        "| Setting | World | Carrier | k | Cases | Distinct C | Low C (n) | High C (n) | Delta S domain | Delta S equal |",
        "|---|---|---:|---:|---:|---:|---|---|---:|---:|",
    ]
    for x in result["strata"]:
        out.append(
            f"| {x['setting']} | {x['world']} | {x['carrier_family']} | {x['k']} | {x['n_cases']:,} "
            f"| {x['n_distinct_C']} | {x['low_C']} ({x['low_C_n']:,}) | {x['high_C']} ({x['high_C_n']:,}) "
            f"| {fmt(x['delta_S_domain_highC_minus_lowC'])} | {fmt(x['delta_S_equal_highC_minus_lowC'])} |"
        )
    out += [
        "", "## Counts and mean scores for each C level", "",
        "C is reported as the exact fraction max(F)/k. Counts are pooled over the 500 trials;",
        "they are synthetic counts, not natural-solver prevalence estimates.", "",
        "| Setting | World | Carrier | k | C | Cases | Mean S domain | Mean S equal |",
        "|---|---|---:|---:|---|---:|---:|---:|",
    ]
    for x in result["C_level_means"]:
        out.append(
            f"| {x['setting']} | {x['world']} | {x['carrier_family']} | {x['k']} | {x['C']} "
            f"| {x['n_cases']:,} | {fmt(x['mean_S_domain'])} | {fmt(x['mean_S_equal'])} |"
        )
    out += [
        "", "## Limits", "",
        "- No p-values, confidence intervals, model fits, or inferential conclusions are produced.",
        "- Mixture rows are separated by the realized world label.",
        "- W2 should have C=1 throughout its eligible strata and therefore no within-stratum C contrast.",
        "- Descriptive contrasts cannot rescue W1; the frozen W1 disposition remains FAILED.",
        "- The original archives, manifest, design, report, and amendments are read-only inputs.", "",
        "## Input integrity", "",
        "| Setting | Records | Bytes | SHA-256 |", "|---|---:|---:|---|",
    ]
    for x in result["input_files_verified"]:
        out.append(f"| {x['setting']} | {x['records']:,} | {x['bytes']:,} | {x['sha256']} |")
    out += [
        "", "## Reproduction", "",
        "Run from the repository root using the pinned interpreter:", "",
        "    py -V:Astral/CPython3.14.0 engineered-study/math/analyze_stratum_specific_contrasts.py",
        "",
        "The script writes only new Markdown and JSON files under",
        "engineered-study/math/results/three_world/stratum_specific_analysis/.", "",
    ]
    return "\n".join(out)


def main() -> int:
    root_default = Path(__file__).resolve().parent / "results" / "three_world"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=root_default)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    outdir = (args.output_dir or root / "stratum_specific_analysis").resolve()
    if outdir == root or root not in outdir.parents:
        raise SystemExit("Output directory must be a new subdirectory of the saved archive root.")
    try:
        report_path = outdir / "STRATUM_SPECIFIC_CONTRASTS_2026-10-24.md"
        json_path = outdir / "stratum_specific_contrasts_2026-10-24.json"
        if report_path.exists() or json_path.exists():
            raise FileExistsError("Output already exists; refusing to overwrite existing analysis results.")
        result = analyze(root, outdir)
        write_atomic(report_path, render(result))
        write_atomic(json_path, json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Saved records verified and analyzed: {result['total_records']:,}")
    print(f"Carrier-k strata with multiple C values: {result['carrier_k_strata_with_multiple_C']:,}")
    print("W1 disposition unchanged: FAILED; descriptive audit only.")
    print(f"Output directory: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
