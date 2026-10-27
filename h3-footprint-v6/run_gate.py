from __future__ import annotations

import argparse
import ast
import builtins
import contextlib
import hashlib
import json
import math
import re
import secrets
import subprocess
import symtable
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import instrument

HARNESS_ROOT = Path(__file__).resolve().parent
ROOT = HARNESS_ROOT
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


def _dotted_name(node: ast.AST) -> str | None:
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def _import_map(tree: ast.Module) -> dict[str, str]:
    imported: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name.split(".")[0]
                imported[local] = alias.name if alias.asname else local
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                local = alias.asname or alias.name
                imported[local] = node.module + "." + alias.name
    return imported


def _resolve_call(name: str, imported: dict[str, str]) -> str:
    root, _, rest = name.partition(".")
    if root in imported:
        base = imported[root]
        return base + ("." + rest if rest else "")
    return name


_SCOPE_BOUNDARIES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)


def _own_walk(node: ast.AST):
    """Walk a function body without descending into nested scopes."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _SCOPE_BOUNDARIES):
            continue
        yield child
        yield from _own_walk(child)


def _reachable_functions(tree: ast.Module) -> list[ast.FunctionDef]:
    """Functions reachable from solve; unused helpers cannot affect the label."""
    funcs: dict[str, list[ast.FunctionDef]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs.setdefault(node.name, []).append(node)
    if "solve" not in funcs:
        return []
    seen: set[str] = set()
    stack = ["solve"]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        for func in funcs.get(name, []):
            for item in _own_walk(func):
                if isinstance(item, ast.Call):
                    called = _dotted_name(item.func)
                    if called and called in funcs:
                        stack.append(called)
    return [func for name in seen for func in funcs.get(name, [])]


def _max_for_depth(node: ast.AST, depth: int = 0) -> int:
    if isinstance(node, ast.For):
        depth += 1
    best = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _SCOPE_BOUNDARIES):
            continue
        best = max(best, _max_for_depth(child, depth))
    return best


def _has_nested_subscript(node: ast.AST) -> bool:
    for item in _own_walk(node):
        if isinstance(item, ast.Subscript) and isinstance(item.value, ast.Subscript):
            return True
    return False


def _has_recursive_reachable_function(functions: list[ast.FunctionDef]) -> bool:
    for func in functions:
        for item in _own_walk(func):
            if isinstance(item, ast.Call) and _dotted_name(item.func) == func.name:
                return True
    return False


def base_label(source: str) -> str:
    """Conservative structural classifier over the syntax tree.

    Only imported names that are actually called from solve or its reachable
    helpers count. Comments, docstrings, unused imports, and unused helpers
    cannot change the label. If zero or multiple algorithm signals are
    present, return "other" rather than assigning a cell on weak evidence.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return "other"
    functions = _reachable_functions(tree)
    if not functions:
        return "other"
    imported = _import_map(tree)
    calls: set[str] = set()
    attr_names: set[str] = set()
    for func in functions:
        for node in _own_walk(func):
            if isinstance(node, ast.Call):
                name = _dotted_name(node.func)
                if name:
                    calls.add(_resolve_call(name, imported))
            elif isinstance(node, ast.Attribute):
                attr_names.add(node.attr)

    parents: dict[ast.AST, ast.AST] = {}
    for func in functions:
        for parent in _own_walk(func):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent
    range_ancestor = False
    for func in functions:
        for loop in _own_walk(func):
            if not (isinstance(loop, ast.For) and isinstance(loop.iter, ast.Name) and loop.iter.id == "edges"):
                continue
            current = parents.get(loop)
            while current is not None:
                if isinstance(current, ast.For) and isinstance(current.iter, ast.Call):
                    if _dotted_name(current.iter.func) == "range":
                        range_ancestor = True
                        break
                current = parents.get(current)
            if range_ancestor:
                break
        if range_ancestor:
            break

    signals: set[str] = set()
    if calls & {"heapq.heappush", "heapq.heappop"}:
        signals.add("heap_dijkstra")
    if "collections.deque" in calls and attr_names & {"popleft", "appendleft"}:
        signals.add("bfs")
    if range_ancestor:
        signals.add("bellman_ford")
    if any(_max_for_depth(func) >= 3 and _has_nested_subscript(func) for func in functions):
        signals.add("floyd")
    if _has_recursive_reachable_function(functions):
        signals.add("dfs_bruteforce")
    return signals.pop() if len(signals) == 1 else "other"


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


