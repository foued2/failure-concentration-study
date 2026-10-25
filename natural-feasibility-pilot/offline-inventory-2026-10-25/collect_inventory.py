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


def pack_summary(pack_dir: Path) -> dict:
    files = sorted(pack_dir.glob("solver_*.py"))
    per_file = {}
    base_by_file = {}
    for p in files:
        norm = p.read_text(encoding="utf-8").replace("\r\n", "\n")
        m = HEADER_RE.match(norm)
        body = norm[m.end():] if m else norm
        per_file[p.name] = hashlib.sha256(body.encode()).hexdigest()
        base_by_file[p.name] = int(m.group(2)) if m else None
    groups = defaultdict(list)
    for name, digest in per_file.items():
        groups[digest].append(name)
    bases = defaultdict(set)
    for name, base in base_by_file.items():
        if base is not None:
            bases[base].add(per_file[name])
    aggregate = hashlib.sha256()
    for name in sorted(per_file):
        aggregate.update(f"{per_file[name]}  {name}\n".encode())
    return {
        "files": len(files),
        "unique_bodies_after_header_strip": len(groups),
        "base_bodies_in_header": len(bases),
        "replica_groups": {d: names for d, names in sorted(groups.items()) if len(names) > 1},
        "replica_files_beyond_first": sum(len(names) - 1 for names in groups.values()),
        "aggregate_sha256_of_sorted_sha256_lines": aggregate.hexdigest(),
    }


def v01() -> dict:
    report = load_json(ROOT / "pilot" / "pilot_report.json")
    body_cells = defaultdict(set)
    row_cells = Counter()
    eligible_bodies = set()
    eligible_row_count = 0
    body_rows = defaultdict(list)
    for instance, data in report["instances"].items():
        for row in data["rows"]:
            key = (row["k"], row["C"])
            row_cells[key] += 1
            body_cells[key].add(row["solver"])
            body_rows[row["solver"]].append((instance, row["k"], row["C"], row.get("Y"), row["eligible"]))
            if row["eligible"]:
                eligible_bodies.add(row["solver"])
                eligible_row_count += 1
    k_values = sorted({k for k, _ in body_cells})
    cells = []
    for (k, c), bodies in sorted(body_cells.items()):
        cells.append({"k": k, "C": c, "body_instance_rows": row_cells[(k, c)], "distinct_bodies": len(bodies), "bodies": sorted(bodies)})
    per_k = defaultdict(list)
    for (k, c) in body_cells:
        per_k[k].append(c)
    return {
        "id": "v0.1_mimo_sssp_pilot",
        "task": "SSSP",
        "generator": "opencode/mimo-v2.6-flash-free, 20 single-shot submissions, one session",
        "source": ["pilot/pilot_report.json", "pilot/PILOT_REPORT.md", "specs/generator_spec.json"],
        "records": sum(row_cells.values()),
        "unique_bodies": len(body_rows),
        "eligible_bodies_k_ge_2": len(eligible_bodies),
        "eligible_body_instance_rows": eligible_row_count,
        "k_values": k_values,
        "distinct_C_levels_by_k": {str(k): sorted(set(per_k[k])) for k in sorted(per_k)},
        "cells": cells,
        "same_k_different_C_pairs": 0,
        "notes": "16/20 bodies had k=0 and are ineligible. Four multi-failure bodies occupy k=25(C=0.2), k=10(C=0.5), k=5(C=1), k=5(C=1); no fixed-k group has two C levels.",
    }


def v02() -> dict:
    report = load_json(ROOT / "v02" / "pilot_v02" / "pilot_v02_report.json")
    rows = []
    for instance, data in report["instances"].items():
        for row in data["rows"]:
            if row.get("eligible"):
                rows.append({"instance": instance, **row})
    cells = Counter((r["k"], r["C"]) for r in rows)
    bodies_by_cell = defaultdict(set)
    base_by_file = {}
    for p in sorted((ROOT / "generation_v02" / "pack").glob("solver_*.py")):
        norm = p.read_text(encoding="utf-8").replace("\r\n", "\n")
        m = HEADER_RE.match(norm)
        base_by_file[p.stem] = int(m.group(2)) if m else None
    for r in rows:
        bodies_by_cell[(r["k"], r["C"])].add(r["solver"])
    per_k = defaultdict(set)
    for (k, c) in cells:
        per_k[k].add(c)
    pack = pack_summary(ROOT / "generation_v02" / "pack")
    return {
        "id": "v0.2_mimo_sssp_pack",
        "task": "SSSP",
        "generator": "frozen 120-file single-shot pack; 40 unique bodies, exactly 3 replicas each (per v0.2 audit)",
        "source": ["v02/pilot_v02/pilot_v02_report.json", "v02/FREEZE_V02.md", "v02/INTERPRETABILITY_AUDIT_2026-10-14.md", "generation_v02/pack/"],
        "pack": pack,
        "pilot_eligible_rows": len(rows),
        "pilot_distinct_body_files": len({r['solver'] for r in rows}),
        "pilot_distinct_base_bodies": len({base_by_file[r['solver']] for r in rows}),
        "eligible_bodies_k_ge_2": len({base_by_file[r['solver']] for r in rows}),
        "confirmatory_eligible_pairs_reported": 1200,
        "confirmatory_per_row_persisted": False,
        "cells": [
            {
                "k": k,
                "C": c,
                "body_instance_rows": n,
                "distinct_body_files": len(bodies_by_cell[(k, c)]),
                "distinct_base_bodies": len({base_by_file[name] for name in bodies_by_cell[(k, c)]}),
            }
            for (k, c), n in sorted(cells.items())
        ],
        "distinct_C_levels_by_k": {str(k): sorted(v) for k, v in sorted(per_k.items())},
        "same_k_different_C_pairs": 0,
        "eligible_distinct_base_bodies": len({base_by_file[r['solver']] for r in rows}),
        "notes": "All 90 audited eligible rows satisfy C=5/k exactly; each k has one C level. Confirmatory rows were persisted only as aggregates. The 120 files are 40 base bodies x 3 replicas, so they are not 120 independent units.",
    }


