from __future__ import annotations

import ast
import builtins
import hashlib
import json
import math
import os
import re
import subprocess
import symtable
import sys
from collections import Counter, defaultdict
from pathlib import Path

import instrument
import container_eval

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


def body_meta() -> dict[str, dict]:
    """Assign each distinct body to the first generation batch that emitted it."""
    meta: dict[str, dict] = {}
    path = GEN / "attempts.jsonl"
    if not path.exists():
        return meta
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        batch_id = rec.get("batch_id")
        group_id = f"batch-{batch_id:03d}" if batch_id is not None else None
        candidates = rec.get("candidate_records")
        if candidates is None:
            candidates = [{"body_hash": h} for h in rec.get("body_hashes", [])]
        for item in candidates:
            h = item.get("body_hash") if isinstance(item, dict) else item
            if h:
                meta.setdefault(h, {
                    "group_id": group_id or f"untracked:{h}",
                    "model": rec.get("model"),
                    "prompt_variant": rec.get("prompt_variant"),
                    "batch_id": batch_id,
                })
    return meta


def undefined_global_names(source: str) -> list[str]:
    """Conservative static warning for referenced globals never bound in source."""
    try:
        root = symtable.symtable(source, "<candidate>", "exec")
    except SyntaxError:
        return []
    module_bound = {
        symbol.get_name()
        for symbol in root.get_symbols()
        if symbol.is_assigned() or symbol.is_imported() or symbol.is_namespace()
    }
    runtime_names = {
        "__name__", "__package__", "__spec__", "__builtins__", "__doc__",
        "__loader__", "__file__", "__cached__", "__annotations__",
    }
    allowed = set(dir(builtins)) | runtime_names
    missing: set[str] = set()

    def visit(table) -> None:
        if table.get_type() != "module":
            for symbol in table.get_symbols():
                name = symbol.get_name()
                if symbol.is_referenced() and symbol.is_global() and name not in module_bound and name not in allowed:
                    missing.add(name)
        for child in table.get_children():
            visit(child)

    visit(root)
    return sorted(missing)


def _json_object_from_stdout(stdout: str) -> dict | None:
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def _invalid_candidate(row: dict, reason: str) -> dict:
    row.update({
        "excluded": reason, "load_error": reason, "fails": None,
        "family_counts": None, "k": None, "C": None, "max_f": None,
        "eligible": False, "probes_completed": 0,
    })
    return row