def _nonce_payload(stdout: str, nonce: str) -> dict | None:
    # The worker prints exactly one nonce-tagged line. Candidate code shares
    # the worker process and can print extra lines (for example from atexit),
    # so require exactly one match and ignore everything else. Zero or
    # multiple matches are malformed and invalidate the candidate.
    prefix = nonce + " "
    matches = [line[len(prefix):] for line in stdout.splitlines() if line.startswith(prefix)]
    if len(matches) != 1:
        return None
    try:
        value = json.loads(matches[0])
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _load_expected() -> dict[str, int]:
    return json.loads((HARNESS_ROOT / "expected_values.json").read_text(encoding="utf-8"))


def _probe_input(probe: dict) -> str:
    return json.dumps({
        "n": probe["n"],
        "edges": [list(edge) for edge in probe["edges"]],
        "s": probe["s"],
        "t": probe["t"],
    }, sort_keys=True)


def _invalid_candidate(row: dict, reason: str) -> dict:
    row.update({
        "excluded": reason, "load_error": reason, "fails": None,
        "family_counts": None, "k": None, "C": None, "max_f": None,
        "eligible": False, "probes_completed": 0,
    })
    return row


def evaluate_body(
    path: Path,
    meta: dict[str, dict],
    expected: dict[str, int] | None = None,
    scratch_dir: Path | str | None = None,
) -> dict:
    source = path.read_text(encoding="utf-8")
    h = path.stem
    info = meta.get(h) or {}
    row = {
        "body_hash": h, "base_algorithm": base_label(source),
        "source_chars": len(source), "excluded": None, "timeout": False,
        "fails": None, "k": None, "C": None,
        "group_id": info.get("group_id"), "generator": info.get("model"),
        "prompt_variant": info.get("prompt_variant"), "batch_id": info.get("batch_id"),
    }
    reason = unsafe_reason(source)
    if reason:
        return _invalid_candidate(row, reason)
    missing = undefined_global_names(source)
    if missing:
        return _invalid_candidate(row, "undefined_name:" + ",".join(missing))
    if row["group_id"] is None:
        return _invalid_candidate(row, "missing_provenance")

    if expected is None:
        expected = _load_expected()

    scratch_base = Path(scratch_dir) if scratch_dir is not None else None
    if scratch_base is not None:
        scratch_base.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="h3probe-", dir=str(scratch_base) if scratch_base else None) as td:
        scratch = Path(td)
        nonce = secrets.token_hex(16)
        try:
            proc = subprocess.run(
                [sys.executable, "-I", str(WORKER), str(path), "--preflight", nonce],
                cwd=str(scratch), capture_output=True, text=True, timeout=5,
                encoding="utf-8", errors="replace",
            )
        except subprocess.TimeoutExpired:
            return _invalid_candidate(row, "preflight_timeout")
        except Exception as exc:
            return _invalid_candidate(row, "preflight_runner_error:" + type(exc).__name__)
        pre = _nonce_payload(proc.stdout, nonce)
        if proc.returncode != 0 or pre is None:
            return _invalid_candidate(row, "preflight_invalid_output")
        if pre.get("phase") != "preflight" or pre.get("valid") is not True or pre.get("load_error"):
            detail = pre.get("load_error") or pre.get("error") or "candidate did not load"
            return _invalid_candidate(row, "load_error:" + str(detail))

        fails: list[bool] = []
        had_probe_timeout = False
        for probe_index, probe in enumerate(instrument.PROBES):
            nonce = secrets.token_hex(16)
            try:
                proc = subprocess.run(
                    [sys.executable, "-I", str(WORKER), str(path), "--probe", str(probe_index),
                     _probe_input(probe), nonce],
                    cwd=str(scratch), capture_output=True, text=True, timeout=5,
                    encoding="utf-8", errors="replace",
                )
            except subprocess.TimeoutExpired:
                had_probe_timeout = True
                fails.append(True)
                continue
            except Exception as exc:
                return _invalid_candidate(row, "probe_runner_error:" + type(exc).__name__)
            data = _nonce_payload(proc.stdout, nonce)
            if proc.returncode != 0 or data is None:
                return _invalid_candidate(row, "probe_invalid_output")
            if data.get("phase") == "load" or data.get("load_error"):
                return _invalid_candidate(row, "load_error_during_probe")
            if data.get("phase") != "probe" or data.get("probe_index") != probe_index:
                return _invalid_candidate(row, "probe_invalid_output")
            if "error" in data:
                fails.append(True)
                continue
            if "answer" not in data:
                return _invalid_candidate(row, "probe_invalid_output")
            answer = data["answer"]
            expected_value = expected[probe["probe_id"]]
            # The parent owns the comparison. The child only returns the raw
            # answer, so a forged answer is merely a wrong answer, not a
            # forged verdict.
            bad = isinstance(answer, bool) or not isinstance(answer, int) or answer != expected_value
            fails.append(bad)

    counts = instrument.family_counts(fails)
    k, c = instrument.concentration(fails)
    row.update({
        "excluded": None, "load_error": None, "fails": fails, "family_counts": counts, "timeout": had_probe_timeout,
        "k": k, "C": c, "max_f": max(counts.values()),
        "eligible": 2 <= k <= 24, "probes_completed": len(fails),
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


def _futility(eligible: list[dict], support_eligible: list[dict] | None = None) -> dict:
    """Predeclared stop rule evaluated at completed-batch checkpoints.

    At checkpoint c, count distinct eligible provenance groups from batches
    with batch_id < c. Trigger if that count is below the frozen minimum.
    The support-eligible count is reported separately because "other"
    candidates can meet the pace without being able to form a supported cell.
    """
    support_eligible = eligible if support_eligible is None else support_eligible
    completed = _completed_batches()
    checkpoints = []
    first_triggered = None
    for batch, minimum in sorted(FUTILITY_CHECKPOINTS.items()):
        reached = completed >= batch
        groups_at = None
        support_groups_at = None
        triggered_here = False
        if reached:
            group_ids = {
                row["group_id"]
                for row in eligible
                if row.get("group_id") and isinstance(row.get("batch_id"), int) and row["batch_id"] < batch
            }
            support_group_ids = {
                row["group_id"]
                for row in support_eligible
                if row.get("group_id") and isinstance(row.get("batch_id"), int) and row["batch_id"] < batch
            }
            groups_at = len(group_ids)
            support_groups_at = len(support_group_ids)
            triggered_here = groups_at < minimum
            if triggered_here and first_triggered is None:
                first_triggered = batch
        checkpoints.append({
            "batch": batch,
            "min_eligible_groups": minimum,
            "reached": reached,
            "eligible_groups_at_checkpoint": groups_at,
            "support_eligible_groups_at_checkpoint": support_groups_at,
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


def build(scratch_dir: Path | str | None = None, expected: dict[str, int] | None = None) -> dict:
    meta = body_meta()
    if expected is None:
        expected = _load_expected()
    rows = [evaluate_body(p, meta, expected, scratch_dir) for p in sorted(BODIES.glob("*.py"))]
    invalid_rows = [r for r in rows if r["excluded"] is not None]
    valid_rows = [r for r in rows if r["excluded"] is None and r.get("k") is not None]
    rejected = [r for r in valid_rows if r["k"] > 0]
    eligible = [r for r in valid_rows if 2 <= r["k"] <= 24]
    # "other" is a residual label for structurally unidentified solvers. It
    # remains in counts, distributions, degeneracy, and futility, but it cannot
    # form or support a (base algorithm, k) cell because that would pool
    # different algorithms into one cell.
    other_eligible = [r for r in eligible if r["base_algorithm"] == "other"]
    support_eligible = [r for r in eligible if r["base_algorithm"] != "other"]
    cells = defaultdict(lambda: defaultdict(list))
    for row in support_eligible:
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
    futility = _futility(eligible, support_eligible)
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
        "valid_bodies": len(valid_rows), "invalid_candidates": len(invalid_rows),
        "eligible_bodies": len(eligible),
        "eligible_groups": len({r["group_id"] for r in eligible if r.get("group_id")}),
        "support_eligible_bodies": len(support_eligible),
        "support_eligible_groups": len({r["group_id"] for r in support_eligible if r.get("group_id")}),
        "other_eligible_bodies": len(other_eligible),
        "other_eligible_groups": len({r["group_id"] for r in other_eligible if r.get("group_id")}),
        "other_excluded_from_supported_cells": True,
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
        "- Support-eligible bodies (identified algorithm): " + str(report["support_eligible_bodies"]),
        "- Support-eligible provenance groups: " + str(report["support_eligible_groups"]),
        "- Other-labelled eligible bodies (reported, excluded from cells): " + str(report["other_eligible_bodies"]),
        "- Other-labelled eligible provenance groups: " + str(report["other_eligible_groups"]),
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
        "Candidates that fail static checks or cannot load are invalid and receive no k. Runtime exceptions and timeouts during an individual probe count as that probe failing. The primary degeneracy metric is the saturation rate (fraction of eligible candidates with max_j f_j = 5), restricted to eligible candidates (2 <= k <= 24); it replaces the V1/V2 per-family all-or-none rate, which is confounded at low k. Futility is a predeclared stop rule evaluated at batches 100/200/300 (minimum 10/20/30 eligible provenance groups). Candidates labelled other remain in all counts, distributions, degeneracy rates, and futility, but cannot form a supported cell or contribute to the PASS group count; pooling unidentified algorithms would otherwise create a false PASS.",
        "",
        "A PASS would not establish predictive value or power. This is a footprint feasibility gate only.",
    ]
    return "\n".join(lines) + "\n"


CORE_ARTIFACTS = ["run_gate.py", "probe_worker.py", "instrument.py", "expected_values.json"]
REQUIRED_ISOLATION_CHECKS = [
    "evaluator_inside_sandbox",
    "network_blocked",
    "host_write_blocked",
    "expected_values_write_blocked",
    "other_candidate_write_blocked",
    "extra_output_rejected",
    "repo_not_present",
    "correct_result_after_tamper_attempts",
]


def _canonical_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify_frozen(manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    recorded = manifest.get("artifact_hashes_sha256") or {}
    checked = {}
    ok = True
    for name in CORE_ARTIFACTS:
        expected = recorded.get(name)
        actual = _canonical_hash(ROOT / name)
        match = expected == actual
        checked[name] = {"expected": expected, "actual": actual, "ok": match}
        ok = ok and match
    return {"manifest": str(manifest_path), "checked": checked, "ok": ok}


def load_isolation_report(path: Path) -> dict:
    report = json.loads(path.read_text(encoding="utf-8"))
    failed = [name for name in REQUIRED_ISOLATION_CHECKS if report.get(name) is not True]
    return {"path": str(path), "failed_checks": failed, "ok": not failed}


def main() -> None:
    global RESULTS
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default=str(RESULTS))
    parser.add_argument("--scratch-dir", default=None)
    parser.add_argument("--freeze-manifest", required=True)
    parser.add_argument("--isolation-report", required=True)
    args = parser.parse_args()

    RESULTS = Path(args.results_dir)
    manifest = Path(args.freeze_manifest)
    isolation = load_isolation_report(Path(args.isolation_report))
    if not isolation["ok"]:
        raise SystemExit("Refusing to evaluate: isolation report failed checks " + ", ".join(isolation["failed_checks"]))
    integrity_start = verify_frozen(manifest)
    if not integrity_start["ok"]:
        raise SystemExit("Refusing to evaluate: frozen harness hash mismatch.")

    RESULTS.mkdir(parents=True, exist_ok=True)
    report = build(scratch_dir=args.scratch_dir)
    integrity_end = verify_frozen(manifest)
    report["isolation"] = isolation
    report["harness_integrity"] = {"start": integrity_start, "end": integrity_end}
    if not integrity_end["ok"]:
        report["verdict"] = "FAIL"
        report["reason"] = "harness_modified_during_run"
    (RESULTS / "footprint.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    (RESULTS / "REPORT.md").write_text(markdown(report), encoding="utf-8")
    print(markdown(report))


if __name__ == "__main__":
    main()
