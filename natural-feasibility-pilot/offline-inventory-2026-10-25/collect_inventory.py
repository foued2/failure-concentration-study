"""Read-only offline inventory for natural/background solver records.

This script never imports, compiles, or executes solver code. It only reads
retained JSON/text artifacts, hashes input files, and tabulates eligibility.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HEADER_RE = re.compile(r'^"""Submission (\d{3}) \(base body (\d+), replica (\d+)\)\."""\n\n')

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_hashes(paths: list[Path]) -> list[dict]:
    rows = []
    for p in paths:
        if p.exists():
            rows.append({"path": p.relative_to(ROOT).as_posix(), "sha256": sha256(p), "bytes": p.stat().st_size})
        else:
            rows.append({"path": p.relative_to(ROOT).as_posix(), "sha256": None, "bytes": None, "missing": True})
    return rows


def norm_c(k: int, c) -> float | None:
    """C is undefined at k=0; historical zero is a stored sentinel, not concentration."""
    return None if k == 0 else float(c)


def pack_summary(pack_dir: Path) -> dict:
    files = sorted(pack_dir.glob("solver_*.py"))
    body_sha_by_file = {}
    base_by_file = {}
    for p in files:
        norm = p.read_text(encoding="utf-8").replace("\r\n", "\n")
        m = HEADER_RE.match(norm)
        body = norm[m.end():] if m else norm
        body_sha_by_file[p.name] = hashlib.sha256(body.encode()).hexdigest()
        base_by_file[p.name] = int(m.group(2)) if m else None
    groups = defaultdict(list)
    for name, digest in body_sha_by_file.items():
        groups[digest].append(name)
    bases = defaultdict(set)
    for name, base in base_by_file.items():
        if base is not None:
            bases[base].add(body_sha_by_file[name])
    aggregate = hashlib.sha256()
    for name in sorted(body_sha_by_file):
        aggregate.update(f"{body_sha_by_file[name]}  {name}\n".encode())
    return {
        "files": len(files),
        "unique_bodies_after_header_strip": len(groups),
        "base_bodies_in_header": len(bases),
        "body_sha256_by_file": body_sha_by_file,
        "replica_groups": {d: names for d, names in sorted(groups.items()) if len(names) > 1},
        "replica_files_beyond_first": sum(len(names) - 1 for names in groups.values()),
        "aggregate_sha256_of_sorted_sha256_lines": aggregate.hexdigest(),
    }


def contrast_from_cells(cells: list[dict]) -> dict:
    """Derive fixed-k, different-C contrasts from eligible cell counts.

    A body pair qualifies only when both bodies are eligible at the same k>1
    but have different C. Level pairs count the distinct C comparisons; body
    pairs multiply the independent eligible bodies on each side.
    """
    by_k = defaultdict(lambda: defaultdict(int))
    for cell in cells:
        k = int(cell["k"])
        c = cell.get("C")
        n = int(cell.get("eligible_body_count") or 0)
        if k < 2 or c is None or n <= 0:
            continue
        by_k[k][float(c)] += n
    body_pairs = 0
    level_pairs = 0
    details = {}
    for k, counts in sorted(by_k.items()):
        levels = sorted(counts)
        lp = len(levels) * (len(levels) - 1) // 2
        bp = 0
        for i, c1 in enumerate(levels):
            for c2 in levels[i + 1:]:
                bp += counts[c1] * counts[c2]
        level_pairs += lp
        body_pairs += bp
        details[str(k)] = {
            "C_levels": levels,
            "eligible_bodies_by_C": {str(c): counts[c] for c in levels},
            "C_level_pairs": lp,
            "body_pairs": bp,
        }
    return {
        "same_k_different_C_pairs": body_pairs,
        "same_k_different_C_level_pairs": level_pairs,
        "by_k": details,
    }


def v01() -> dict:
    report = load_json(ROOT / "pilot" / "pilot_report.json")
    body_cells = defaultdict(set)
    row_cells = Counter()
    eligible_units = {}
    eligible_row_count = 0
    body_rows = defaultdict(list)
    for instance, data in report["instances"].items():
        for row in data["rows"]:
            k = int(row["k"])
            c = norm_c(k, row["C"])
            key = (k, c)
            row_cells[key] += 1
            body_cells[key].add(row["solver"])
            body_rows[row["solver"]].append((instance, k, c, row.get("Y"), row["eligible"]))
            if row["eligible"]:
                eligible_row_count += 1
                if k >= 2:
                    eligible_units[row["solver"]] = (k, c)
    cells = []
    for (k, c), bodies in sorted(body_cells.items(), key=lambda item: (item[0][0], -1 if item[0][1] is None else item[0][1])):
        elig = [b for b in bodies if b in eligible_units and eligible_units[b][0] >= 2]
        if k == 0:
            status = "ineligible_k_lt_2"
        elif len(elig) == len(bodies):
            status = "eligible"
        elif elig:
            status = "mixed"
        else:
            status = "ineligible"
        cells.append({
            "k": k,
            "C": c,
            "status": status,
            "body_instance_rows": row_cells[(k, c)],
            "distinct_bodies": len(bodies),
            "eligible_body_count": len(elig),
            "bodies": sorted(bodies),
        })
    per_k = defaultdict(set)
    for (k, c) in row_cells:
        if k >= 2 and c is not None:
            per_k[k].add(c)
    contrast = contrast_from_cells(cells)
    return {
        "id": "v0.1_mimo_sssp_pilot",
        "task": "SSSP",
        "generator": "opencode/mimo-v2.6-flash-free, 20 single-shot submissions, one session",
        "source": ["pilot/pilot_report.json", "pilot/PILOT_REPORT.md", "specs/generator_spec.json"],
        "records": sum(row_cells.values()),
        "unique_bodies": len(body_rows),
        "eligible_bodies_k_ge_2": len(eligible_units),
        "eligible_body_instance_rows": eligible_row_count,
        "k_values": sorted({k for k, _ in row_cells}),
        "distinct_C_levels_by_k": {str(k): sorted(v) for k, v in sorted(per_k.items())},
        "cells": cells,
        "contrast": contrast,
        "same_k_different_C_pairs": contrast["same_k_different_C_pairs"],
        "notes": "16/20 bodies had k=0 and are ineligible for a concentration contrast. Four multi-failure bodies occupy k=25(C=0.2), k=10(C=0.5), k=5(C=1), k=5(C=1); no fixed-k group has two C levels. C is undefined at k=0.",
    }


def v02() -> dict:
    report = load_json(ROOT / "v02" / "pilot_v02" / "pilot_v02_report.json")
    rows = []
    for instance, data in report["instances"].items():
        for row in data["rows"]:
            if row.get("eligible"):
                rows.append({"instance": instance, **row})
    cells = Counter()
    files_by_cell = defaultdict(set)
    base_by_file = {}
    for p in sorted((ROOT / "generation_v02" / "pack").glob("solver_*.py")):
        norm = p.read_text(encoding="utf-8").replace("\r\n", "\n")
        m = HEADER_RE.match(norm)
        base_by_file[p.stem] = int(m.group(2)) if m else None
    units = {}
    for r in rows:
        k = int(r["k"])
        c = norm_c(k, r["C"])
        base = base_by_file.get(r["solver"])
        cells[(k, c)] += 1
        files_by_cell[(k, c)].add(r["solver"])
        if base is not None:
            units[base] = (k, c)
    cell_rows = []
    for (k, c), n in sorted(cells.items()):
        base_count = len({base_by_file[name] for name in files_by_cell[(k, c)] if base_by_file.get(name) is not None})
        cell_rows.append({
            "k": k,
            "C": c,
            "status": "eligible",
            "body_instance_rows": n,
            "distinct_body_files": len(files_by_cell[(k, c)]),
            "distinct_base_bodies": base_count,
            "eligible_body_count": base_count,
        })
    per_k = defaultdict(set)
    for (k, c) in cells:
        if k >= 2 and c is not None:
            per_k[k].add(c)
    contrast = contrast_from_cells(cell_rows)
    pack = pack_summary(ROOT / "generation_v02" / "pack")
    return {
        "id": "v0.2_mimo_sssp_pack",
        "task": "SSSP",
        "generator": "frozen 120-file single-shot pack; 40 unique bodies, exactly 3 replicas each (per v0.2 audit)",
        "source": ["v02/pilot_v02/pilot_v02_report.json", "v02/FREEZE_V02.md", "v02/INTERPRETABILITY_AUDIT_2026-10-14.md", "generation_v02/pack/"],
        "pack": pack,
        "pilot_eligible_rows": len(rows),
        "pilot_distinct_body_files": len({r["solver"] for r in rows}),
        "pilot_distinct_base_bodies": len(units),
        "eligible_bodies_k_ge_2": len(units),
        "eligible_distinct_base_bodies": len(units),
        "confirmatory_eligible_pairs_reported": 1200,
        "confirmatory_per_row_persisted": False,
        "cells": cell_rows,
        "distinct_C_levels_by_k": {str(k): sorted(v) for k, v in sorted(per_k.items())},
        "contrast": contrast,
        "same_k_different_C_pairs": contrast["same_k_different_C_pairs"],
        "notes": "All 90 audited eligible rows satisfy C=5/k exactly; each k has one C level. Confirmatory rows were persisted only as aggregates. The 120 files are 40 base bodies x 3 replicas, so they are not 120 independent units.",
    }


def sssp_natural(run_id: str, dirname: str) -> dict:
    d = ROOT / "natural-feasibility-pilot" / dirname
    results = load_json(d / "PILOT_RESULTS.json")
    supports = results.get("summary", {}).get("support_by_k_C", {})
    cells = []
    for k_raw, c_map in supports.items():
        k = int(k_raw)
        for c_raw, data in c_map.items():
            c = norm_c(k, c_raw)
            n = int(data.get("distinct_bodies") or 0)
            cells.append({
                "k": k,
                "C": c,
                "status": "eligible" if k >= 2 else "ineligible_k_lt_2",
                "attempts": data.get("attempts"),
                "distinct_bodies": n,
                "eligible_body_count": n if k >= 2 else 0,
            })
    k_ge_2 = sum(c["eligible_body_count"] for c in cells)
    contrast = contrast_from_cells(cells)
    return {
        "id": run_id,
        "task": "SSSP",
        "generator": results.get("population"),
        "source": [f"natural-feasibility-pilot/{dirname}/PILOT_RESULTS.json", f"natural-feasibility-pilot/{dirname}/FEASIBILITY_REPORT.md"],
        "generation_requests": results.get("generation_requests"),
        "model_written_outputs": results.get("model_written_generation_attempts"),
        "generation_failures": results.get("generation_failures"),
        "distinct_canonical_bodies": results.get("distinct_canonical_bodies"),
        "eligible_executed_bodies": results.get("summary", {}).get("eligible_executed_bodies"),
        "eligible_bodies_k_ge_2": k_ge_2,
        "state": results.get("state"),
        "cells": cells,
        "contrast": contrast,
        "same_k_different_C_pairs": contrast["same_k_different_C_pairs"],
        "notes": "All completed bodies have k=0, so C is undefined and no k>=2 support exists.",
    }


def expression() -> dict:
    d = ROOT / "next-task" / "expression-pilot-gemini-20261022T163536Z"
    results = load_json(d / "PILOT_RESULTS.json")
    bodies = {}
    for attempt_dir in sorted((d / "attempts").iterdir()):
        if not attempt_dir.is_dir():
            continue
        diag_path = attempt_dir / "host-authoritative" / "diagnostic.json"
        if not diag_path.exists():
            continue
        screen_path = attempt_dir / "source-screen.json"
        screen = load_json(screen_path) if screen_path.exists() else {}
        diag = load_json(diag_path)
        eval_path = attempt_dir / "host-authoritative" / "evaluation.json"
        evaluation = load_json(eval_path) if eval_path.exists() else {}
        body_id = screen.get("body_id") or attempt_dir.name
        k = int(diag["k"])
        c = norm_c(k, diag["C"])
        diag_crash = int(diag.get("status_counts", {}).get("crash", 0))
        eval_crash = sum(1 for row in evaluation.get("probe_rows", []) if row.get("status") == "crash")
        if body_id not in bodies:
            bodies[body_id] = {
                "body_id": body_id,
                "k": k,
                "C": c,
                "attempts": [],
                "diag_crash": diag_crash,
                "eval_crash": eval_crash,
            }
        bodies[body_id]["attempts"].append(attempt_dir.name)
    grouped = defaultdict(list)
    for body in bodies.values():
        grouped[(body["k"], body["C"])].append(body)
    cells = []
    excluded_crashed = []
    for (k, c), group in sorted(grouped.items(), key=lambda item: (item[0][0], -1 if item[0][1] is None else item[0][1])):
        eligible = [b for b in group if b["diag_crash"] == 0 and b["eval_crash"] == 0]
        if k == 0:
            status = "ineligible_k_lt_2"
        elif eligible:
            status = "eligible"
        else:
            status = "excluded_crash"
        cells.append({
            "k": k,
            "C": c,
            "status": status,
            "attempts": len(group),
            "distinct_bodies": len(group),
            "eligible_body_count": len(eligible) if k >= 2 else 0,
        })
        for body in group:
            if k >= 2 and (body["diag_crash"] or body["eval_crash"]):
                excluded_crashed.append({
                    "body_id": body["body_id"],
                    "k": k,
                    "C": c,
                    "diag_crash": body["diag_crash"],
                    "eval_crash": body["eval_crash"],
                })
    contrast = contrast_from_cells(cells)
    protocol_eligible = [b for b in bodies.values() if b["diag_crash"] == 0 and b["eval_crash"] == 0]
    return {
        "id": "gemini_expression_30",
        "task": "bounded integer expression",
        "generator": "Google Gemini API / gemini-3.5-flash-lite, 30 slots",
        "source": [f"next-task/{d.name}/PILOT_RESULTS.json", f"next-task/{d.name}/FEASIBILITY_REPORT.md", "next-task/07_EXPRESSION_PILOT_AUDIT_2026-10-22.md"],
        "generation_requests": results.get("generation_requests"),
        "model_written_outputs": results.get("model_written_generation_attempts"),
        "generation_failures": results.get("generation_failures"),
        "source_rejected": results.get("source_rejected"),
        "duplicates": results.get("duplicates"),
        "distinct_canonical_bodies": results.get("distinct_canonical_bodies"),
        "pilot_reported_eligible_bodies": results.get("eligible_executed_bodies"),
        "protocol_eligible_bodies": len(protocol_eligible),
        "eligible_bodies_k_ge_2": sum(1 for b in protocol_eligible if b["k"] >= 2),
        "eligible_executed_bodies": results.get("eligible_executed_bodies"),
        "state": results.get("state"),
        "crash_policy": "Any crash in the diagnostic or evaluation suite makes a body ineligible under the frozen protocol; crashes are counted separately from diagnostic failures.",
        "cells": cells,
        "excluded_crashed_bodies": excluded_crashed,
        "contrast": contrast,
        "same_k_different_C_pairs": contrast["same_k_different_C_pairs"],
        "notes": "All 13 bodies with k>=2 crash and are excluded. The six k=0 bodies are valid but cannot support a concentration contrast. The nine k=2 bodies each crash on two diagnostic and two evaluation inputs; the singleton k=7 body has seven crashes each; the three k=30 bodies crash on all 30 diagnostic and evaluation inputs.",
    }


def main() -> None:
    data = {
        "audit_date": "2026-10-25",
        "protocol": "engineered-study/math/15_NATURAL_SOLVER_FEASIBILITY_PROTOCOL_2026-10-24.md",
        "mode": "offline inventory only; no solver or model execution",
        "disposition": "INFEASIBLE_WITH_CURRENT_DATA",
        "disposition_basis": "Zero eligible same-k, different-C body pairs with independent lineage in every audited dataset.",
        "outcome_limitation": "Historical evaluation outcomes already existed and were visible to this audit; it is not a blind inventory. Eligibility uses artifact validity, crash status, lineage, and the presence of an evaluation record, not score magnitudes. No C-S association is fitted or reported here.",
        "datasets": [],
        "excluded_categories": [
            {"category": "engineered-study controls", "reason": "constructed controls, not independently generated natural solver bodies"},
            {"category": "three-world simulation", "reason": "synthetic mathematical simulation, not solver records"},
            {"category": "followup 1-request run", "reason": "0 generated bodies"},
            {"category": "expression syntax rejects", "reason": "2 invalid artifacts, not executable bodies"},
        ],
        "input_hashes": [],
    }
    data["datasets"] = [
        v01(),
        v02(),
        sssp_natural("codex_sssp_100", "natural-pilot-20261021T123319Z"),
        sssp_natural("gemini_sssp_100", "natural-pilot-gemini-20261021T172103Z"),
        expression(),
    ]

    hash_paths = [
        ROOT / "engineered-study" / "math" / "15_NATURAL_SOLVER_FEASIBILITY_PROTOCOL_2026-10-24.md",
        ROOT / "pilot" / "PILOT_REPORT.md",
        ROOT / "pilot" / "pilot_report.json",
        ROOT / "specs" / "generator_spec.json",
        ROOT / "specs" / "instrument_spec.json",
        ROOT / "study" / "families.py",
        ROOT / "study" / "probes.py",
        ROOT / "study" / "instances.py",
        ROOT / "study" / "sssp.py",
        ROOT / "v02" / "FREEZE_V02.md",
        ROOT / "v02" / "PROTOCOL_V02.md",
        ROOT / "v02" / "spec_v02.json",
        ROOT / "v02" / "freeze_v02.py",
        ROOT / "v02" / "pilot_v02" / "pilot_v02_report.json",
        ROOT / "v02" / "INTERPRETABILITY_AUDIT_2026-10-14.md",
        ROOT / "v02" / "confirmatory_v02" / "confirmatory_v02_report.json",
        ROOT / "v02" / "generate_pack.py",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-20261021T123319Z" / "PILOT_RESULTS.json",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-20261021T123319Z" / "FEASIBILITY_REPORT.md",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-20261021T123319Z" / "attempts.json",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-20261021T123319Z" / "protocol.json",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-gemini-20261021T172103Z" / "PILOT_RESULTS.json",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-gemini-20261021T172103Z" / "FEASIBILITY_REPORT.md",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-gemini-20261021T172103Z" / "attempts.json",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-gemini-20261021T172103Z" / "INTEGRITY.json",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-gemini-20261021T172103Z" / "CLOSURE_VALIDATION.json",
        ROOT / "natural-feasibility-pilot" / "natural-pilot-gemini-20261021T172103Z" / "protocol.json",
        ROOT / "next-task" / "build_expression_banks.py",
        ROOT / "next-task" / "freeze_expression_banks.py",
        ROOT / "next-task" / "banks" / "BUILD_MANIFEST.json",
        ROOT / "next-task" / "expression-pilot-gemini-20261022T163536Z" / "PILOT_RESULTS.json",
        ROOT / "next-task" / "expression-pilot-gemini-20261022T163536Z" / "FEASIBILITY_REPORT.md",
        ROOT / "next-task" / "expression-pilot-gemini-20261022T163536Z" / "PROTOCOL.json",
        ROOT / "next-task" / "expression-pilot-gemini-20261022T163536Z" / "attempts.json",
        ROOT / "next-task" / "banks" / "diagnostic.json",
        ROOT / "next-task" / "banks" / "evaluation.json",
        ROOT / "next-task" / "06_EXPRESSION_PILOT_RESULT_2026-10-22.md",
        ROOT / "next-task" / "07_EXPRESSION_PILOT_AUDIT_2026-10-22.md",
    ]
    data["input_hashes"] = file_hashes(hash_paths)
    data["pack_hashes"] = {
        "v0.1": pack_summary(ROOT / "generation" / "pilot_pack"),
        "v0.2": pack_summary(ROOT / "generation_v02" / "pack"),
    }

    (OUT / "inventory_data.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    with (OUT / "inventory_table.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "dataset", "task", "k", "C", "status", "units_or_rows",
            "distinct_body_files_or_bodies", "distinct_base_bodies",
            "eligible_bodies_in_cell", "eligible_k_ge_2",
            "same_k_different_C_pairs", "note",
        ])
        for ds in data["datasets"]:
            for cell in ds["cells"]:
                w.writerow([
                    ds["id"], ds["task"], cell["k"],
                    "" if cell.get("C") is None else cell["C"],
                    cell.get("status", ""),
                    cell.get("body_instance_rows", cell.get("attempts")),
                    cell.get("distinct_bodies", cell.get("distinct_body_files")),
                    cell.get("distinct_base_bodies", ""),
                    cell.get("eligible_body_count", ""),
                    ds.get("eligible_bodies_k_ge_2"),
                    ds.get("same_k_different_C_pairs"),
                    ds.get("notes", ""),
                ])

    print(json.dumps({
        "disposition": data["disposition"],
        "datasets": [
            {
                "id": ds["id"],
                "eligible_k_ge_2": ds.get("eligible_bodies_k_ge_2"),
                "same_k_different_C_pairs": ds.get("same_k_different_C_pairs"),
                "cells": ds["cells"],
            }
            for ds in data["datasets"]
        ],
        "v02_pack_unique_bodies": data["pack_hashes"]["v0.2"]["unique_bodies_after_header_strip"],
    }, indent=2))


if __name__ == "__main__":
    main()