def evaluate_body(path: Path, meta: dict[str, dict]) -> dict:
    """Score one candidate while keeping its source and each probe inside Docker."""
    source = path.read_text(encoding="utf-8")
    h = path.stem
    info = meta.get(h) or {}
    row = {
        "body_hash": h, "base_algorithm": base_label(source),
        "source_chars": len(source), "excluded": None, "timeout": False,
        "fails": None, "k": None, "C": None,
        "group_id": info.get("group_id"), "generator": info.get("model"),
        "prompt_variant": info.get("prompt_variant"), "batch_id": info.get("batch_id"),
        "execution_backend": "docker-fresh-container-per-probe",
    }
    reason = unsafe_reason(source)
    if reason:
        return _invalid_candidate(row, reason)
    missing = undefined_global_names(source)
    if missing:
        return _invalid_candidate(row, "undefined_name:" + ",".join(missing))
    if row["group_id"] is None:
        return _invalid_candidate(row, "missing_provenance")

    try:
        pre = container_eval.preflight(path, timeout=5.0)
    except container_eval.ContainerInfrastructureError:
        # An unavailable Docker engine is an operational blocker, not evidence
        # that a candidate is invalid. Abort rather than turn an infra failure
        # into a scientific observation.
        raise
    if pre.get("status") != "preflight_ok":
        detail = pre.get("error") or pre.get("error_type") or pre.get("status") or "candidate did not load"
        return _invalid_candidate(row, "container_preflight:" + str(detail))

    expected_values = json.loads((ROOT / "expected_values.json").read_text(encoding="utf-8"))
    fails: list[bool] = []
    had_probe_timeout = False
    probe_summaries: list[dict] = []
    for probe_index, probe in enumerate(instrument.PROBES):
        try:
            result = container_eval.run_probe(path, probe, timeout=5.0)
        except container_eval.ContainerInfrastructureError:
            raise
        status = result.get("status")
        probe_summaries.append({
            "probe_index": probe_index,
            "probe_id": probe["probe_id"],
            "status": status,
            "timed_out": result.get("timed_out") is True,
            "elapsed_seconds": result.get("elapsed_seconds"),
            "exit_code": result.get("exit_code"),
            "image_id": (result.get("image") or {}).get("image_id"),
        })

        if status == "timed_out":
            # The prespecified rule treats a timeout during an individual probe
            # as that probe failing, but never lets the container persist.
            had_probe_timeout = True
            fails.append(True)
            continue
        if status == "runtime_error":
            fails.append(True)
            continue
        if status == "load_error":
            row["container_probe_summaries"] = probe_summaries
            return _invalid_candidate(
                row, "load_error_during_probe:" + str(result.get("error_type", "unknown"))
            )
        if status != "ok":
            row["container_probe_summaries"] = probe_summaries
            return _invalid_candidate(
                row, "container_probe_invalid_output:" + str(status)
            )

        answer_type = result.get("answer_type")
        answer = result.get("answer")
        expected = expected_values[probe["probe_id"]]
        fails.append(answer_type != "int" or type(answer) is not int or answer != expected)

    counts = instrument.family_counts(fails)
    k, c = instrument.concentration(fails)
    row.update({
        "excluded": None, "load_error": None, "fails": fails,
        "family_counts": counts, "timeout": had_probe_timeout,
        "k": k, "C": c, "max_f": max(counts.values()),
        "eligible": 2 <= k <= 24, "probes_completed": len(fails),
        "container_probe_summaries": probe_summaries,
        "container_image": container_eval.ensure_image(),
    })
    return row

def _all_or_none_fraction(rows: list[dict]) -> float | None:
    """Secondary metric retained from V1/V2: per-family-count all-or-none rate."""
    values = [v for row in rows for v in (row.get("family_counts") or {}).values()]
    return (sum(v in (0, 5) for v in values) / len(values)) if values else None


def _saturation_rate(rows: list[dict]) -> float | None:
    """Primary degeneracy metric: fraction of candidates with a fully failed family.

    A candidate is saturated when max_j f_j == 5. This is not confounded by low k:
    at k=2 a profile such as [2,0,0,0,0,0] is not saturated.
    """
    if not rows:
        return None
    return sum(1 for row in rows if row.get("max_f") == 5) / len(rows)


FUTILITY_CHECKPOINTS = {100: 10, 200: 20, 300: 30}
SATURATION_MAX = 0.80
HARD_CAP_BATCHES = 400


def _completed_batches() -> int:
    path = GEN / "attempts.jsonl"
    if not path.exists():
        return 0
    ids: set[int] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        batch_id = record.get("batch_id")
        if isinstance(batch_id, int):
            ids.add(batch_id)
    return len(ids)


def _futility(eligible: list[dict]) -> dict:
    """Predeclared stop rule evaluated at completed-batch checkpoints.

    At checkpoint c, count distinct eligible provenance groups from batches
    with batch_id < c. Trigger if that count is below the frozen minimum.
    """
    completed = _completed_batches()
    checkpoints = []
    first_triggered = None
    for batch, minimum in sorted(FUTILITY_CHECKPOINTS.items()):
        reached = completed >= batch
        groups_at = None
        triggered_here = False
        if reached:
            group_ids = {
                row["group_id"]
                for row in eligible
                if row.get("group_id") and isinstance(row.get("batch_id"), int) and row["batch_id"] < batch
            }
            groups_at = len(group_ids)
            triggered_here = groups_at < minimum
            if triggered_here and first_triggered is None:
                first_triggered = batch
        checkpoints.append({
            "batch": batch,
            "min_eligible_groups": minimum,
            "reached": reached,
            "eligible_groups_at_checkpoint": groups_at,
            "triggered_at_checkpoint": triggered_here,
        })
    return {
        "rule": "Stop if eligible provenance groups at batch 100/200/300 are below 10/20/30 (linear pace to the 40-group PASS target).",
        "completed_batches": completed,
        "hard_cap_batches": HARD_CAP_BATCHES,
        "checkpoints": checkpoints,
        "triggered": first_triggered is not None,
        "first_triggered_batch": first_triggered,
    }


