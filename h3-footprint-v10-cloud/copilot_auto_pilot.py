"""Bounded keyless Copilot-Auto exploratory footprint screen.

This is not the frozen three-generator H3 gate, not held-out evaluation, and
not a confirmatory study. The generation path is capped at 12 requests with
no retries. Candidate source is parsed but never executed on the generation VM.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from typing import Any

MAX_REQUESTS = 12
REQUEST_TIMEOUT_SECONDS = 120
MAX_RESPONSE_BYTES = 128 * 1024

FORBIDDEN_IMPORTS = {
    "os", "subprocess", "socket", "pathlib", "shutil", "importlib", "ctypes",
    "multiprocessing", "threading", "requests", "urllib", "http", "ftplib",
    "telnetlib", "pickle", "marshal",
}
FORBIDDEN_CALLS = {"open", "eval", "exec", "compile", "__import__", "input", "breakpoint"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prompts() -> list[tuple[str, str]]:
    contract = (
        "Task: directed single-source/single-target shortest path. Implement "
        "solve(n, edges, s, t), where vertices are 0..n-1, edges is a list of "
        "(u, v, nonnegative integer weight) triples, and the return value is "
        "the shortest distance as an integer or -1 if t is unreachable. "
        "Output only valid Python source, no markdown fence, tests, explanation, "
        "or entry point. Include exactly one top-level synchronous function named "
        "solve. Keep all code self-contained. Do not use network access, subprocesses, "
        "filesystem access, dynamic code execution, or environment inspection."
    )
    instructions = {
        "direct": "Implement the function directly and correctly. " + contract,
        "menu": "Choose one appropriate algorithm, such as Dijkstra, Bellman-Ford, or Floyd-Warshall, and implement it. " + contract,
        "simple": "Prefer a straightforward, robust implementation over clever optimizations. " + contract,
    }
    # Fixed, balanced schedule: four requests per wording variant, interleaved.
    return [(f"request-{i + 1:02d}", variant, instructions[variant])
            for i in range(MAX_REQUESTS)
            for variant in [("direct", "menu", "simple")[i % 3]]]


def normalize_candidate(response: str) -> tuple[str | None, str | None]:
    source = response.strip()
    if source.startswith("```"):
        lines = source.splitlines()
        if len(lines) < 3 or not lines[-1].strip().startswith("```"):
            return None, "malformed_code_fence"
        source = "\n".join(lines[1:-1]).strip()
    if not source:
        return None, "empty_response"
    if len(source.encode("utf-8")) > MAX_RESPONSE_BYTES:
        return None, "response_over_128KiB"
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, TypeError):
        return None, "python_parse_error"

    solve_defs = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "solve"
    ]
    if len(solve_defs) != 1 or not isinstance(solve_defs[0], ast.FunctionDef):
        return None, "requires_exactly_one_sync_solve"

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.split(".")[0] in FORBIDDEN_IMPORTS for alias in node.names):
                return None, "forbidden_import"
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                return None, "forbidden_import"
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_CALLS:
                return None, "forbidden_call"

    # Preserve the complete module, but reject top-level code that would execute
    # during import. Literal constants, imports, docstrings and definitions pass.
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Import, ast.ImportFrom)):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if isinstance(node, ast.Assign):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError, MemoryError, RecursionError):
                return None, "top_level_nonliteral_assignment"
            continue
        if isinstance(node, ast.AnnAssign):
            if node.value is not None:
                try:
                    ast.literal_eval(node.value)
                except (ValueError, TypeError, MemoryError, RecursionError):
                    return None, "top_level_nonliteral_assignment"
            continue
        return None, "top_level_executable_code"

    return source + "\n", None


def error_category(stderr: bytes, returncode: int | None) -> str:
    text = stderr.decode("utf-8", "replace").lower()
    if "not available" in text:
        return "model_unavailable"
    if "unauthorized" in text or "authentication" in text or "401" in text:
        return "authentication_error"
    if "quota" in text or "rate limit" in text or "429" in text:
        return "quota_or_rate_limit"
    if returncode == 124:
        return "timeout"
    if returncode is None:
        return "timeout"
    return "cli_error"


def run_generation(out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = out_dir / "responses"
    body_dir = out_dir / "bodies"
    raw_dir.mkdir(exist_ok=True)
    body_dir.mkdir(exist_ok=True)

    version_result = subprocess.run(
        ["copilot", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=15, check=False,
    )
    cli_version = version_result.stdout.decode("utf-8", "replace").strip()[:200]

    records: list[dict[str, Any]] = []
    first_hash_request: dict[str, str] = {}
    schedule = prompts()
    if len(schedule) != MAX_REQUESTS or Counter(v for _, v, _ in schedule) != {"direct": 4, "menu": 4, "simple": 4}:
        raise AssertionError("fixed request schedule changed")

    for request_id, variant, prompt in schedule:
        started = time.time()
        proc = None
        stdout = b""
        stderr = b""
        returncode: int | None = None
        category = None
        try:
            proc = subprocess.Popen(
                ["copilot", "-p", prompt, "-s", "--no-ask-user", "--model=auto"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
            try:
                stdout, stderr = proc.communicate(timeout=REQUEST_TIMEOUT_SECONDS)
                returncode = proc.returncode
            except subprocess.TimeoutExpired as exc:
                stdout = exc.output or b""
                stderr = exc.stderr or b""
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
                try:
                    tail_out, tail_err = proc.communicate(timeout=5)
                    stdout = tail_out or stdout
                    stderr = tail_err or stderr
                except Exception:
                    pass
                returncode = 124
                category = "timeout"
        except (OSError, subprocess.SubprocessError) as exc:
            category = "cli_start_error" if isinstance(exc, OSError) else "cli_error"
            stderr = type(exc).__name__.encode()
            returncode = None

        response_path = raw_dir / f"{request_id}.raw.txt"
        response_sha = sha256(stdout)
        truncated = len(stdout) > MAX_RESPONSE_BYTES
        response_path.write_bytes(stdout[:MAX_RESPONSE_BYTES] if truncated else stdout)
        rec: dict[str, Any] = {
            "request_id": request_id,
            "provenance_group": request_id,
            "prompt_variant": variant,
            "provider_route": "GitHub Copilot CLI via GitHub Actions GITHUB_TOKEN",
            "model_requested": "auto",
            "actual_model_identity": "not exposed or verified by this CLI invocation",
            "cli_version": cli_version or None,
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "exit_code": returncode,
            "raw_response_sha256": response_sha,
            "raw_response_bytes": len(stdout),
            "raw_response_artifact_truncated": truncated,
            "raw_response_artifact_path": str(Path("responses") / response_path.name),
            "stderr_sha256": sha256(stderr),
            "stderr_bytes": len(stderr),
            "retry_count": 0,
            "candidate_generation_requested": True,
        }

        if category is None and returncode != 0:
            category = error_category(stderr, returncode)
        if category is not None or returncode != 0:
            rec.update({"status": "request_failed", "error_category": category or "cli_error"})
            records.append(rec)
            print(f"{request_id}: request_failed ({rec['error_category']})", flush=True)
            continue

        if truncated:
            rec.update({"status": "invalid_response", "error_category": "response_over_128KiB"})
            records.append(rec)
            print(f"{request_id}: invalid_response (response_over_128KiB)", flush=True)
            continue

        try:
            response = stdout.decode("utf-8")
        except UnicodeDecodeError:
            rec.update({"status": "invalid_response", "error_category": "response_not_utf8"})
            records.append(rec)
            print(f"{request_id}: invalid_response (response_not_utf8)", flush=True)
            continue

        source, invalid_reason = normalize_candidate(response)
        if invalid_reason:
            rec.update({"status": "invalid_response", "error_category": invalid_reason})
            records.append(rec)
            print(f"{request_id}: invalid_response ({invalid_reason})", flush=True)
            continue

        body_bytes = source.encode("utf-8")
        body_hash = sha256(body_bytes)
        body_path = body_dir / f"{request_id}.py"
        body_path.write_bytes(body_bytes)
        rec.update({
            "status": "candidate_ready",
            "body_sha256": body_hash,
            "body_bytes": len(body_bytes),
            "body_path": str(Path("bodies") / body_path.name),
        })
        if body_hash in first_hash_request:
            rec["duplicate_of"] = first_hash_request[body_hash]
        else:
            first_hash_request[body_hash] = request_id
            rec["duplicate_of"] = None
        records.append(rec)
        print(f"{request_id}: candidate_ready duplicate_of={rec['duplicate_of']}", flush=True)

    manifest = {
        "schema_version": 1,
        "kind": "copilot_auto_single_provider_exploratory_footprint_screen",
        "fixed_request_cap": MAX_REQUESTS,
        "requests_attempted": len(records),
        "retry_policy": "no retries",
        "prompt_schedule": {"direct": 4, "menu": 4, "simple": 4, "interleaved": True},
        "provider_route": "GitHub Copilot CLI via GitHub Actions GITHUB_TOKEN",
        "model_requested": "auto",
        "actual_model_identity_verified": False,
        "candidate_count_before_deduplication": sum(r["status"] == "candidate_ready" for r in records),
        "unique_candidate_body_count": len(first_hash_request),
        "H3_confirmatory_batches_started": False,
        "held_out_evaluation_performed": False,
        "H3_scientific_result": False,
        "requests": records,
    }
    (out_dir / "candidate-index.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "kind": manifest["kind"],
        "requests_attempted": manifest["requests_attempted"],
        "candidate_count_before_deduplication": manifest["candidate_count_before_deduplication"],
        "unique_candidate_body_count": manifest["unique_candidate_body_count"],
        "cap": MAX_REQUESTS,
        "actual_model_identity_verified": False,
        "H3_confirmatory_batches_started": False,
    }, indent=2))
    return 0


def classify_base_algorithm(source: str) -> str:
    s = source.lower()
    if "heapq" in s or "heappush" in s or "heappop" in s:
        return "heap_dijkstra"
    if "floyd" in s or ("dist" in s and "[[" in s and "range(n)" in s):
        return "floyd"
    if "bellman" in s or ("range(n - 1)" in s and "for u, v, w in edges" in s):
        return "bellman_ford"
    if "deque" in s or "collections" in s:
        return "bfs"
    if "def dfs" in s or "def walk" in s or "def visit" in s:
        return "dfs_bruteforce"
    return "other"


def run_scoring(index_path: Path, reports_dir: Path, expected_path: Path,
                instrument_path: Path, out_path: Path) -> int:
    inst_dir = str(instrument_path.resolve().parent)
    if inst_dir not in sys.path:
        sys.path.insert(0, inst_dir)
    import instrument  # trusted frozen instrument, only in the separate scoring job

    index = json.loads(index_path.read_text(encoding="utf-8"))
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    probes = instrument.PROBES
    probe_ids = [p["probe_id"] for p in probes]
    if len(probes) != 30 or len(probe_ids) != len(set(probe_ids)) or set(expected) != set(probe_ids):
        raise ValueError("instrument/expected-answer inventory is inconsistent")

    invalid_reasons: Counter[str] = Counter()
    scored: list[dict[str, Any]] = []
    duplicate_count = 0
    first_hash: dict[str, str] = {}
    request_records = index.get("requests", [])
    for rec in request_records:
        if rec.get("status") != "candidate_ready":
            invalid_reasons[str(rec.get("error_category") or rec.get("status") or "unknown")] += 1
            continue
        request_id = rec["request_id"]
        body_hash = rec.get("body_sha256")
        if not isinstance(body_hash, str) or len(body_hash) != 64:
            raise ValueError(f"missing body hash for {request_id}")
        if body_hash in first_hash:
            duplicate_count += 1
            continue
        first_hash[body_hash] = request_id

        report_path = reports_dir / f"{request_id}.json"
        if not report_path.exists():
            raise ValueError(f"missing isolated execution report for {request_id}")
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report.get("candidate_sha256") != body_hash:
            raise ValueError(f"candidate hash mismatch for {request_id}")
        if report.get("isolation_harness_ok") is not True or report.get("all_trees_empty") is not True:
            raise ValueError(f"execution boundary not verified for {request_id}")
        if report.get("probe_count") != 30 or len(report.get("results", [])) != 30:
            raise ValueError(f"wrong result count for {request_id}")
        result_map = {r.get("probe_id"): r for r in report["results"]}
        if len(result_map) != 30 or set(result_map) != set(probe_ids):
            raise ValueError(f"probe inventory mismatch for {request_id}")
        if any(r.get("status") == "load_error" for r in report["results"]):
            invalid_reasons["candidate_load_error"] += 1
            continue

        fails = []
        for pid in probe_ids:
            row = result_map[pid]
            correct = (
                row.get("status") == "ok"
                and row.get("answer_type") == "int"
                and type(row.get("answer")) is int
                and row.get("answer") == expected[pid]
            )
            fails.append(not correct)
        family_counts = instrument.family_counts(fails)
        k = sum(fails)
        if k != sum(family_counts.values()):
            raise AssertionError("family counts do not sum to k")
        max_family_count = max(family_counts.values())
        concentration = None if k == 0 else max_family_count / k
        if k == 0:
            eligible = False
        else:
            eligible = 2 <= k <= 24
        body_path = Path(index_path).parent / rec["body_path"]
        source = body_path.read_text(encoding="utf-8")
        row = {
            "request_id": request_id,
            "provenance_group": rec["provenance_group"],
            "prompt_variant": rec["prompt_variant"],
            "model_requested": "auto",
            "actual_model_identity_verified": False,
            "body_sha256": body_hash,
            "base_algorithm": classify_base_algorithm(source),
            "valid_for_k": True,
            "k": k,
            "family_counts": family_counts,
            "max_family_count": max_family_count,
            "C": concentration,
            "eligible_2_to_24": eligible,
            "saturated_max_family": max_family_count == 5,
            "probe_failure_count": sum(fails),
            "correct_probe_count": 30 - sum(fails),
        }
        scored.append(row)

    k_distribution = Counter(str(r["k"]) for r in scored)
    saturation_rate = (
        sum(r["saturated_max_family"] for r in scored if r["eligible_2_to_24"])
        / sum(r["eligible_2_to_24"] for r in scored)
        if any(r["eligible_2_to_24"] for r in scored) else None
    )
    cells: dict[tuple[str, int], dict[int, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in scored:
        if row["eligible_2_to_24"]:
            cells[(row["base_algorithm"], row["k"])][row["max_family_count"]].append(row)
    supported_cells = []
    variation_cells = []
    cross_c_pairs = 0
    for (algorithm, k), levels in sorted(cells.items()):
        level_counts = {str(max_f): len({r["provenance_group"] for r in rows}) for max_f, rows in sorted(levels.items())}
        if len(levels) >= 2:
            variation_cells.append({
                "base_algorithm": algorithm, "k": k,
                "C_levels": {str(max_f): max_f / k for max_f in sorted(levels)},
                "distinct_group_counts_per_C_level": level_counts,
            })
            for a, b in itertools.combinations(sorted(levels), 2):
                cross_c_pairs += len({r["provenance_group"] for r in levels[a]}) * len({r["provenance_group"] for r in levels[b]})
        if sum(n >= 4 for n in level_counts.values()) >= 2:
            supported_cells.append({
                "base_algorithm": algorithm, "k": k,
                "C_levels": {str(max_f): max_f / k for max_f in sorted(levels)},
                "distinct_group_counts_per_C_level": level_counts,
                "distinct_groups": sum(len({r["provenance_group"] for r in rows}) for rows in levels.values()),
            })

    report = {
        "schema_version": 1,
        "kind": "copilot_auto_single_provider_exploratory_footprint_screen",
        "interpretation": "exploratory screen only; not the frozen three-generator H3 gate",
        "fixed_request_cap": MAX_REQUESTS,
        "requests_attempted": len(request_records),
        "raw_candidate_ready_responses": sum(r.get("status") == "candidate_ready" for r in request_records),
        "valid_unique_candidates_assigned_k": len(scored),
        "unique_candidate_body_duplicates_excluded": duplicate_count,
        "invalid_or_failed_request_counts": dict(sorted(invalid_reasons.items())),
        "k_distribution_valid_candidates": dict(sorted(k_distribution.items(), key=lambda x: int(x[0]))),
        "eligible_candidate_count_2_to_24": sum(r["eligible_2_to_24"] for r in scored),
        "eligible_saturation_rate": saturation_rate,
        "same_k_different_C_observed": bool(variation_cells),
        "same_k_different_C_cells": variation_cells,
        "supported_cells_under_m_min_4": supported_cells,
        "supported_cell_count": len(supported_cells),
        "cross_C_group_pair_count": cross_c_pairs,
        "candidate_results": scored,
        "original_gate_pass_claimed": False,
        "original_gate_verdict": "NOT_APPLICABLE_TO_12-REQUEST_SCREEN",
        "reason_no_gate_verdict": "The screen has a fixed cap of 12 requests and cannot meet the original 40-group PASS requirement or its three-supported-cell threshold by design.",
        "provider_route": "GitHub Copilot CLI via GitHub Actions GITHUB_TOKEN",
        "model_requested": "auto",
        "actual_model_identity_verified": False,
        "H3_confirmatory_batches_started": False,
        "held_out_evaluation_performed": False,
        "H3_scientific_result": False,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "kind": report["kind"],
        "requests_attempted": report["requests_attempted"],
        "valid_unique_candidates_assigned_k": report["valid_unique_candidates_assigned_k"],
        "eligible_candidate_count_2_to_24": report["eligible_candidate_count_2_to_24"],
        "same_k_different_C_observed": report["same_k_different_C_observed"],
        "supported_cell_count": report["supported_cell_count"],
        "cross_C_group_pair_count": report["cross_C_group_pair_count"],
        "original_gate_verdict": report["original_gate_verdict"],
        "H3_scientific_result": False,
    }, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    gen = commands.add_parser("generate")
    gen.add_argument("--out-dir", required=True)
    score = commands.add_parser("score")
    score.add_argument("--index", required=True)
    score.add_argument("--reports-dir", required=True)
    score.add_argument("--expected-values", required=True)
    score.add_argument("--instrument", required=True)
    score.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.command == "generate":
        return run_generation(Path(args.out_dir))
    return run_scoring(
        Path(args.index), Path(args.reports_dir), Path(args.expected_values),
        Path(args.instrument), Path(args.out),
    )


if __name__ == "__main__":
    raise SystemExit(main())
