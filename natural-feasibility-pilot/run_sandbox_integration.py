"""Run controlled-only Sandbox integration cases; never generates solver code."""
from __future__ import annotations

import html
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

from integration_runner import (CaptureRejected, parse_worker_scalar, reconstruct_host_record,
                                render_integration_report, validate_capture_directory,
                                validate_integration_report)
from study.sssp import dijkstra_ref

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
ARTIFACTS = ROOT / "integration-validation" / f"run-{time.strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:8]}"
PYTHON = Path(sys.executable)
BATTERY = ROOT / "diagnostic_battery.json"
SANDBOX_EXE = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "WindowsSandbox.exe"
CASE_SPECS = [
    ("fixture_normal", "", "normal", {"status": "complete", "expected_output": True}, True),
    ("pattern_zero", "", "normal", {"k": 0, "C": 0.0, "family_counts": [0, 0, 0, 0, 0, 0]}, True),
    ("pattern_one_family", "F1_0,F1_1,F1_2,F1_3", "normal", {"k": 4, "C": 1.0, "family_counts": [4, 0, 0, 0, 0, 0]}, True),
    ("pattern_two_families", "F1_0,F1_1,F2_0,F2_1", "normal", {"k": 4, "C": 0.5, "family_counts": [2, 2, 0, 0, 0, 0]}, True),
    ("pattern_four_families", "F1_0,F2_0,F3_0,F4_0", "normal", {"k": 4, "C": 0.25, "family_counts": [1, 1, 1, 1, 0, 0]}, True),
    ("fixture_timeout_tree", "", "timeout", {"status": "timeout", "tree_terminated": True}, True),
    ("fixture_crash", "", "crash", {"status": "crash"}, True),
    ("fixture_malformed", "", "malformed", {"reject_worker_output": True}, True),
    ("fixture_oversized", "", "oversized", {"reject_worker_output": True}, True),
    ("fixture_forged_claims", "", "forged", {"reject_worker_output": True}, True),
    ("fixture_unexpected_sidecar", "", "unexpected", {}, False),
]


def no_running_sandbox() -> None:
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", "@(Get-Process WindowsSandbox,WindowsSandboxRemoteSession -ErrorAction SilentlyContinue).Count"],
        capture_output=True, text=True, check=True,
    )
    if int(result.stdout.strip() or "0") != 0:
        raise RuntimeError("A Windows Sandbox session is already running; refusing to disturb it.")


def write_config(path: Path, guest_input: Path, guest_output: Path, case_id: str,
                 failure_ids: str, mode: str, nonce: str) -> None:
    cmd = (
        "powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass "
        "-File C:\\Users\\WDAGUtilityAccount\\Desktop\\pilot-input\\sandbox_supervisor.ps1 "
        f"-CaseId {case_id} -FailureIds {failure_ids or 'NONE'} -FixtureMode {mode} -Nonce {nonce} "
        f"-ProbeLimit {1 if case_id.startswith('fixture_') else 30}"
    )
    config = f"""<Configuration>
  <VGpu>Disable</VGpu><Networking>Disable</Networking><ProtectedClient>Enable</ProtectedClient>
  <ClipboardRedirection>Disable</ClipboardRedirection><AudioInput>Disable</AudioInput><VideoInput>Disable</VideoInput>
  <PrinterRedirection>Disable</PrinterRedirection><MemoryInMB>2048</MemoryInMB>
  <MappedFolders>
    <MappedFolder><HostFolder>{html.escape(str(guest_input))}</HostFolder><SandboxFolder>C:\\Users\\WDAGUtilityAccount\\Desktop\\pilot-input</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
    <MappedFolder><HostFolder>{html.escape(str(guest_output))}</HostFolder><SandboxFolder>C:\\Users\\WDAGUtilityAccount\\Desktop\\pilot-output</SandboxFolder><ReadOnly>false</ReadOnly></MappedFolder>
  </MappedFolders><LogonCommand><Command>{html.escape(cmd)}</Command></LogonCommand>
</Configuration>"""
    path.write_text(config, encoding="utf-8")


