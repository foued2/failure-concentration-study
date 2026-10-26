from __future__ import annotations

import ast
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import instrument

ROOT = Path(__file__).resolve().parent
GEN = ROOT / "generated"
BODIES = GEN / "bodies"
RESULTS = ROOT / "results"
WORKER = ROOT / "probe_worker.py"

FORBIDDEN_IMPORTS = {
    "os",
    "subprocess",
    "socket",
    "pathlib",
    "shutil",
    "importlib",
    "ctypes",
    "multiprocessing",
    "threading",
    "requests",
    "urllib",
    "http",
    "ftplib",
    "telnetlib",
    "pickle",
    "marshal",
}
FORBIDDEN_CALLS = {
    "open",
    "eval",
    "exec",
    "compile",
    "__import__",
    "input",
    "breakpoint",
}


def unsafe_reason(source: str) -> str | None:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return f"syntax:{exc.msg}"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                    return f"import:{alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                return f"from:{node.module}"
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_CALLS:
                return f"call:{node.func.id}"
    return None


def base_label(source: str) -> str:
    s = source.lower()
    if "heapq" in s or "heappush" in s or "heappop" in s:
        return "heap_dijkstra"
    if "floyd" in s or re.search(r"(?m)^\s*dist\s*=\s*\[\[", source):
        return "floyd"
    if "bellman" in s or ("range(n - 1)" in s and "for u, v, w in edges" in s):
        return "bellman_ford"
    if "deque" in s or "collections" in s:
        return "bfs"
    if "def dfs" in s or "def walk" in s or "def visit" in s:
        return "dfs_bruteforce"
    return "other"


def body_meta() -> dict[str, list[dict]]:
    meta: dict[str, list[dict]] = {}
    path = GEN / "attempts.jsonl"
    if not path.exists():
        return meta
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        for h in rec.get("body_hashes", []):
            meta.setdefault(h, []).append(
                {"model": rec.get("model"), "prompt_variant": rec.get("prompt_variant"), "batch_id": rec.get("batch_id")}
            )
    return meta


