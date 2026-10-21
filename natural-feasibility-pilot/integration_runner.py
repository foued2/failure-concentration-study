"""Host-side validation for untrusted Sandbox diagnostic captures.

This module never executes solver source. It accepts only a bounded guest
transport envelope, re-checks every raw answer against the local reference
oracle, derives the six family counts and k/C, then returns host-owned rows.
"""
from __future__ import annotations

import json
import os
import stat
import sys
import argparse
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from study.features import concentration, family_counts
from study.families import FAMILY_ORDER
from study.sssp import dijkstra_ref

MAX_CAPTURE_BYTES = 2 * 1024 * 1024
MAX_SOLVER_STDOUT_BYTES = 64 * 1024
EXPECTED_FILENAME = "capture.json"
TRANSPORT_KEYS = {"schema", "nonce", "case_id", "probe_rows"}
ROW_KEYS = {"probe_id", "status", "exit_code", "timed_out", "tree_terminated", "stdout_b64", "stderr_b64"}
ROW_KEYS_WITH_TIMING = ROW_KEYS | {"elapsed_ms"}


class CaptureRejected(ValueError):
    """Untrusted transport failed a strict integrity check."""


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CaptureRejected(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_transport(raw: bytes, expected_nonce: str, expected_case_id: str) -> dict[str, Any]:
    if len(raw) > MAX_CAPTURE_BYTES:
        raise CaptureRejected("capture exceeds byte limit")
    try:
        doc = json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=_no_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CaptureRejected(f"invalid UTF-8/JSON: {exc}") from exc
    if not isinstance(doc, dict) or set(doc) != TRANSPORT_KEYS:
        raise CaptureRejected("transport has missing or unexpected top-level fields")
    if doc["schema"] != 1 or doc["nonce"] != expected_nonce or doc["case_id"] != expected_case_id:
        raise CaptureRejected("schema, nonce, or case identity mismatch")
    if expected_case_id.startswith("fixture_"):
        expected_rows = 1
    elif expected_case_id.startswith("evaluation_"):
        expected_rows = 20
    elif expected_case_id.startswith("controls_"):
        expected_rows = 6
    else:
        expected_rows = 30
    if not isinstance(doc["probe_rows"], list) or len(doc["probe_rows"]) != expected_rows:
        raise CaptureRejected(f"transport must contain exactly {expected_rows} probe rows")
    seen: set[str] = set()
    for row in doc["probe_rows"]:
        if not isinstance(row, dict) or frozenset(row) not in {frozenset(ROW_KEYS), frozenset(ROW_KEYS_WITH_TIMING)}:
            raise CaptureRejected("probe row has missing or unexpected fields")
        if "elapsed_ms" in row and (isinstance(row["elapsed_ms"], bool) or not isinstance(row["elapsed_ms"], (int, float)) or row["elapsed_ms"] < 0):
            raise CaptureRejected("elapsed_ms must be a non-negative number")
        if not isinstance(row["probe_id"], str) or row["probe_id"] in seen:
            raise CaptureRejected("probe identity is invalid or duplicated")
        seen.add(row["probe_id"])
        if row["status"] not in {"complete", "timeout", "crash", "overflow"}:
            raise CaptureRejected("unknown worker state")
        if not isinstance(row["timed_out"], bool):
            raise CaptureRejected("timed_out must be boolean")
        if not isinstance(row["tree_terminated"], bool) or not row["tree_terminated"]:
            raise CaptureRejected("worker process tree termination was not established")
        if not isinstance(row["stdout_b64"], str) or not isinstance(row["stderr_b64"], str):
            raise CaptureRejected("stdout/stderr captures must be base64 strings")
    return doc


def validate_capture_directory(directory: Path, expected_nonce: str, expected_case_id: str) -> dict[str, Any]:
    """Read a closed Sandbox output folder without following links/reparse points."""
    directory = Path(directory)
    try:
        root = directory.lstat()
    except FileNotFoundError as exc:
        raise CaptureRejected("capture directory is missing") from exc
    if not stat.S_ISDIR(root.st_mode) or _is_reparse(root):
        raise CaptureRejected("capture path is not a plain directory")
    entries = list(directory.iterdir())
    if len(entries) != 1 or entries[0].name != EXPECTED_FILENAME:
        raise CaptureRejected("unexpected or missing output file")
    path = entries[0]
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise CaptureRejected("capture file disappeared") from exc
    if not stat.S_ISREG(info.st_mode) or _is_reparse(info):
        raise CaptureRejected("capture is not a regular non-reparse file")
    if info.st_size > MAX_CAPTURE_BYTES:
        raise CaptureRejected("capture exceeds byte limit")
    return parse_transport(path.read_bytes(), expected_nonce, expected_case_id)


def _is_reparse(info: os.stat_result) -> bool:
    # Windows exposes FILE_ATTRIBUTE_REPARSE_POINT in st_file_attributes;
    # POSIX symlinks are rejected by the lstat file-type check above.
    attrs = getattr(info, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attrs & reparse_flag)


def reconstruct_host_record(transport: dict[str, Any], probes: list[dict]) -> dict[str, Any]:
    expected = {p["probe_id"]: p for p in probes}
    rows: list[dict[str, Any]] = []
    failures: list[bool] = []
    transport_by_id = {r["probe_id"]: r for r in transport["probe_rows"]}
    if set(transport_by_id) != set(expected):
        raise CaptureRejected("probe IDs differ from the frozen diagnostic battery")
    for probe in probes:
        item = transport_by_id[probe["probe_id"]]
        problem = probe.get("input", probe)
        variant = probe.get("variant")
        if variant is None:
            variant = int(str(probe["probe_id"]).rsplit("_", 1)[1])
        status = item["status"]
        output: int | None = None
        error: str | None = None
        failed = True
        if status == "overflow":
            raise CaptureRejected(f"{probe['probe_id']}: bounded stdout limit exceeded")
        if status == "complete" and not item["timed_out"] and item["exit_code"] == 0:
            try:
                output = parse_worker_scalar(item)
                oracle = dijkstra_ref(problem["n"], [tuple(e) for e in problem["edges"]], problem["s"], problem["t"])
                normalized = -1 if oracle is None else oracle
                failed = isinstance(output, bool) or output != normalized
            except (ValueError, UnicodeDecodeError) as exc:
                raise CaptureRejected(f"{probe['probe_id']}: malformed solver output: {exc}") from exc
        else:
            error = status if status != "complete" else "nonzero exit or timeout flag"
        failures.append(failed)
        rows.append({
            "probe_id": probe["probe_id"], "family": probe["family"],
            "variant": variant, "status": status,
            "solver_output": output, "error": error, "failed": failed,
        })
    counts = family_counts(failures)
    k, c = concentration(failures)
    if k != sum(counts.values()):
        raise AssertionError("host feature arithmetic mismatch")
    return {
        "source": "host_reconstructed_from_untrusted_raw_capture",
        "case_id": transport["case_id"], "probe_rows": rows,
        "family_counts": counts, "k": k, "C": c,
        "worker_claims_used": False,
    }


def parse_worker_scalar(row: dict[str, Any]) -> int:
    """Accept only a bounded, single ASCII integer from raw worker stdout."""
    import base64

    if row.get("status") == "overflow":
        raise CaptureRejected("bounded stdout limit exceeded")
    try:
        raw_output = base64.b64decode(row["stdout_b64"], validate=True)
        if len(raw_output) > MAX_SOLVER_STDOUT_BYTES:
            raise CaptureRejected("worker stdout exceeds byte limit")
        text = raw_output.decode("ascii", errors="strict")
    except (ValueError, UnicodeDecodeError, KeyError) as exc:
        raise CaptureRejected(f"malformed worker stdout: {exc}") from exc
    if text.endswith("\r\n"):
        token = text[:-2]
    elif text.endswith("\n"):
        token = text[:-1]
    else:
        token = text
    if not token or "\n" in token or "\r" in token or not token.lstrip("-").isdigit():
        raise CaptureRejected("worker output is not one strict integer")
    return int(token)


def render_integration_report(report: dict[str, Any]) -> str:
    """Render only values read from the retained integration-record object."""
    lines = ["# Sandbox integration calibration", "",
             "Controlled software fixtures only. No model-generated solver ran.", "",
             f"Cases passed: {report['pass_count']}/{report['case_count']}", "",
             "| Case | Result | Details |", "| --- | --- | --- |"]
    for row in report["cases"]:
        details = row.get("reason", "")
        if "k" in row:
            details += f"; family counts={row['family_counts']}; k={row['k']}; C={row['C']}"
        lines.append(f"| {row['case_id']} | {row['result']} | {details} |")
    lines += ["", "The guest's writable folder is untrusted transport. Host records are recomputed from raw output after the Sandbox session exits. This validates these fixtures and this execution path only; it does not establish resistance to a Sandbox escape or that arbitrary generated bodies can safely inspect only one input.", ""]
    lines[-2] = ("Scope limits: this used a hand-built PowerShell control worker, not a generic Python solver adapter. "
                 "The worker receives one probe over stdin but can also read the mapped diagnostic battery; "
                 "input isolation for model-written solver code is therefore NOT VERIFIED. The pilot is not ready "
                 "to execute generated solvers. The tested capture path does not claim resistance to Sandbox escape.")
    return "\n".join(lines)


def validate_integration_report(report: dict[str, Any], rendered: str) -> None:
    """Fail closed if any rendered report text differs from retained records."""
    expected = render_integration_report(report)
    if rendered != expected:
        raise AssertionError("integration report differs from its retained machine-readable records")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-dir", type=Path, required=True)
    parser.add_argument("--nonce", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--probes", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    args = parser.parse_args()
    probes = json.loads(args.probes.read_text(encoding="utf-8"))
    transport = validate_capture_directory(args.capture_dir, args.nonce, args.case_id)
    authoritative = reconstruct_host_record(transport, probes)
    args.record.parent.mkdir(parents=True, exist_ok=True)
    args.record.write_text(json.dumps(authoritative, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"case_id": authoritative["case_id"], "family_counts": authoritative["family_counts"],
                      "k": authoritative["k"], "C": authoritative["C"]}, sort_keys=True))


if __name__ == "__main__":
    main()