EVALUATION_CACHE_NAME = "evaluated_rows.jsonl"
EVALUATION_CACHE_VERSION = 1


def evaluation_fingerprint() -> str:
    """Pin every trusted artifact that can change candidate labels or measurements."""
    base = Path(__file__).resolve().parent
    paths = (
        "run_gate.py",
        "container_eval.py",
        "container_eval.py",
        "container-image/Dockerfile",
        "container-image/sandbox_worker.py",
        "instrument.py",
        "expected_values.json",
    )
    digest = hashlib.sha256()
    digest.update(("cache-version=" + str(EVALUATION_CACHE_VERSION) + "\n").encode("utf-8"))
    digest.update(("python=" + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "\n").encode("utf-8"))
    for relative in paths:
        path = base / relative
        if not path.is_file():
            raise RuntimeError("Cannot fingerprint evaluation dependency: " + relative)
        payload = path.read_bytes().replace(b"\r\n", b"\n")
        digest.update(relative.encode("utf-8") + b"\0")
        digest.update(hashlib.sha256(payload).digest())
    return digest.hexdigest()


def load_evaluation_cache(path: Path, fingerprint: str) -> dict[str, dict]:
    """Load only cache entries produced by the identical pinned evaluator."""
    cache: dict[str, dict] = {}
    if not path.is_file():
        return cache
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            # Ignore a torn final append. It will be rewritten on the next run.
            continue
        if not isinstance(record, dict) or record.get("fingerprint") != fingerprint:
            continue
        body_hash = record.get("body_hash")
        row = record.get("row")
        source_sha256 = record.get("source_sha256")
        if (
            isinstance(body_hash, str)
            and isinstance(row, dict)
            and isinstance(source_sha256, str)
            and row.get("body_hash") == body_hash
        ):
            cache[body_hash] = {
                "source_sha256": source_sha256,
                "row": row,
            }
    return cache