def run_guest(config: Path, capture_dir: Path) -> None:
    process = subprocess.Popen([str(SANDBOX_EXE), str(config)], creationflags=subprocess.CREATE_NO_WINDOW)
    capture = capture_dir / "capture.json"
    guest_error = capture_dir / "guest-error.txt"
    deadline = time.monotonic() + 240
    while time.monotonic() < deadline:
        if capture.exists():
            break
        if guest_error.exists():
            _wait_session_closed(config.name, 30)
            raise RuntimeError("Guest supervisor failed: " + guest_error.read_text(encoding="utf-8", errors="replace"))
        time.sleep(0.25)
    else:
        _stop_own_session(config.name)
        raise TimeoutError("Sandbox did not produce a capture within 240 seconds.")
    # The GUI launcher exits before the guest. Wait for this exact guest session,
    # not the front-end process, before reading its writable mount.
    _wait_session_closed(config.name, 45)
    process.wait(timeout=5)


def _session_pids(config_name: str) -> list[int]:
    escaped = config_name.replace("'", "''")
    command = ("@(Get-CimInstance Win32_Process -Filter \"Name='WindowsSandboxRemoteSession.exe'\" "
               f"| Where-Object {{$_.CommandLine -like '*{escaped}*'}} | ForEach-Object {{$_.ProcessId}}) -join ','")
    result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], capture_output=True, text=True, check=True)
    return [int(x) for x in result.stdout.strip().split(",") if x.strip()]


def _wait_session_closed(config_name: str, seconds: int) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if not _session_pids(config_name):
            return
        time.sleep(0.5)
    _stop_own_session(config_name)
    raise TimeoutError(f"Sandbox session {config_name} did not close within {seconds}s.")