def sssp_natural(run_id: str, dirname: str) -> dict:
    d = ROOT / "natural-feasibility-pilot" / dirname
    results = load_json(d / "PILOT_RESULTS.json")
    supports = results.get("summary", {}).get("support_by_k_C", {})
    cells = []
    for k, c_map in supports.items():
        for c, data in c_map.items():
            cells.append({
                "k": int(k), "C": float(c),
                "attempts": data.get("attempts"),
                "distinct_bodies": data.get("distinct_bodies"),
                "evaluation_correct_counts": data.get("evaluation_correct_counts"),
            })
    k_ge_2 = sum(c["distinct_bodies"] for c in cells if c["k"] >= 2)
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
        "same_k_different_C_pairs": 0,
        "notes": "All completed bodies have k=0, so C is undefined/zero and no k>=2 support exists.",
    }


def expression() -> dict:
    d = ROOT / "next-task" / "expression-pilot-gemini-20261022T163536Z"
    results = load_json(d / "PILOT_RESULTS.json")
    cells = []
    for k, c_map in results.get("support_by_k_C", {}).items():
        for c, data in c_map.items():
            cells.append({
                "k": int(k), "C": float(c),
                "attempts": data.get("attempts"),
                "distinct_bodies": data.get("distinct_bodies"),
                "evaluation_correct_counts": data.get("evaluation_correct_counts"),
            })
    k_ge_2 = sum(c["distinct_bodies"] for c in cells if c["k"] >= 2)
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
        "eligible_executed_bodies": results.get("eligible_executed_bodies"),
        "eligible_bodies_k_ge_2": k_ge_2,
        "state": results.get("state"),
        "cells": cells,
        "same_k_different_C_pairs": 0,
        "notes": "k=2 occurs with C=1 only (9 bodies); k=30 with C=1/6 only (3 bodies); k=7 is a singleton. The nine k=2 bodies share one whitespace bug; the three k=30 bodies are uniform crashes. No fixed-k C separation.",
    }


def main() -> None:
    data = {
        "audit_date": "2026-10-25",
        "protocol": "engineered-study/math/15_NATURAL_SOLVER_FEASIBILITY_PROTOCOL_2026-10-24.md",
        "mode": "offline inventory only; no solver or model execution",
        "disposition": "INFEASIBLE_WITH_CURRENT_DATA",
        "disposition_basis": "Zero eligible same-k, different-C body pairs with independent lineage in every audited dataset.",
        "datasets": [
            v01(),
            v02(),
            sssp_natural("codex_sssp_100", "natural-pilot-20261021T123319Z"),
            sssp_natural("gemini_sssp_100", "natural-pilot-gemini-20261021T172103Z"),
            expression(),
        ],
        "excluded_categories": [
            {"category": "engineered-study controls", "reason": "constructed controls, not independently generated natural solver bodies"},
            {"category": "three-world simulation", "reason": "synthetic mathematical simulation, not solver records"},
            {"category": "followup 1-request run", "reason": "0 generated bodies"},
            {"category": "expression syntax rejects", "reason": "2 invalid artifacts, not executable bodies"},
        ],
        "input_hashes": [],
    }

    hash_paths = [
        ROOT / "engineered-study" / "math" / "15_NATURAL_SOLVER_FEASIBILITY_PROTOCOL_2026-10-24.md",
        ROOT / "pilot" / "PILOT_REPORT.md",
        ROOT / "pilot" / "pilot_report.json",
        ROOT / "specs" / "generator_spec.json",
        ROOT / "v02" / "FREEZE_V02.md",
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
        w.writerow(["dataset", "task", "k", "C", "units_or_rows", "distinct_body_files_or_bodies", "distinct_base_bodies", "eligible_k_ge_2", "same_k_different_C_pairs", "note"])
        for ds in data["datasets"]:
            for cell in ds["cells"]:
                w.writerow([
                    ds["id"], ds["task"], cell["k"], cell["C"],
                    cell.get("body_instance_rows", cell.get("attempts")),
                    cell.get("distinct_bodies", cell.get("distinct_body_files")),
                    cell.get("distinct_base_bodies", ""),
                    ds.get("eligible_bodies_k_ge_2"),
                    ds.get("same_k_different_C_pairs"),
                    ds.get("notes", ""),
                ])

    print(json.dumps({
        "disposition": data["disposition"],
        "datasets": [
            {
                "id": ds["id"],
                "cells": ds["cells"],
                "eligible_k_ge_2": ds.get("eligible_bodies_k_ge_2"),
            }
            for ds in data["datasets"]
        ],
        "v02_pack": data["pack_hashes"]["v0.2"],
        "v01_pack": data["pack_hashes"]["v0.1"],
    }, indent=2))


if __name__ == "__main__":
    main()