def append_evaluation_cache(
    path: Path,
    fingerprint: str,
    source_path: Path,
    row: dict,
) -> None:
    """Durably append one measured row so an interrupted remote job can resume."""
    payload = source_path.read_bytes()
    record = {
        "cache_version": EVALUATION_CACHE_VERSION,
        "fingerprint": fingerprint,
        "body_hash": row["body_hash"],
        "source_sha256": hashlib.sha256(payload).hexdigest(),
        "row": row,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def build() -> dict:
    meta = body_meta()
    cache_path = ROOT / "results" / EVALUATION_CACHE_NAME
    fingerprint = evaluation_fingerprint()
    cached = load_evaluation_cache(cache_path, fingerprint)
    rows = []
    cache_hits = 0
    evaluated_now = 0
    for body_path in sorted(BODIES.glob("*.py")):
        body_bytes = body_path.read_bytes()
        source_sha256 = hashlib.sha256(body_bytes).hexdigest()
        candidate_hash = body_path.stem
        cached_row = cached.get(candidate_hash)
        if cached_row is not None and cached_row.get("source_sha256") == source_sha256:
            row = cached_row["row"]
            cache_hits += 1
        else:
            row = evaluate_body(body_path, meta)
            append_evaluation_cache(cache_path, fingerprint, body_path, row)
            cached[candidate_hash] = {
                "source_sha256": source_sha256,
                "row": row,
            }
            evaluated_now += 1
        rows.append(row)
    invalid_rows = [r for r in rows if r["excluded"] is not None]
    valid_rows = [r for r in rows if r["excluded"] is None and r.get("k") is not None]
    rejected = [r for r in valid_rows if r["k"] > 0]
    eligible = [r for r in valid_rows if 2 <= r["k"] <= 24]
    cells = defaultdict(lambda: defaultdict(list))
    for row in eligible:
        cells[(row["base_algorithm"], row["k"])][row["C"]].append(row)

    cell_table, supported = [], []
    for (label, k), levels in sorted(cells.items(), key=lambda item: (item[0][0], item[0][1])):
        level_rows, ok = [], len(levels) >= 2
        for c in sorted(levels):
            candidates = levels[c]
            group_ids = sorted({r["group_id"] for r in candidates if r.get("group_id")})
            level_rows.append({
                "C": c, "candidate_bodies": len(candidates), "groups": len(group_ids),
                "group_ids": group_ids,
                "generators": dict(Counter(r.get("generator") or "unknown" for r in candidates)),
            })
            if len(group_ids) < 4:
                ok = False
        all_groups = sorted({r["group_id"] for level in levels.values() for r in level if r.get("group_id")})
        entry = {
            "base_algorithm": label, "k": k, "levels": level_rows,
            "candidate_bodies": sum(len(level) for level in levels.values()),
            "groups": len(all_groups), "group_ids": all_groups, "supported": ok,
        }
        cell_table.append(entry)
        if ok:
            supported.append(entry)

    unique_groups = {gid for cell in supported for gid in cell["group_ids"]}
    group_pairs: set[tuple[str, int, str, str]] = set()
    for cell in supported:
        label, k = cell["base_algorithm"], cell["k"]
        group_to_c = defaultdict(set)
        for c, candidate_rows in cells[(label, k)].items():
            for row in candidate_rows:
                if row.get("group_id"):
                    group_to_c[row["group_id"]].add(c)
        gids = sorted(group_to_c)
        for i, group_a in enumerate(gids):
            for group_b in gids[i+1:]:
                if any(ca != cb for ca in group_to_c[group_a] for cb in group_to_c[group_b]):
                    group_pairs.add((label, k, group_a, group_b))

    aone_all = _all_or_none_fraction(valid_rows)
    aone_rejected = _all_or_none_fraction(rejected)
    aone_eligible = _all_or_none_fraction(eligible)
    sat_all = _saturation_rate(valid_rows)
    sat_rejected = _saturation_rate(rejected)
    sat_eligible = _saturation_rate(eligible)
    futility = _futility(eligible)
    distinct_k = sorted({cell["k"] for cell in supported})

    # Primary degeneracy rule: saturation among eligible candidates only. The
    # V1/V2 per-family all-or-none rate is retained for continuity but is not
    # used for the verdict because it is confounded at low k.
    if futility["triggered"]:
        verdict, reason = "FAIL", "futility_checkpoint_batch_%d" % futility["first_triggered_batch"]
    elif eligible and sat_eligible is not None and sat_eligible > SATURATION_MAX:
        verdict, reason = "FAIL", "degeneracy_saturation_among_eligible_k"
    elif len(supported) >= 3 and len(distinct_k) >= 2 and len(unique_groups) >= 40:
        verdict, reason = "PASS", "thresholds_met"
    elif 1 <= len(supported) <= 2:
        verdict, reason = "WEAK", "one_or_two_supported_cells"
    else:
        verdict, reason = "FAIL", "insufficient_support"

    return {
        "verdict": verdict, "reason": reason, "candidate_bodies": len(rows),
        "evaluation_cache": {
            "version": EVALUATION_CACHE_VERSION,
            "fingerprint": fingerprint,
            "cache_path": str(cache_path),
            "cache_hits": cache_hits,
            "evaluated_this_run": evaluated_now,
            "rows_available": len(rows),
        },
        "valid_bodies": len(valid_rows), "invalid_candidates": len(invalid_rows),
        "eligible_bodies": len(eligible),
        "eligible_groups": len({r["group_id"] for r in eligible if r.get("group_id")}),
        "rejected_bodies": len(rejected), "target_rejected_bodies": 150,
        "target_reached": len(rejected) >= 150,
        "k_distribution": dict(sorted(Counter(r["k"] for r in valid_rows).items())),
        "max_f_distribution": dict(sorted(Counter(r["max_f"] for r in valid_rows).items())),
        "saturation_rate_all_valid": sat_all,
        "saturation_rate_rejected": sat_rejected,
        "saturation_rate_eligible": sat_eligible,
        "saturation_max": SATURATION_MAX,
        "all_or_none_fraction_all_valid": aone_all,
        "all_or_none_fraction_rejected": aone_rejected,
        "all_or_none_fraction_eligible": aone_eligible,
        "futility": futility,
        "supported_cells": supported, "cell_table": cell_table,
        "supported_cell_count": len(supported), "distinct_supported_k": distinct_k,
        "unique_groups_in_supported_cells": len(unique_groups),
        "cross_group_pairs_different_C": len(group_pairs),
        "base_algorithm_counts": dict(Counter(r["base_algorithm"] for r in valid_rows)),
        "exclusion_reasons": dict(Counter(r["excluded"] for r in invalid_rows)),
        "rows": rows,
    }


def markdown(report: dict) -> str:
    lines = [
        "# H3 Footprint Gate Result", "",
        "Verdict: " + report["verdict"] + " (" + report["reason"] + ")", "",
        "- Candidate bodies: " + str(report["candidate_bodies"]),
        "- Valid candidates: " + str(report["valid_bodies"]),
        "- Invalid candidates (not assigned k): " + str(report["invalid_candidates"]),
        "- B1-rejected valid candidates: " + str(report["rejected_bodies"]),
        "- Eligible bodies (2 <= k <= 24): " + str(report["eligible_bodies"]),
        "- Eligible provenance groups: " + str(report["eligible_groups"]),
        "- Target of 150 rejected bodies reached: " + str(report["target_reached"]),
        "- Saturation rate (max_j f_j = 5) among all valid candidates: " + str(report["saturation_rate_all_valid"]),
        "- Saturation rate among rejected candidates: " + str(report["saturation_rate_rejected"]),
        "- Saturation rate among eligible candidates (primary degeneracy metric): " + str(report["saturation_rate_eligible"]),
        "- Saturation cutoff: " + str(report["saturation_max"]),
        "- All-or-none fraction among eligible candidates (secondary, not used for verdict): " + str(report["all_or_none_fraction_eligible"]),
        "- Completed batches: " + str(report["futility"]["completed_batches"]),
        "- Futility stop triggered: " + str(report["futility"]["triggered"]) + ("" if report["futility"]["first_triggered_batch"] is None else " (batch " + str(report["futility"]["first_triggered_batch"]) + ")"),
        "- Supported cells: " + str(report["supported_cell_count"]),
        "- Distinct supported k: " + str(report["distinct_supported_k"]),
        "- Unique provenance groups in supported cells: " + str(report["unique_groups_in_supported_cells"]),
        "- Distinct cross-group pairs with different C: " + str(report["cross_group_pairs_different_C"]), "",
        "## Distribution", "",
        "k: " + str(report["k_distribution"]), "",
        "max_j f_j: " + str(report["max_f_distribution"]), "",
        "## Supported cells", "",
        "| base algorithm | k | C levels (distinct groups) | candidate bodies |",
        "|---|---:|---|---:|",
    ]
    for cell in report["supported_cells"]:
        levels = ", ".join(str(level["C"]) + " (" + str(level["groups"]) + " groups)" for level in cell["levels"])
        lines.append("| " + str(cell["base_algorithm"]) + " | " + str(cell["k"]) + " | " + levels + " | " + str(cell["candidate_bodies"]) + " |")
    if not report["supported_cells"]:
        lines.append("| none | | | |")
    lines += [
        "",
        "Candidates that fail static checks or cannot load are invalid and receive no k. Runtime exceptions and timeouts during an individual probe count as that probe failing. The primary degeneracy metric is the saturation rate (fraction of eligible candidates with max_j f_j = 5), restricted to eligible candidates (2 <= k <= 24); it replaces the V1/V2 per-family all-or-none rate, which is confounded at low k. Futility is a predeclared stop rule evaluated at batches 100/200/300 (minimum 10/20/30 eligible provenance groups).",
        "",
        "A PASS would not establish predictive value or power. This is a footprint feasibility gate only.",
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