def _stop_own_session(config_name: str) -> None:
    pids = _session_pids(config_name)
    for pid in pids:
        subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue"], check=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=[x[0] for x in CASE_SPECS], action="append")
    args = parser.parse_args()
    cases = [x for x in CASE_SPECS if not args.case or x[0] in args.case]
    if not SANDBOX_EXE.is_file():
        raise RuntimeError("Windows Sandbox executable is unavailable.")
    if ARTIFACTS.exists():
        raise RuntimeError(f"Refusing to overwrite existing integration artifacts: {ARTIFACTS}")
    no_running_sandbox()
    captures_root = ARTIFACTS / "captures"
    authoritative_root = ARTIFACTS / "authoritative"
    captures_root.mkdir(parents=True)
    authoritative_root.mkdir(parents=True)
    all_results: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="fc-pilot-sbx-") as temp:
        temp_root = Path(temp)
        guest_input = temp_root / "guest-input"
        guest_input.mkdir()
        # Deliberately exclude evaluation_bank.json and all expected labels.
        for filename in ("diagnostic_battery.json", "sandbox_supervisor.ps1", "sandbox_worker_fixture.ps1"):
            shutil.copyfile(ROOT / filename, guest_input / filename)
        for case_id, failure_ids, mode, expected, should_validate in cases:
            nonce = uuid.uuid4().hex
            capture_dir = captures_root / case_id
            capture_dir.mkdir()
            config = temp_root / f"{case_id}.wsb"
            write_config(config, guest_input, capture_dir, case_id, failure_ids, mode, nonce)
            run_guest(config, capture_dir)
            probes = json.loads(BATTERY.read_text(encoding="utf-8"))
            try:
                transport = validate_capture_directory(capture_dir, nonce, case_id)
                if case_id.startswith("fixture_"):
                    row = transport["probe_rows"][0]
                    if row["probe_id"] != "F1_0" or not row["tree_terminated"]:
                        raise AssertionError(f"{case_id}: probe identity or process-tree check failed")
                    if expected.get("status") and row["status"] != expected["status"]:
                        stderr = __import__("base64").b64decode(row["stderr_b64"]).decode("utf-8", errors="replace")
                        raise AssertionError(f"{case_id}: status={row['status']} expected {expected['status']}; stderr={stderr}")
                    if expected.get("expected_output"):
                        actual = parse_worker_scalar(row)
                        p = probes[0]["input"]
                        oracle = dijkstra_ref(p["n"], [tuple(e) for e in p["edges"]], p["s"], p["t"])
                        if actual != (-1 if oracle is None else oracle):
                            raise AssertionError(f"{case_id}: solver output {actual} disagrees with host oracle {oracle}")
                    if expected.get("reject_worker_output"):
                        try:
                            parse_worker_scalar(row)
                        except CaptureRejected as exc:
                            all_results.append({"case_id": case_id, "result": "PASS", "reason": f"unsafe stdout rejected: {exc}"})
                            continue
                        raise AssertionError(f"{case_id}: unsafe stdout was accepted")
                    all_results.append({"case_id": case_id, "result": "PASS", "reason": f"supervisor recorded {row['status']}; tree_terminated=true"})
                    continue
                result = reconstruct_host_record(transport, probes)
                if not should_validate:
                    raise AssertionError(f"{case_id}: malformed case was unexpectedly accepted")
                if expected.get("k") is not None and result["k"] != expected["k"]:
                    raise AssertionError(f"{case_id}: k={result['k']} expected {expected['k']}")
                if expected.get("C") is not None and result["C"] != expected["C"]:
                    raise AssertionError(f"{case_id}: C={result['C']} expected {expected['C']}")
                if expected.get("family_counts") is not None and list(result["family_counts"].values()) != expected["family_counts"]:
                    raise AssertionError(f"{case_id}: family counts mismatch: {result['family_counts']}")
                record_path = authoritative_root / f"{case_id}.json"
                record_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                all_results.append({"case_id": case_id, "result": "PASS", "reason": "host validation and expected behavior matched",
                                    "k": result["k"], "C": result["C"], "family_counts": list(result["family_counts"].values())})
            except CaptureRejected as exc:
                if should_validate:
                    raise
                all_results.append({"case_id": case_id, "result": "PASS", "reason": f"unsafe output rejected: {exc}"})
            if not should_validate and not any(r["case_id"] == case_id for r in all_results):
                raise AssertionError(f"{case_id}: required rejection was not recorded")

    report = {
        "status": "CONTROLLED_SANDBOX_INTEGRATION_ONLY",
        "runner_scope": "hand_built_PowerShell_control_fixture_only",
        "generic_python_solver_runner_validated": False,
        "generated_solver_execution_authorized": False,
        "generated_solver_attempts": 0,
        "natural_solver_outcomes": 0,
        "sandbox_sessions": len(cases),
        "evaluation_bank_mounted": False,
        "cases": all_results,
        "pass_count": sum(r["result"] == "PASS" for r in all_results),
        "case_count": len(all_results),
    }
    for row in all_results:
        case_dir = captures_root / row["case_id"]
        if (case_dir / "capture.json").is_file():
            row["capture_path"] = str((case_dir / "capture.json").relative_to(ARTIFACTS))
            row["capture_sha256"] = hashlib.sha256((case_dir / "capture.json").read_bytes()).hexdigest()
        host_record = authoritative_root / f"{row['case_id']}.json"
        if host_record.is_file():
            row["authoritative_path"] = str(host_record.relative_to(ARTIFACTS))
            row["authoritative_sha256"] = hashlib.sha256(host_record.read_bytes()).hexdigest()
    (ARTIFACTS / "integration_records.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    retained_report = json.loads((ARTIFACTS / "integration_records.json").read_text(encoding="utf-8"))
    report_path = ARTIFACTS / "INTEGRATION_REPORT.md"
    report_path.write_text(render_integration_report(retained_report), encoding="utf-8")
    validate_integration_report(retained_report, report_path.read_text(encoding="utf-8"))
    manifest = {"status": report["status"], "records": []}
    for row in all_results:
        manifest["records"].append({key: row[key] for key in ("case_id", "capture_path", "capture_sha256",
                                                               "authoritative_path", "authoritative_sha256") if key in row})
    (ARTIFACTS / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["pass_count"] != report["case_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
    ("fixture_normal", "", "normal", {"status": "complete", "expected_output": True}, True),
