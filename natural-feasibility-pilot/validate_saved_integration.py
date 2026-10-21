"""Revalidate a completed controlled Sandbox run and finalize its manifest."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from integration_runner import (CaptureRejected, parse_worker_scalar, reconstruct_host_record,
                                render_integration_report, validate_capture_directory,
                                validate_integration_report)
from study.probes import make_probe_suite
from study.sssp import dijkstra_ref


def validate_run(root: Path) -> dict:
    root = Path(root)
    records_path = root / "integration_records.json"
    records = json.loads(records_path.read_text(encoding="utf-8"))
    records["runner_scope"] = "hand_built_PowerShell_control_fixture_only"
    records["generic_python_solver_runner_validated"] = False
    records["generated_solver_execution_authorized"] = False
    if records.get("generated_solver_attempts") != 0 or records.get("natural_solver_outcomes") != 0:
        raise AssertionError("run must contain zero generated solvers and natural outcomes")
    probes = json.loads((root.parent.parent / "diagnostic_battery.json").read_text(encoding="utf-8"))
    expected_patterns = {
        "pattern_zero": ([0, 0, 0, 0, 0, 0], 0, 0.0),
        "pattern_one_family": ([4, 0, 0, 0, 0, 0], 4, 1.0),
        "pattern_two_families": ([2, 2, 0, 0, 0, 0], 4, 0.5),
        "pattern_four_families": ([1, 1, 1, 1, 0, 0], 4, 0.25),
    }
    manifest_rows = []
    for row in records["cases"]:
        case_id = row["case_id"]
        capture_dir = root / "captures" / case_id
        capture_path = capture_dir / "capture.json"
        if not capture_path.is_file():
            raise AssertionError(f"{case_id}: missing raw capture")
        raw = json.loads(capture_path.read_text(encoding="utf-8"))
        transport = None
        try:
            transport = validate_capture_directory(capture_dir, raw["nonce"], case_id)
        except CaptureRejected:
            if case_id != "fixture_unexpected_sidecar":
                raise
        if case_id in expected_patterns:
            if transport is None:
                raise AssertionError(f"{case_id}: valid capture rejected")
            rebuilt = reconstruct_host_record(transport, probes)
            saved_path = root / "authoritative" / f"{case_id}.json"
            saved = json.loads(saved_path.read_text(encoding="utf-8"))
            if saved != rebuilt:
                raise AssertionError(f"{case_id}: retained host record differs from independent reconstruction")
            counts, k, c = expected_patterns[case_id]
            if (list(rebuilt["family_counts"].values()), rebuilt["k"], rebuilt["C"]) != (counts, k, c):
                raise AssertionError(f"{case_id}: pattern mismatch")
        elif case_id.startswith("fixture_") and case_id != "fixture_unexpected_sidecar":
            if transport is None or len(transport["probe_rows"]) != 1:
                raise AssertionError(f"{case_id}: invalid single-probe fixture transport")
            worker = transport["probe_rows"][0]
            if case_id == "fixture_normal":
                actual = parse_worker_scalar(worker)
                p = probes[0]["input"]
                expected = dijkstra_ref(p["n"], [tuple(e) for e in p["edges"]], p["s"], p["t"])
                if actual != (-1 if expected is None else expected):
                    raise AssertionError("normal fixture disagrees with the reference oracle")
            elif case_id == "fixture_timeout_tree":
                if worker["status"] != "timeout" or not worker["tree_terminated"]:
                    raise AssertionError("timeout/tree fixture did not pass")
            elif case_id == "fixture_crash":
                if worker["status"] != "crash" or worker["exit_code"] == 0:
                    raise AssertionError("crash fixture did not pass")
            elif case_id in {"fixture_malformed", "fixture_oversized", "fixture_forged_claims"}:
                try:
                    parse_worker_scalar(worker)
                except CaptureRejected:
                    pass
                else:
                    raise AssertionError(f"{case_id}: unsafe stdout accepted")
        elif case_id == "fixture_unexpected_sidecar":
            if transport is not None:
                raise AssertionError("unexpected sidecar was accepted")
        else:
            raise AssertionError(f"unrecognized integration case {case_id}")

        row["capture_path"] = str(capture_path.relative_to(root))
        row["capture_sha256"] = hashlib.sha256(capture_path.read_bytes()).hexdigest()
        authoritative_path = root / "authoritative" / f"{case_id}.json"
        if authoritative_path.is_file():
            row["authoritative_path"] = str(authoritative_path.relative_to(root))
            row["authoritative_sha256"] = hashlib.sha256(authoritative_path.read_bytes()).hexdigest()
        manifest_rows.append({key: row[key] for key in ("case_id", "capture_path", "capture_sha256",
                                                       "authoritative_path", "authoritative_sha256") if key in row})
    if records["pass_count"] != records["case_count"] or records["case_count"] != len(records["cases"]):
        raise AssertionError("recorded test summary is inconsistent")
    records_path.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = render_integration_report(records)
    report_path = root / "INTEGRATION_REPORT.md"
    report_path.write_text(report, encoding="utf-8")
    validate_integration_report(records, report_path.read_text(encoding="utf-8"))
    manifest = {"status": records["status"], "records": manifest_rows,
                "runner_scope": records["runner_scope"],
                "generic_python_solver_runner_validated": False,
                "generated_solver_execution_authorized": False,
                "generated_solver_attempts": 0, "natural_solver_outcomes": 0}
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"cases": len(records["cases"]), "passed": records["pass_count"], "manifest_records": len(manifest_rows)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_saved_integration.py <run-directory>")
    print(json.dumps(validate_run(Path(sys.argv[1])), indent=2))
