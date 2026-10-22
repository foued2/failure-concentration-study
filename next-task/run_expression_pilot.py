"""Run the preregistered expression pilot; no predictive model is fitted.

Preflight is the default. A generation run requires the explicit ``--execute``
flag. Tests inject a fake generator and executor and never contact a provider.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Callable

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PILOT = REPO / "natural-feasibility-pilot"
PIPELINE = PILOT / "python-pipeline-integration"
EXPRESSION_PIPELINE = ROOT / "pipeline_expression_strict"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PILOT))
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(PIPELINE))

import run_generated_smoke as suite_runner
from expression_task import FAMILY_ORDER, evaluate_ast, validate_bank
from integration_runner import CaptureRejected
from pilot_tool import body_id
from source_policy import screen_source

CAP = 30
PROVIDER = "Google Gemini API"
MODEL = "gemini-3.5-flash-lite"
ENDPOINT_HOST = "generativelanguage.googleapis.com"
ENDPOINT_PATH = f"/v1beta/models/{MODEL}:generateContent"
GENERATION_CONFIG = {"temperature": 1.0, "maxOutputTokens": 4096}
RUN_LABEL = "expression-pilot-gemini"
PROTOCOL_03 = ROOT / "03_PILOT_PREREGISTRATION_2026-10-22.md"
AMENDMENT_03A = ROOT / "03A_PREREGISTRATION_AMENDMENT_2026-10-22.md"
AMENDMENT_03B = ROOT / "03B_OUTPUT_CONTRACT_AMENDMENT_2026-10-22.md"
LAUNCH_PRECONDITIONS_03C = ROOT / "03C_PILOT_LAUNCH_PRECONDITIONS_2026-10-22.md"
BANKS = ROOT / "banks"
DIAGNOSTIC_PATH = BANKS / "diagnostic.json"
EVALUATION_PATH = BANKS / "evaluation.json"
FREEZE_PATH = BANKS / "FREEZE.json"
MANIFEST_PATH = BANKS / "BUILD_MANIFEST.json"
PROVIDER_BLOCK_MARKERS = ("usage limit", "rate limit", "quota", "too many requests", "hard block")
HALT_STATES = {"HALTED_GENERATION_AUTH", "HALTED_GENERATION_USAGE_LIMIT"}

PROMPT = (
    "Write one Python implementation of a function `solve(expr)` that evaluates a bounded "
    "integer arithmetic expression given as a string. The expression contains non-negative "
    "integer literals, binary operators `+`, `-`, `*`, parentheses, optional ASCII spaces, "
    "and a unary minus before a primary. There is no division or exponentiation. Return the "
    "exact integer result as an `int`. Make the function self-contained and use only the "
    "Python standard library. Do not read files, access the network, or print. Return only "
    "Python source code defining `solve`, with no Markdown fences, explanation, example "
    "usage, or tests. Write the first solution that comes to mind; do not self-review or "
    "revise it."
)

ROW_STATUSES = {"pass", "wrong", "wrong_type", "invalid", "error", "timeout", "crash", "overflow"}
TRANSPORT_STATUSES = {"complete", "timeout", "crash", "overflow"}
EXECUTION_STATUSES = {"not_run", "duplicate_skipped", "source_rejected", "complete", "runner_error"}
GENERATION_STATUSES = {"generated", "generation_failed", "generation_timeout"}
STRICT_PIPELINE_NAME = "pipeline_expression_strict"
STRICT_ADAPTER_SHA256 = "d7a96e7d59f92f86858a29104c74a141bb9debeb9a85d9d98b58cd11cce55a67"


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temp, path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_strict_adapter() -> str:
    if EXPRESSION_PIPELINE.name != STRICT_PIPELINE_NAME:
        raise RuntimeError("the runner is not pointed at the strict expression pipeline")
    adapter = EXPRESSION_PIPELINE / "python_adapter.py"
    if not adapter.is_file():
        raise RuntimeError("strict expression adapter is missing")
    actual = sha256_file(adapter)
    if actual != STRICT_ADAPTER_SHA256:
        raise RuntimeError(
            "strict expression adapter hash does not match the strict calibration adapter")
    return actual


def git_state() -> dict:
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO, check=True, capture_output=True,
            text=True).stdout.strip()
        tracked = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=REPO,
            check=True, capture_output=True, text=True).stdout
        untracked_next_task = subprocess.run(
            ["git", "status", "--porcelain", "--", "next-task"], cwd=REPO,
            check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("cannot inspect repository state") from exc
    if not head:
        raise RuntimeError("repository HEAD is unavailable")
    return {
        "head": head,
        "tracked_dirty": bool(tracked.strip()),
        "next_task_dirty": bool(untracked_next_task.strip()),
    }


def require_clean_launch_tree() -> str:
    state = git_state()
    if state["tracked_dirty"] or state["next_task_dirty"]:
        raise RuntimeError(
            "commit the corrected expression-runner set before --execute; "
            "tracked changes or uncommitted next-task files are present")
    return state["head"]


def validate_run_label(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", value):
        raise ValueError("run label must be 1-64 safe path characters")
    return value


def parse_not_before(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("--not-before must include a timezone")
    return parsed.astimezone(timezone.utc)


def redact_secret(value: str, secret: str | None) -> str:
    return value.replace(secret, "[REDACTED]") if secret else value


def load_preregistered_prompt(path: Path = PROTOCOL_03) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("> Write one Python implementation of a function `solve(expr)`"):
            return line[2:].strip()
    raise RuntimeError("the exact expression prompt is missing from the preregistration")


def load_frozen_banks() -> tuple[list[dict], list[dict], dict]:
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    if freeze.get("status") != "FROZEN_FOR_CALIBRATION":
        raise RuntimeError("expression banks are not frozen for calibration")
    if freeze.get("no_model_calls") is not True:
        raise RuntimeError("freeze record does not attest zero model calls")
    if freeze.get("manifest_sha256") != sha256_file(MANIFEST_PATH):
        raise RuntimeError("bank manifest changed after freeze")
    docs = {}
    for name, path, id_key in (
        ("diagnostic", DIAGNOSTIC_PATH, "probe_id"),
        ("evaluation", EVALUATION_PATH, "hid"),
    ):
        expected_hash = freeze[name]["sha256"]
        if sha256_file(path) != expected_hash:
            raise RuntimeError(f"{name} bank changed after freeze")
        doc = json.loads(path.read_text(encoding="utf-8"))
        if doc.get("task_id") != freeze["task_id"]:
            raise RuntimeError(f"{name} bank task identity does not match freeze record")
        records = doc["records"]
        validate_bank(records, 5)
        ids = [record.get(id_key) for record in records]
        if len(ids) != 30 or None in ids or len(set(ids)) != 30:
            raise RuntimeError(f"{name} bank record identities are not unique")
        if any(evaluate_ast(record["expr"]) != record["expected"] for record in records):
            raise RuntimeError(f"{name} bank expected value disagrees with the AST oracle")
        if any(record.get("family") not in FAMILY_ORDER for record in records):
            raise RuntimeError(f"{name} bank has an unknown family")
        docs[name] = records
    if {r["expr"] for r in docs["diagnostic"]} & {r["expr"] for r in docs["evaluation"]}:
        raise RuntimeError("diagnostic and evaluation expression strings overlap")
    return docs["diagnostic"], docs["evaluation"], freeze


def guest_entries(records: list[dict], id_key: str) -> list[dict]:
    """Return the guest payload: identity and expression only, never oracle data."""
    return [{"probe_id": record[id_key], "input": {"expr": record["expr"]}} for record in records]


def host_metadata(records: list[dict], id_key: str) -> dict[str, dict]:
    return {
        record[id_key]: {
            "probe_id": record[id_key],
            "family": record["family"],
            "expr": record["expr"],
            "expected": record["expected"],
        }
        for record in records
    }


class WrongReturnType(ValueError):
    """The guest returned a value whose Python type is not exactly int."""

    def __init__(self, return_type: str):
        self.return_type = return_type
        super().__init__(f"return type is {return_type!r}, expected exact int")


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise CaptureRejected(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_expression_return(raw: dict) -> dict:
    """Parse the strict guest envelope; reject every non-int return type."""
    if raw.get("status") == "overflow":
        raise CaptureRejected("bounded stdout limit exceeded")
    try:
        data = base64.b64decode(raw["stdout_b64"], validate=True)
        if len(data) > 64 * 1024:
            raise CaptureRejected("worker stdout exceeds byte limit")
        text = data.decode("utf-8", errors="strict")
    except (ValueError, UnicodeDecodeError, KeyError) as exc:
        raise CaptureRejected(f"malformed worker stdout: {exc}") from exc
    if text.endswith("\r\n"):
        text = text[:-2]
    elif text.endswith("\n"):
        text = text[:-1]
    if not text or "\n" in text or "\r" in text:
        raise CaptureRejected("worker output is not one strict envelope")
    try:
        envelope = json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CaptureRejected(f"malformed return envelope: {exc}") from exc
    if not isinstance(envelope, dict) or set(envelope) not in (
        {"return_type"}, {"return_type", "value"},
    ):
        raise CaptureRejected("return envelope has missing or unexpected fields")
    return_type = envelope.get("return_type")
    if not isinstance(return_type, str) or not return_type:
        raise CaptureRejected("return envelope has an invalid return_type")
    if return_type != "int":
        raise WrongReturnType(return_type)
    value = envelope.get("value")
    if not isinstance(value, str) or not re.fullmatch(r"-?[0-9]+", value):
        raise CaptureRejected("return envelope has a malformed integer value")
    return {"return_type": "int", "value": int(value)}


def expression_outcome(raw: dict, entry: dict, meta: dict, phase: str) -> dict:
    expected = meta["expected"]
    parsed = None
    return_type = None
    error = None
    correct = False
    if raw.get("status") == "complete" and raw.get("exit_code") == 0 and not raw.get("timed_out"):
        try:
            parsed = parse_expression_return(raw)["value"]
            return_type = "int"
            correct = type(parsed) is int and parsed == expected
        except WrongReturnType as exc:
            return_type = exc.return_type
            error = str(exc)
        except CaptureRejected as exc:
            error = str(exc)
    else:
        error = str(raw.get("status", "error"))
    status = (
        "pass" if correct
        else "wrong" if parsed is not None
        else "wrong_type" if return_type is not None
        else "invalid" if raw.get("status") == "complete"
        else str(raw.get("status", "error"))
    )
    return {
        "phase": phase,
        "probe_id": entry["probe_id"],
        "family": meta["family"],
        "expr": meta["expr"],
        "expected": expected,
        "solver_output": parsed,
        "return_type": return_type,
        "correct": correct,
        "status": status,
        "error": error,
        "raw_stdout_b64": raw.get("stdout_b64", ""),
        "raw_stderr_b64": raw.get("stderr_b64", ""),
        "exit_code": raw.get("exit_code"),
        "timed_out": bool(raw.get("timed_out", False)),
        "tree_terminated": bool(raw.get("tree_terminated", False)),
        "worker_elapsed_ms": raw.get("elapsed_ms"),
    }


def diagnostic_summary(rows: list[dict]) -> dict:
    counts = {family: 0 for family in FAMILY_ORDER}
    for row in rows:
        if row["status"] != "pass":
            counts[row["family"]] += 1
    k = sum(counts.values())
    c = max(counts.values()) / k if k else 0.0
    return {
        "probe_ids": [row["probe_id"] for row in rows],
        "probe_rows": rows,
        "rows": len(rows),
        "passed": len(rows) - k,
        "failed": k,
        "family_order": FAMILY_ORDER,
        "family_counts": counts,
        "k": k,
        "C": c,
        "status_counts": dict(sorted(Counter(row["status"] for row in rows).items())),
        "all_tree_terminated": all(row["tree_terminated"] and not row["timed_out"] for row in rows),
        "timed_out": any(row["timed_out"] for row in rows),
    }


def evaluation_summary(rows: list[dict]) -> dict:
    correct_count = sum(1 for row in rows if row["correct"])
    return {
        "probe_ids": [row["probe_id"] for row in rows],
        "probe_rows": rows,
        "rows": len(rows),
        "correct_count": correct_count,
        "failed": len(rows) - correct_count,
        "pass_fraction": correct_count / len(rows) if rows else 0.0,
        "all_correct": bool(rows) and correct_count == len(rows),
        "status_counts": dict(sorted(Counter(row["status"] for row in rows).items())),
        "all_tree_terminated": all(row["tree_terminated"] and not row["timed_out"] for row in rows),
        "timed_out": any(row["timed_out"] for row in rows),
    }


def validate_suite_rows(rows: list[dict], entries: list[dict], phase: str) -> None:
    if len(rows) != len(entries):
        raise ValueError(f"{phase} row count {len(rows)} != {len(entries)}")
    expected_ids = [entry["probe_id"] for entry in entries]
    if [row.get("probe_id") for row in rows] != expected_ids:
        raise ValueError(f"{phase} row identities or order do not match the suite")
    if len(set(expected_ids)) != len(expected_ids):
        raise ValueError(f"{phase} suite identities are not unique")
    for row in rows:
        if row.get("status") not in TRANSPORT_STATUSES:
            raise ValueError(f"{phase} row has unknown transport status: {row.get('status')!r}")
        if not isinstance(row.get("tree_terminated"), bool):
            raise ValueError(f"{phase} row is missing tree_terminated")
        if not row["tree_terminated"]:
            raise ValueError(f"{phase} row is not tree-terminated")
        if bool(row.get("timed_out")) != (row.get("status") == "timeout"):
            raise ValueError(f"{phase} timeout status is inconsistent")
        if row.get("status") == "complete" and not isinstance(row.get("exit_code"), int):
            raise ValueError(f"{phase} complete row is missing an integer exit code")


def validate_attempts(attempts: list[dict]) -> list[str]:
    errors: list[str] = []
    if len(attempts) > CAP:
        errors.append("attempt count exceeds the 30-request cap")
    ids = [row.get("attempt_id") for row in attempts]
    expected_ids = [f"attempt-{index:04d}" for index in range(1, len(attempts) + 1)]
    if ids != expected_ids:
        errors.append("attempt identifiers are not sequential")
    completed_bodies: dict[str, str] = {}
    for row in attempts:
        attempt_id = row.get("attempt_id")
        expected_order = (
            int(attempt_id.split("-")[-1])
            if isinstance(attempt_id, str) and attempt_id.startswith("attempt-")
            and attempt_id.split("-")[-1].isdigit()
            else None
        )
        if row.get("generation_order") != expected_order:
            errors.append(f"{attempt_id}: generation order does not match identity")
        generation_status = row.get("generation_status")
        if generation_status not in GENERATION_STATUSES:
            errors.append(f"{attempt_id}: unknown generation status")
        execution_status = row.get("execution_status")
        if execution_status not in EXECUTION_STATUSES:
            errors.append(f"{attempt_id}: unknown execution status")
        if generation_status != "generated":
            if row.get("diagnostic") is not None or row.get("evaluation") is not None:
                errors.append(f"{attempt_id}: failed generation has host results")
            continue
        bid = row.get("body_id")
        if not isinstance(bid, str) or not re.fullmatch(r"[0-9a-f]{64}", bid):
            errors.append(f"{attempt_id}: missing or invalid body identity")
        screen = row.get("source_screen") or {}
        if not isinstance(screen.get("accepted"), bool):
            errors.append(f"{attempt_id}: missing source-screen result")
        if execution_status == "complete":
            if bid in completed_bodies:
                errors.append(f"{attempt_id}: duplicate body was executed twice")
            completed_bodies[bid] = attempt_id
            diag = row.get("diagnostic")
            ev = row.get("evaluation")
            if not isinstance(diag, dict) or not isinstance(ev, dict):
                errors.append(f"{attempt_id}: complete execution lacks host results")
                continue
            if diag.get("rows") != 30 or ev.get("rows") != 30:
                errors.append(f"{attempt_id}: incomplete host suites")
            if len(diag.get("probe_rows", [])) != 30 or len(ev.get("probe_rows", [])) != 30:
                errors.append(f"{attempt_id}: incomplete host row lists")
            if len(set(diag.get("probe_ids", []))) != 30 or len(set(ev.get("probe_ids", []))) != 30:
                errors.append(f"{attempt_id}: duplicate host probe identities")
            if diag.get("k") != diag.get("failed"):
                errors.append(f"{attempt_id}: diagnostic k is inconsistent")
            if ev.get("correct_count") != sum(1 for r in ev.get("probe_rows", []) if r.get("correct")):
                errors.append(f"{attempt_id}: evaluation correct count is inconsistent")
            expected_k = sum(1 for r in diag.get("probe_rows", []) if r.get("status") != "pass")
            if diag.get("k") != expected_k:
                errors.append(f"{attempt_id}: diagnostic k disagrees with rows")
            if row.get("eligible") and (diag.get("timed_out") or ev.get("timed_out")):
                errors.append(f"{attempt_id}: eligible body contains a timeout")
        elif execution_status == "duplicate_skipped":
            if not row.get("duplicate_of"):
                errors.append(f"{attempt_id}: duplicate lacks duplicate_of")
            if row.get("diagnostic") is not None or row.get("evaluation") is not None:
                errors.append(f"{attempt_id}: duplicate has host results")
        elif execution_status == "source_rejected":
            if screen.get("accepted") is not False:
                errors.append(f"{attempt_id}: source_rejected without a rejected screen")
            if row.get("diagnostic") is not None or row.get("evaluation") is not None:
                errors.append(f"{attempt_id}: rejected source has host results")
        elif execution_status == "runner_error":
            if not row.get("exclusion_reason"):
                errors.append(f"{attempt_id}: runner_error lacks a reason")
    return errors


def request_one(attempt_dir: Path, number: int) -> dict:
    """Make one provider request and retain every produced artifact."""
    response_path = attempt_dir / "generated-response.txt"
    key = os.environ.get("GEMINI_API_KEY")
    endpoint = f"https://{ENDPOINT_HOST}{ENDPOINT_PATH}"
    save_json(attempt_dir / "generation-request.json", {
        "provider": PROVIDER, "model": MODEL, "endpoint": endpoint,
        "generation_config": GENERATION_CONFIG,
        "prompt_sha256": sha256_text(PROMPT),
        "api_key_env": "GEMINI_API_KEY", "api_key_present": bool(key),
    })
    if not key:
        save_json(attempt_dir / "generation-error.json", {"error": "GEMINI_API_KEY is not configured"})
        (attempt_dir / "generation-stderr.txt").write_text(
            "GEMINI_API_KEY is not configured\n", encoding="utf-8")
        return {"status": "generation_failed", "failure_kind": "auth", "elapsed_seconds": 0.0,
                "http_status": None, "response_present": False}
    body = {
        "contents": [{"role": "user", "parts": [{"text": PROMPT}]}],
        "generationConfig": GENERATION_CONFIG,
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    started_at = datetime.now(timezone.utc)
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read()
        elapsed = time.perf_counter() - started
        finished_at = datetime.now(timezone.utc)
        payload = json.loads(raw.decode("utf-8"))
        (attempt_dir / "gemini-response.json").write_bytes(raw)
        text = extract_gemini_text(payload)
        candidate = (payload.get("candidates") or [{}])[0]
        finish_reason = candidate.get("finishReason")
        usage = payload.get("usageMetadata", {})
        save_json(attempt_dir / "generation-metadata.json", {
            "http_status": 200, "finish_reason": finish_reason, "usage": usage,
            "invoked_at_utc": started_at.isoformat(), "finished_at_utc": finished_at.isoformat(),
            "elapsed_seconds": elapsed,
        })
        if not text:
            prompt_block = payload.get("promptFeedback", {}).get("blockReason")
            reason = prompt_block or finish_reason or "empty response"
            failure_kind = "provider_block" if prompt_block else "other"
            (attempt_dir / "generation-stderr.txt").write_text(
                f"Gemini returned no text: {reason}\n", encoding="utf-8")
            return {"status": "generation_failed", "failure_kind": failure_kind,
                    "elapsed_seconds": elapsed, "http_status": 200, "response_present": False,
                    "finish_reason": finish_reason, "invoked_at_utc": started_at.isoformat(),
                    "finished_at_utc": finished_at.isoformat()}
        response_path.write_text(text, encoding="utf-8")
        if finish_reason != "STOP":
            (attempt_dir / "generation-stderr.txt").write_text(
                f"Gemini finishReason={finish_reason}\n", encoding="utf-8")
            return {"status": "generation_failed",
                    "failure_kind": "truncated" if finish_reason == "MAX_TOKENS" else "other",
                    "elapsed_seconds": elapsed, "http_status": 200, "response_present": True,
                    "finish_reason": finish_reason, "invoked_at_utc": started_at.isoformat(),
                    "finished_at_utc": finished_at.isoformat()}
        source = text
        (attempt_dir / "generated-solver.py").write_text(source, encoding="utf-8")
        screen = screen_source(source)
        screened = {
            "accepted": screen.accepted,
            "reasons": list(screen.reasons),
            "body_id": body_id(source),
            "source_bytes": len(source.encode("utf-8")),
        }
        save_json(attempt_dir / "source-screen.json", screened)
        return {"status": "generated", "elapsed_seconds": elapsed, "http_status": 200,
                "finish_reason": finish_reason, "usage": usage, "source": source,
                "screen": screened, "invoked_at_utc": started_at.isoformat(),
                "finished_at_utc": finished_at.isoformat()}
    except urllib.error.HTTPError as exc:
        elapsed = time.perf_counter() - started
        raw_error = exc.read().decode("utf-8", "replace")
        safe_error = redact_secret(raw_error, key)
        save_json(attempt_dir / "generation-error.json", {
            "http_status": exc.code, "reason": redact_secret(str(exc.reason), key),
            "body": safe_error[:4000], "invoked_at_utc": started_at.isoformat(),
        })
        (attempt_dir / "generation-stderr.txt").write_text(
            f"HTTP {exc.code}: {exc.reason}\n{safe_error[:2000]}\n", encoding="utf-8")
        return {"status": "generation_failed",
                "failure_kind": classify_http_failure(exc.code, safe_error),
                "elapsed_seconds": elapsed, "http_status": exc.code, "response_present": False,
                "invoked_at_utc": started_at.isoformat(),
                "finished_at_utc": datetime.now(timezone.utc).isoformat()}
    except urllib.error.URLError as exc:
        elapsed = time.perf_counter() - started
        safe_error = redact_secret(str(exc.reason), key)
        save_json(attempt_dir / "generation-error.json", {
            "error": safe_error, "invoked_at_utc": started_at.isoformat()})
        (attempt_dir / "generation-stderr.txt").write_text(safe_error + "\n", encoding="utf-8")
        return {"status": "generation_failed", "failure_kind": "network",
                "elapsed_seconds": elapsed, "http_status": None, "response_present": False,
                "invoked_at_utc": started_at.isoformat(),
                "finished_at_utc": datetime.now(timezone.utc).isoformat()}
    except TimeoutError:
        elapsed = time.perf_counter() - started
        save_json(attempt_dir / "generation-error.json", {
            "error": "timeout", "invoked_at_utc": started_at.isoformat()})
        (attempt_dir / "generation-stderr.txt").write_text(
            "Gemini request timed out\n", encoding="utf-8")
        return {"status": "generation_timeout", "failure_kind": "timeout",
                "elapsed_seconds": elapsed, "http_status": None, "response_present": False,
                "invoked_at_utc": started_at.isoformat(),
                "finished_at_utc": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        elapsed = time.perf_counter() - started
        safe_error = redact_secret(f"{type(exc).__name__}: {exc}", key)
        save_json(attempt_dir / "generation-error.json", {
            "error": safe_error, "invoked_at_utc": started_at.isoformat()})
        (attempt_dir / "generation-stderr.txt").write_text(safe_error + "\n", encoding="utf-8")
        return {"status": "generation_failed", "failure_kind": "other",
                "elapsed_seconds": elapsed, "http_status": None, "response_present": False,
                "invoked_at_utc": started_at.isoformat(),
                "finished_at_utc": datetime.now(timezone.utc).isoformat()}


def extract_gemini_text(payload: dict) -> str:
    parts = []
    for candidate in payload.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if part.get("thought"):
                continue
            if part.get("text"):
                parts.append(part["text"])
    return "".join(parts)


def classify_http_failure(code: int, body: str) -> str:
    text = body.lower()
    if code == 429 or any(marker in text for marker in PROVIDER_BLOCK_MARKERS):
        return "usage_limit"
    if code in (401, 403):
        return "auth"
    return "provider_error"


def execute_attempt(attempt_dir: Path, temp: Path, source: str, attempt_id: str,
                    diagnostic: list[dict], evaluation: list[dict],
                    execute_fn: Callable, runtime: Path) -> dict:
    diag_entries = guest_entries(diagnostic, "probe_id")
    eval_entries = guest_entries(evaluation, "hid")
    diag_meta = host_metadata(diagnostic, "probe_id")
    eval_meta = host_metadata(evaluation, "hid")
    suite_runner.PIPELINE = EXPRESSION_PIPELINE
    suite_runner.RUN = attempt_dir
    diag_transport, diag_wall = execute_fn(
        temp, f"diagnostic_{attempt_id}", f"diagnostic_{attempt_id}",
        diag_entries, source, runtime)
    validate_suite_rows(diag_transport["probe_rows"], diag_entries, "diagnostic")
    diag_rows = [
        expression_outcome(raw, entry, diag_meta[entry["probe_id"]], "diagnostic")
        for raw, entry in zip(diag_transport["probe_rows"], diag_entries, strict=True)
    ]
    eval_transport, eval_wall = execute_fn(
        temp, f"evaluation_{attempt_id}", f"holdout_{attempt_id}",
        eval_entries, source, runtime)
    validate_suite_rows(eval_transport["probe_rows"], eval_entries, "evaluation")
    eval_rows = [
        expression_outcome(raw, entry, eval_meta[entry["probe_id"]], "evaluation")
        for raw, entry in zip(eval_transport["probe_rows"], eval_entries, strict=True)
    ]
    diag = diagnostic_summary(diag_rows)
    ev = evaluation_summary(eval_rows)
    diag["suite_wall_seconds"] = diag_wall
    ev["suite_wall_seconds"] = eval_wall
    eligible = bool(
        diag["all_tree_terminated"]
        and ev["all_tree_terminated"]
        and not diag["timed_out"]
        and not ev["timed_out"]
    )
    return {"diagnostic": diag, "evaluation": ev, "eligible": eligible}


def summarize(attempts: list[dict]) -> dict:
    completed = [
        row for row in attempts
        if row.get("execution_status") == "complete" and row.get("eligible")
    ]
    by_body: dict[str, dict] = {}
    for row in completed:
        by_body.setdefault(row["body_id"], row)
    eligible = list(by_body.values())
    support: dict[int, dict[float, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in eligible:
        k = int(row["diagnostic"]["k"])
        c = float(row["diagnostic"]["C"])
        support[k][c].append(row)
    fixed_k_contrasts = []
    feasible = False
    for k in sorted(key for key in support if key > 0):
        groups = support[k]
        eligible_cs = {
            c: rows for c, rows in groups.items()
            if len({row["body_id"] for row in rows}) >= 2
        }
        if not eligible_cs:
            continue
        contrast_pairs = []
        for c1, c2 in combinations(sorted(eligible_cs), 2):
            counts1 = {row["body_id"]: row["evaluation"]["correct_count"] for row in eligible_cs[c1]}
            counts2 = {row["body_id"]: row["evaluation"]["correct_count"] for row in eligible_cs[c2]}
            contrast = (
                (any(v == 30 for v in counts1.values()) and any(v < 30 for v in counts2.values()))
                or (any(v == 30 for v in counts2.values()) and any(v < 30 for v in counts1.values()))
            )
            contrast_pairs.append({"C": [c1, c2], "evaluation_correct_counts": [counts1, counts2],
                                   "cross_C_contrast": contrast})
            feasible = feasible or contrast
        fixed_k_contrasts.append({
            "k": k,
            "C_values": sorted(eligible_cs),
            "distinct_bodies_by_C": {str(c): len({row["body_id"] for row in rows})
                                     for c, rows in eligible_cs.items()},
            "evaluation_correct_counts_by_C": {
                str(c): {row["body_id"]: row["evaluation"]["correct_count"] for row in rows}
                for c, rows in eligible_cs.items()
            },
            "cross_C_contrasts": contrast_pairs,
        })
    all_eligible_k = [int(row["diagnostic"]["k"]) for row in eligible]
    if feasible:
        missing = []
    elif not eligible:
        missing = ["NO_ELIGIBLE_BODIES"]
    elif all(k == 0 for k in all_eligible_k):
        missing = ["CEILING_NO_FAILURE_VARIATION"]
    elif not any(k > 0 for k in all_eligible_k):
        missing = ["NO_INCORRECT_BODIES"]
    elif not any(
        len({row["body_id"] for rows in support[k].values() for row in rows}) >= 2
        for k in support if k > 0
    ):
        missing = ["INCORRECT_BODIES_BUT_NO_REPEATED_K"]
    elif not any(
        len({c for c in support[k] if len({row["body_id"] for row in support[k][c]}) >= 2}) >= 2
        for k in support if k > 0
    ):
        missing = ["REPEATED_K_BUT_NO_C_SEPARATION"]
    else:
        missing = ["C_SEPARATION_WITHOUT_EVALUATION_SEPARATION"]
    return {
        "eligible_executed_bodies": len(eligible),
        "fixed_k_contrasts": fixed_k_contrasts,
        "support_by_k_C": {
            str(k): {
                str(c): {
                    "attempts": len(rows),
                    "distinct_bodies": len({row["body_id"] for row in rows}),
                    "evaluation_correct_counts": [row["evaluation"]["correct_count"] for row in rows],
                }
                for c, rows in groups.items()
            }
            for k, groups in sorted(support.items())
        },
        "feasibility_demonstrated": feasible,
        "missing_conditions": missing,
    }


def classify_state(summary: dict, halt_reason: str | None = None) -> str:
    if halt_reason:
        return "HALTED_GENERATION_AUTH" if "auth" in halt_reason.lower() else "HALTED_GENERATION_USAGE_LIMIT"
    if summary["feasibility_demonstrated"]:
        return "FEASIBILITY_OBSERVED"
    if not summary["eligible_executed_bodies"]:
        return "NO_ELIGIBLE_BODIES"
    return summary["missing_conditions"][0]


def render_report(result: dict) -> str:
    lines = [
        "# Expression pilot report", "",
        f"State: **{result['state']}**", "",
        f"Run: `{result['run_id']}`.",
        f"Generation requests: {result['generation_requests']}/{CAP}.",
        f"Model-written generation outputs: {result['model_written_generation_attempts']}; "
        f"generation failures: {result['generation_failures']}.",
        f"Distinct canonical bodies: {result['distinct_canonical_bodies']}.",
        f"Eligible executed bodies: {result['eligible_executed_bodies']}.",
        f"Feasibility demonstrated: {str(result['feasibility_demonstrated']).lower()}.",
        "", "Missing condition(s): " + ", ".join(result["missing_conditions"]), "",
        "## Bodies", "",
        "| Attempt | Body | k | C | Evaluation correct | Eligible |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in result["attempts"]:
        if row.get("diagnostic") and row.get("evaluation"):
            lines.append(
                f"| {row['attempt_id']} | `{row['body_id'][:12]}` | "
                f"{row['diagnostic']['k']} | {row['diagnostic']['C']:.3f} | "
                f"{row['evaluation']['correct_count']}/30 | {row.get('eligible')} |"
            )
    lines += ["", "## Fixed-k contrasts", ""]
    if result["fixed_k_contrasts"]:
        for row in result["fixed_k_contrasts"]:
            lines.append(
                f"- k={row['k']}: C={row['C_values']}; "
                f"bodies/C={row['distinct_bodies_by_C']}; "
                f"cross-C evaluation contrast={any(x['cross_C_contrast'] for x in row['cross_C_contrasts'])}."
            )
    else:
        lines.append("- None met the minimum support rule.")
    lines += [
        "", "No predictive model was fitted and no concentration effect was tested.",
        "", "The guest could read the other expressions in its current suite. "
        "Expected values, family labels, oracle code, and host records were not in the guest payload. "
        "Source screening is a best-effort policy, not a security boundary.",
        "", "This is an exploratory feasibility check on one declared generator procedure and task; "
        "it is not a confirmatory or prevalence claim.", "",
    ]
    return "\n".join(lines)


def run_pilot(run_dir: Path, generate_fn: Callable | None = None,
              execute_fn: Callable | None = None, attempt_cap: int = CAP,
              runtime: Path | None = None, commit_sha: str | None = None) -> dict:
    if attempt_cap < 1 or attempt_cap > CAP:
        raise ValueError(f"attempt_cap must be between 1 and {CAP}")
    strict_adapter_sha256 = validate_strict_adapter()
    diagnostic, evaluation, freeze = load_frozen_banks()
    preregistered = load_preregistered_prompt()
    if preregistered != PROMPT:
        raise RuntimeError("runner prompt does not match the preregistered prompt")
    generate_fn = generate_fn or request_one
    execute_fn = execute_fn or suite_runner.execute_suite
    if run_dir.exists():
        raise FileExistsError(run_dir)
    run_dir.mkdir(parents=True)
    (run_dir / "attempts").mkdir()
    (run_dir / "prompt.txt").write_text(PROMPT + "\n", encoding="utf-8")
    protocol = {
        "schema": 1,
        "run_id": run_dir.name,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "provider": PROVIDER,
        "model": MODEL,
        "endpoint": f"https://{ENDPOINT_HOST}{ENDPOINT_PATH}",
        "generation_config": GENERATION_CONFIG,
        "attempt_cap": CAP,
        "planned_attempts": attempt_cap,
        "prompt_sha256": sha256_text(PROMPT),
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "repository_commit": commit_sha,
        "prompt_matches_preregistration": True,
        "task_id": freeze["task_id"],
        "bank_hashes": {
            "diagnostic.json": freeze["diagnostic"]["sha256"],
            "evaluation.json": freeze["evaluation"]["sha256"],
            "FREEZE.json": sha256_file(FREEZE_PATH),
        },
        "guest_payload_fields": ["probe_id", "input.expr"],
        "expected_values_guest_visible": False,
        "output_contract": "exact int; type(value) is int",
        "wrong_return_type_scoring": "failed answer in the input family; not ineligible",
        "strict_adapter": "pipeline_expression_strict/python_adapter.py",
        "strict_adapter_sha256": strict_adapter_sha256,
        "no_retries": True,
        "no_replacement_sampling": True,
        "backend_snapshot": None,
        "backend_identity_note": "Backend snapshot/version is unavailable; no exact reproducibility claim.",
        "source_hashes": {},
    }
    for name, path in (
        ("run_expression_pilot.py", Path(__file__).resolve()),
        ("expression_task.py", ROOT / "expression_task.py"),
        ("source_policy.py", PILOT / "source_policy.py"),
        ("run_generated_smoke.py", PILOT / "run_generated_smoke.py"),
        ("integration_runner.py", PILOT / "integration_runner.py"),
        ("pipeline_expression_strict/python_adapter.py", EXPRESSION_PIPELINE / "python_adapter.py"),
        ("pipeline_expression_strict/sandbox_suite_supervisor.ps1",
         EXPRESSION_PIPELINE / "sandbox_suite_supervisor.ps1"),
        ("03_PILOT_PREREGISTRATION_2026-10-22.md", PROTOCOL_03),
        ("03A_PREREGISTRATION_AMENDMENT_2026-10-22.md", AMENDMENT_03A),
        ("03B_OUTPUT_CONTRACT_AMENDMENT_2026-10-22.md", AMENDMENT_03B),
        ("03C_PILOT_LAUNCH_PRECONDITIONS_2026-10-22.md", LAUNCH_PRECONDITIONS_03C),
    ):
        protocol["source_hashes"][name] = sha256_file(path)
    save_json(run_dir / "PROTOCOL.json", protocol)
    attempts: list[dict] = []
    seen_body: dict[str, str] = {}
    halt_reason = None
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="fc-expression-pilot-") as temporary:
        temp = Path(temporary)
        if runtime is None:
            runtime = temp / "python"
            shutil.copytree(
                suite_runner.previous.PYTHON_BASE, runtime,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for index in range(1, attempt_cap + 1):
            attempt_id = f"attempt-{index:04d}"
            attempt_dir = run_dir / "attempts" / attempt_id
            attempt_dir.mkdir()
            generated = generate_fn(attempt_dir, index)
            record = {
                "schema": 1,
                "attempt_id": attempt_id,
                "generation_order": index,
                "provider": PROVIDER,
                "model": MODEL,
                "prompt_sha256": sha256_text(PROMPT),
                "invoked_at_utc": generated.get("invoked_at_utc"),
                "finished_at_utc": generated.get("finished_at_utc"),
                "generation_elapsed_seconds": generated.get("elapsed_seconds"),
                "generation_http_status": generated.get("http_status"),
                "generation_finish_reason": generated.get("finish_reason"),
                "generation_status": generated["status"],
                "generation_failure_kind": generated.get("failure_kind"),
                "attempt_directory": str(attempt_dir.relative_to(run_dir)),
                "generated_response_path": str((attempt_dir / "generated-response.txt").relative_to(run_dir))
                if (attempt_dir / "generated-response.txt").is_file() else None,
                "generated_source_path": str((attempt_dir / "generated-solver.py").relative_to(run_dir))
                if (attempt_dir / "generated-solver.py").is_file() else None,
                "execution_status": "not_run",
                "diagnostic": None,
                "evaluation": None,
                "eligible": False,
                "exclusion_reason": None,
            }
            if generated["status"] != "generated":
                record["exclusion_reason"] = generated["status"]
                attempts.append(record)
                save_json(run_dir / "attempts.json", attempts)
                if generated.get("failure_kind") in {"auth", "usage_limit"}:
                    halt_reason = generated["failure_kind"]
                    break
                continue
            source = generated["source"]
            screen = generated["screen"]
            record["body_id"] = screen["body_id"]
            record["source_screen"] = {
                "accepted": screen["accepted"],
                "reasons": list(screen["reasons"]),
                "body_id": screen["body_id"],
                "source_bytes": screen["source_bytes"],
            }
            if screen["body_id"] in seen_body:
                record.update({
                    "execution_status": "duplicate_skipped",
                    "duplicate_of": seen_body[screen["body_id"]],
                    "exclusion_reason": "duplicate canonical body; retained without replacement sampling",
                })
                attempts.append(record)
                save_json(run_dir / "attempts.json", attempts)
                continue
            seen_body[screen["body_id"]] = attempt_id
            if not screen["accepted"]:
                record.update({
                    "execution_status": "source_rejected",
                    "exclusion_reason": list(screen["reasons"]),
                })
                attempts.append(record)
                save_json(run_dir / "attempts.json", attempts)
                continue
            try:
                host = execute_attempt(
                    attempt_dir, temp, source, attempt_id, diagnostic, evaluation, execute_fn, runtime)
                record.update({
                    "execution_status": "complete",
                    "diagnostic": host["diagnostic"],
                    "evaluation": host["evaluation"],
                    "eligible": host["eligible"],
                })
                save_json(attempt_dir / "host-authoritative" / "diagnostic.json", host["diagnostic"])
                save_json(attempt_dir / "host-authoritative" / "evaluation.json", host["evaluation"])
            except Exception as exc:
                record.update({
                    "execution_status": "runner_error",
                    "exclusion_reason": f"{type(exc).__name__}: {exc}",
                })
            attempts.append(record)
            save_json(run_dir / "attempts.json", attempts)
            diag = record.get("diagnostic")
            print(
                f"[{index}/{attempt_cap}] {record['execution_status']} "
                f"body={record.get('body_id')} "
                f"k={diag.get('k') if diag else None} C={diag.get('C') if diag else None}",
                flush=True)
    summary = summarize(attempts)
    errors = validate_attempts(attempts)
    if errors:
        save_json(run_dir / "VALIDATION_ERRORS.json", errors)
    state = classify_state(summary, halt_reason)
    if errors:
        state = "INTEGRITY_FAILURE"
    result = {
        "schema": 1,
        "run_id": run_dir.name,
        "state": state,
        "halt_reason": halt_reason,
        "planned_attempts": attempt_cap,
        "attempt_count": len(attempts),
        "generation_requests": len(attempts),
        "model_written_generation_attempts": sum(
            1 for row in attempts if row["generation_status"] == "generated"),
        "generation_failures": sum(
            1 for row in attempts if row["generation_status"] != "generated"),
        "source_rejected": sum(
            1 for row in attempts if row["execution_status"] == "source_rejected"),
        "duplicates": sum(
            1 for row in attempts if row["execution_status"] == "duplicate_skipped"),
        "runner_errors": sum(
            1 for row in attempts if row["execution_status"] == "runner_error"),
        "distinct_canonical_bodies": len({
            row["body_id"] for row in attempts if row.get("body_id")}),
        "eligible_executed_bodies": summary["eligible_executed_bodies"],
        "fixed_k_contrasts": summary["fixed_k_contrasts"],
        "support_by_k_C": summary["support_by_k_C"],
        "feasibility_demonstrated": summary["feasibility_demonstrated"],
        "missing_conditions": summary["missing_conditions"],
        "attempts": attempts,
        "validation_errors": errors,
        "predictive_model_fitted": False,
        "generation_elapsed_seconds": time.perf_counter() - started,
        "caveat": (
            "Exploratory feasibility only. Expected values and oracle data are host-side. "
            "The guest can read the other expressions in its current suite; the static screen "
            "is a best-effort policy, not a security boundary."
        ),
    }
    save_json(run_dir / "PILOT_RESULTS.json", {k: v for k, v in result.items() if k != "attempts"})
    (run_dir / "FEASIBILITY_REPORT.md").write_text(render_report(result), encoding="utf-8")
    if errors:
        raise RuntimeError(f"attempt validation failed: {errors}")
    return result


def preflight() -> dict:
    strict_adapter_sha256 = validate_strict_adapter()
    diagnostic, evaluation, freeze = load_frozen_banks()
    prompt = load_preregistered_prompt()
    if prompt != PROMPT:
        raise RuntimeError("runner prompt does not match the preregistered prompt")
    if not EXPRESSION_PIPELINE.is_dir():
        raise RuntimeError("expression Sandbox adapter directory is missing")
    screen_probes = {
        "eval": screen_source("def solve(expr):\n    return eval(expr)\n").reasons,
        "exec": screen_source("def solve(expr):\n    exec('x = 1')\n    return 1\n").reasons,
        "compile": screen_source("def solve(expr):\n    return compile(expr, '<x>', 'eval')\n").reasons,
        "open": screen_source("def solve(expr):\n    return open('x').read()\n").reasons,
        "os_import": screen_source("import os\ndef solve(expr):\n    return 1\n").reasons,
    }
    return {
        "status": "PASS",
        "no_model_calls": True,
        "generation_authorized": False,
        "prompt_sha256": sha256_text(PROMPT),
        "prompt_matches_preregistration": True,
        "task_id": freeze["task_id"],
        "bank_hashes": {
            "diagnostic.json": freeze["diagnostic"]["sha256"],
            "evaluation.json": freeze["evaluation"]["sha256"],
            "FREEZE.json": sha256_file(FREEZE_PATH),
        },
        "diagnostic_records": len(diagnostic),
        "evaluation_records": len(evaluation),
        "source_screen_probes": screen_probes,
        "guest_payload_fields": ["probe_id", "input.expr"],
        "expected_values_guest_visible": False,
        "output_contract": "exact int; type(value) is int",
        "strict_adapter": "pipeline_expression_strict/python_adapter.py",
        "strict_adapter_sha256": strict_adapter_sha256,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="make the 30 preregistered requests")
    parser.add_argument("--run-label", default=RUN_LABEL)
    parser.add_argument("--not-before", help="optional timezone-aware UTC not-before gate")
    args = parser.parse_args()
    report = preflight()
    if not args.execute:
        print(json.dumps(report, indent=2), flush=True)
        return
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("GEMINI_API_KEY is not configured")
    if args.not_before:
        not_before = parse_not_before(args.not_before)
        if datetime.now(timezone.utc) < not_before:
            raise ValueError(f"refusing to start before {not_before.isoformat()}")
    commit_sha = require_clean_launch_tree()
    label = validate_run_label(args.run_label)
    if not suite_runner.previous.SANDBOX.is_file() or not suite_runner.previous.PYTHON_BASE.is_dir():
        raise RuntimeError("Windows Sandbox or the Python runtime is unavailable")
    suite_runner.previous.check_no_running_sandbox()
    run_dir = ROOT / f"{label}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    result = run_pilot(run_dir, commit_sha=commit_sha)
    print(json.dumps({
        "run_dir": str(run_dir),
        "state": result["state"],
        "attempts": result["attempt_count"],
        "eligible_bodies": result["eligible_executed_bodies"],
        "feasibility_demonstrated": result["feasibility_demonstrated"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