def evaluate_body(path: Path, meta: dict[str, list[dict]]) -> dict:
    source = path.read_text(encoding="utf-8")
    h = path.stem
    label = base_label(source)
    reason = unsafe_reason(source)
    row = {
        "body_hash": h,
        "base_algorithm": label,
        "source_chars": len(source),
        "excluded": None,
        "timeout": False,
        "fails": None,
        "generator_labels": meta.get(h, []),
    }
    if reason:
        row["excluded"] = reason
        return row
    try:
        proc = subprocess.run(
            [sys.executable, "-I", str(WORKER), str(path)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=5,
            encoding="utf-8",
            errors="replace",
        )
        raw = proc.stdout.strip().splitlines()
        data = json.loads(raw[-1])
        row["fails"] = data["fails"]
        row["load_error"] = data.get("load_error")
    except subprocess.TimeoutExpired:
        row["timeout"] = True
        row["fails"] = [True] * 30
        row["load_error"] = "timeout"
    except Exception as exc:
        row["fails"] = [True] * 30
        row["load_error"] = f"{type(exc).__name__}: {exc}"
    counts = instrument.family_counts(row["fails"])
    k, c = instrument.concentration(row["fails"])
    row.update(family_counts=counts, k=k, C=c, max_f=max(counts.values()))
    row["eligible"] = 2 <= k <= 24
    return row


def build() -> dict:
    meta = body_meta()
    rows = [evaluate_body(p, meta) for p in sorted(BODIES.glob("*.py"))]
    all_rows = [r for r in rows if r["excluded"] is None]
    eligible = [r for r in all_rows if r["eligible"]]
    cells = defaultdict(lambda: defaultdict(list))
    for r in eligible:
        cells[(r["base_algorithm"], r["k"])][r["C"]].append(r)
    cell_table = []
    supported = []
    for (label, k), levels in sorted(cells.items(), key=lambda x: (x[0][0], x[0][1])):
        level_rows = []
        ok = len(levels) >= 2
        for c in sorted(levels):
            groups = levels[c]
            level_rows.append(
                {
                    "C": c,
                    "groups": len(groups),
                    "generators": dict(
                        Counter(
                            item["model"]
                            for r in groups
                            for item in (r.get("generator_labels") or [{"model": "unknown"}])
                        )
                    ),
                }
            )
            if len(groups) < 4:
                ok = False
        entry = {
            "base_algorithm": label,
            "k": k,
            "levels": level_rows,
            "groups": sum(len(v) for v in levels.values()),
            "supported": ok,
        }
        cell_table.append(entry)
        if ok:
            supported.append(entry)
    unique_groups = set()
    cross_pairs = 0
    for entry in supported:
        label, k = entry["base_algorithm"], entry["k"]
        level_groups = [[r["body_hash"] for r in rows_] for rows_ in cells[(label, k)].values()]
        for group in level_groups:
            unique_groups.update(group)
        n = sum(len(g) for g in level_groups)
        same = sum(math.comb(len(g), 2) for g in level_groups)
        cross_pairs += math.comb(n, 2) - same
    all_or_none = (
        sum(1 for r in all_rows for v in r["family_counts"].values() if v in (0, 5))
        / (6 * len(all_rows))
        if all_rows
        else 1.0
    )
    distinct_k = sorted({e["k"] for e in supported})
    if all_or_none > 0.80:
        verdict = "FAIL"
        reason = "degeneracy"
    elif len(supported) >= 3 and len(distinct_k) >= 2 and len(unique_groups) >= 40:
        verdict = "PASS"
        reason = "thresholds_met"
    elif 1 <= len(supported) <= 2:
        verdict = "WEAK"
        reason = "one_or_two_supported_cells"
    else:
        verdict = "FAIL"
        reason = "insufficient_support"
    report = {
        "verdict": verdict,
        "reason": reason,
        "candidate_bodies": len(rows),
        "excluded_bodies": len(rows) - len(all_rows),
        "eligible_bodies": len(eligible),
        "target_rejected_bodies": 150,
        "target_reached": len(eligible) >= 150,
        "k_distribution": dict(sorted(Counter(r["k"] for r in all_rows).items())),
        "max_f_distribution": dict(sorted(Counter(r["max_f"] for r in all_rows).items())),
        "all_or_none_fraction": all_or_none,
        "supported_cells": supported,
        "cell_table": cell_table,
        "supported_cell_count": len(supported),
        "distinct_supported_k": distinct_k,
        "unique_groups_in_supported_cells": len(unique_groups),
        "cross_group_pairs_different_C": cross_pairs,
        "base_algorithm_counts": dict(Counter(r["base_algorithm"] for r in all_rows)),
        "exclusion_reasons": dict(Counter(r["excluded"] for r in rows if r["excluded"])),
        "rows": rows,
    }
    return report


def markdown(report: dict) -> str:
    lines = [
        "# H3 Footprint Gate Result",
        "",
        f"**Verdict:** `{report['verdict']}` ({report['reason']})",
        "",
        f"- Candidate bodies: {report['candidate_bodies']}",
        f"- Eligible bodies (`2 <= k <= 24`): {report['eligible_bodies']}",
        f"- Target reached: {report['target_reached']}",
        f"- All-or-none fraction: {report['all_or_none_fraction']:.3f}",
        f"- Supported cells: {report['supported_cell_count']}",
        f"- Distinct supported `k`: {report['distinct_supported_k']}",
        f"- Unique groups in supported cells: {report['unique_groups_in_supported_cells']}",
        f"- Cross-group different-`C` pairs: {report['cross_group_pairs_different_C']}",
        "",
        "## Distribution",
        "",
        f"`k`: {report['k_distribution']}",
        "",
        f"`max_j f_j`: {report['max_f_distribution']}",
        "",
        "## Supported cells",
        "",
        "| base algorithm | k | C levels | groups |",
        "|---|---:|---|---:|",
    ]
    for e in report["supported_cells"]:
        levels = ", ".join(f"{x['C']:.4f} ({x['groups']})" for x in e["levels"])
        lines.append(f"| {e['base_algorithm']} | {e['k']} | {levels} | {e['groups']} |")
    if not report["supported_cells"]:
        lines.append("| none |  |  |  |")
    lines += [
        "",
        "A PASS would not establish predictive value or power. A FAIL is a finding about this instrument.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    report = build()
    (RESULTS / "footprint.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    (RESULTS / "REPORT.md").write_text(markdown(report), encoding="utf-8")
    print(markdown(report))


if __name__ == "__main__":
    main()
