from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.model import FAMILY_COUNT, concentration  # noqa: E402

PYTHON_BASE = Path.home() / "AppData/Roaming/uv/python/cpython-3.14-windows-x86_64-none"
SANDBOX = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32/WindowsSandbox.exe"
RUN = ROOT / "results" / "gate1-controls"
BANKS = ROOT / "banks"
CONTROLS = ROOT / "controls"
RUNNER = ROOT / "runner"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_powershell(command: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def check_no_running_sandbox() -> None:
    result = run_powershell(
        "@(Get-Process WindowsSandbox,WindowsSandboxRemoteSession -ErrorAction SilentlyContinue).Count"
    )
    if int(result.stdout.strip() or "0"):
        raise RuntimeError("an existing Sandbox session is running")


def session_pids(config_path: Path) -> list[int]:
    pattern = str(config_path).replace("'", "''")
    command = (
        "@(Get-CimInstance Win32_Process -Filter \"Name='WindowsSandboxRemoteSession.exe'\" "
        f"| Where-Object {{$_.CommandLine -like '*{pattern}*'}} | ForEach-Object {{$_.ProcessId}}) -join ','"
    )
    result = run_powershell(command)
    return [int(value) for value in result.stdout.strip().split(",") if value.strip()]


def write_config(
    path: Path,
    inputs: Path,
    runner: Path,
    runtime: Path,
    output: Path,
    nonce: str,
    case_id: str,
) -> None:
    command = (
        "powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass "
        "-File C:\\fc-runner\\sandbox_suite_supervisor.ps1 "
        f"-Nonce {nonce} -CaseId {case_id} -TimeoutMs 10000"
    )
    xml = f"""<Configuration>
<VGpu>Disable</VGpu><Networking>Disable</Networking><ProtectedClient>Enable</ProtectedClient>
<ClipboardRedirection>Disable</ClipboardRedirection><AudioInput>Disable</AudioInput><VideoInput>Disable</VideoInput>
<PrinterRedirection>Disable</PrinterRedirection><MemoryInMB>2048</MemoryInMB>
<MappedFolders>
 <MappedFolder><HostFolder>{html.escape(str(inputs))}</HostFolder><SandboxFolder>C:\\fc-input</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
 <MappedFolder><HostFolder>{html.escape(str(runner))}</HostFolder><SandboxFolder>C:\\fc-runner</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
 <MappedFolder><HostFolder>{html.escape(str(runtime))}</HostFolder><SandboxFolder>C:\\fc-python</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
 <MappedFolder><HostFolder>{html.escape(str(output))}</HostFolder><SandboxFolder>C:\\fc-output</SandboxFolder><ReadOnly>false</ReadOnly></MappedFolder>
</MappedFolders><LogonCommand><Command>{html.escape(command)}</Command></LogonCommand>
</Configuration>"""
    path.write_text(xml, encoding="utf-8")


def parse_transport(directory: Path, nonce: str, case_id: str, expected_ids: list[str]) -> dict[str, object]:
    entries = list(directory.iterdir())
    if len(entries) != 1 or entries[0].name != "capture.json":
        raise RuntimeError(f"unexpected guest output for {case_id}: {[entry.name for entry in entries]}")
    raw = entries[0].read_bytes()
    if len(raw) > 2 * 1024 * 1024:
        raise RuntimeError("capture exceeds byte limit")
    document = json.loads(raw.decode("utf-8", errors="strict"))
    if not isinstance(document, dict) or set(document) != {"schema", "nonce", "case_id", "probe_rows"}:
        raise RuntimeError("invalid capture envelope")
    if document["schema"] != 1 or document["nonce"] != nonce or document["case_id"] != case_id:
        raise RuntimeError("capture identity mismatch")
    rows = document["probe_rows"]
    if not isinstance(rows, list) or [row.get("probe_id") for row in rows] != expected_ids:
        raise RuntimeError("capture rows do not match suite order")
    for row in rows:
        if not isinstance(row, dict):
            raise RuntimeError("capture row is not an object")
        if row.get("status") not in {"complete", "timeout", "crash", "overflow"}:
            raise RuntimeError("unknown worker status")
        if row.get("tree_terminated") is not True:
            raise RuntimeError("worker tree termination not established")
        if not isinstance(row.get("stdout_b64"), str) or not isinstance(row.get("stderr_b64"), str):
            raise RuntimeError("capture output is not base64 text")
    return {"document": document, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def parse_int(row: dict[str, object]) -> int | None:
    if row["status"] != "complete" or row.get("exit_code") != 0 or row.get("timed_out"):
        return None
    raw = base64.b64decode(str(row["stdout_b64"]), validate=True)
    if len(raw) > 64 * 1024:
        raise ValueError("stdout exceeds limit")
    document = json.loads(raw.decode("utf-8", errors="strict"))
    if not isinstance(document, dict) or set(document) != {"return_type", "value"}:
        raise ValueError("adapter envelope has unexpected fields")
    if document["return_type"] != "int" or not isinstance(document["value"], str):
        raise ValueError("adapter did not return an exact int")
    token = document["value"]
    if not token or token.lstrip("-").isdigit() is False:
        raise ValueError("adapter int token is malformed")
    return int(token)


def execute_suite(
    temp: Path,
    suite_name: str,
    entries: list[dict[str, object]],
    source: str,
    runtime: Path,
    nonce: str,
    case_id: str,
) -> tuple[dict[str, object], float]:
    input_dir = temp / f"input-{suite_name}"
    runner_dir = temp / f"runner-{suite_name}"
    output = RUN / "guest-captures" / suite_name
    input_dir.mkdir()
    runner_dir.mkdir()
    output.mkdir(parents=True)
    (input_dir / "suite.json").write_text(
        json.dumps({"requests": entries}, separators=(",", ":")), encoding="utf-8"
    )
    for name in ("python_adapter.py", "sandbox_suite_supervisor.ps1"):
        shutil.copy2(RUNNER / name, runner_dir / name)
    (runner_dir / "solver.py").write_text(source, encoding="utf-8")
    config = temp / f"{suite_name}.wsb"
    write_config(config, input_dir, runner_dir, runtime, output, nonce, case_id)
    started = time.perf_counter()
    process = subprocess.Popen(
        [str(SANDBOX), str(config)], creationflags=subprocess.CREATE_NO_WINDOW
    )
    capture = output / "capture.json"
    guest_error = output / "guest-error.txt"
    deadline = time.monotonic() + 900
    while time.monotonic() < deadline:
        if capture.is_file() or guest_error.is_file():
            break
        time.sleep(0.2)
    while time.monotonic() < deadline and session_pids(config):
        time.sleep(0.25)
    if session_pids(config):
        for pid in session_pids(config):
            subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", f"Stop-Process -Id {pid} -Force"],
                check=False,
            )
        raise TimeoutError(f"Sandbox session did not close: {suite_name}")
    process.wait(timeout=10)
    elapsed = time.perf_counter() - started
    if guest_error.is_file():
        raise RuntimeError(f"guest supervisor failed: {guest_error.read_text(errors='replace')}")
    if not capture.is_file():
        raise RuntimeError(f"Sandbox produced no capture: {suite_name}")
    transport = parse_transport(output, nonce, case_id, [str(entry["probe_id"]) for entry in entries])
    return transport, elapsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", default="", help="run one control id")
    args = parser.parse_args()
    if RUN.exists():
        raise FileExistsError(f"refusing to overwrite {RUN}")
    if not SANDBOX.is_file():
        raise RuntimeError(f"Windows Sandbox not found: {SANDBOX}")
    if not PYTHON_BASE.is_dir():
        raise RuntimeError(f"Python runtime not found: {PYTHON_BASE}")
    check_no_running_sandbox()
    diagnostic = json.loads((BANKS / "diagnostic.json").read_text(encoding="utf-8"))
    evaluation = json.loads((BANKS / "evaluation.json").read_text(encoding="utf-8"))
    manifest = json.loads((CONTROLS / "MANIFEST.json").read_text(encoding="utf-8"))
    selected = json.loads((ROOT / "profiles" / "selected_profiles.json").read_text(encoding="utf-8"))
    entries = [
        {"probe_id": probe["probe_id"], "input": {"text": probe["text"]}}
        for probe in [*diagnostic["probes"], *evaluation["probes"]]
    ]
    if any("expected" in entry for entry in entries):
        raise AssertionError("expected values leaked into guest suite")
    controls = manifest["controls"]
    if args.only:
        controls = [control for control in controls if control["control_id"] == args.only]
        if not controls:
            raise SystemExit(f"unknown control: {args.only}")
    selected_by_id = {target["target_id"]: target for target in selected["targets"]}
    RUN.mkdir(parents=True)
    (RUN / "guest-captures").mkdir()
    started = time.perf_counter()
    records = []
    with tempfile.TemporaryDirectory(prefix="fc-engineered-controls-") as temporary:
        temp = Path(temporary)
        runtime = temp / "python"
        shutil.copytree(
            PYTHON_BASE, runtime, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
        )
        for control in controls:
            control_id = control["control_id"]
            source = (ROOT / control["path"]).read_text(encoding="utf-8")
            source_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
            if source_hash != control["source_sha256"]:
                raise RuntimeError(f"control source hash mismatch: {control_id}")
            nonce = uuid.uuid4().hex
            case_id = f"control_{control_id}"
            suite_name = f"{control_id.replace('_', '-')}-{uuid.uuid4().hex[:8]}"
            transport, wall = execute_suite(
                temp, suite_name, entries, source, runtime, nonce, case_id
            )
            rows = transport["document"]["probe_rows"]
            source_rows = [*diagnostic["probes"], *evaluation["probes"]]
            checked: list[dict[str, object]] = []
            failure_by_family = [0] * FAMILY_COUNT
            correct_evaluation = 0
            for row, probe in zip(rows, source_rows, strict=True):
                expected = int(probe["expected"])
                parsed = None
                error = None
                status = "execution"
                if row["status"] == "complete" and row.get("exit_code") == 0 and not row.get("timed_out"):
                    try:
                        parsed = parse_int(row)
                        status = "pass" if parsed == expected else "wrong"
                    except (ValueError, KeyError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                        error = str(exc)
                        status = "invalid"
                else:
                    error = row["status"]
                failed = status != "pass"
                if failed and probe["probe_id"].startswith("D"):
                    failure_by_family[int(probe["family_index"])] += 1
                if probe["probe_id"].startswith("E") and not failed:
                    correct_evaluation += 1
                checked.append({
                    "probe_id": probe["probe_id"],
                    "phase": "diagnostic" if probe["probe_id"].startswith("D") else "evaluation",
                    "family": probe["family"],
                    "family_index": probe["family_index"],
                    "text": probe["text"],
                    "expected": expected,
                    "solver_output": parsed,
                    "status": status,
                    "error": error,
                    "worker_status": row["status"],
                    "elapsed_ms": row.get("elapsed_ms"),
                })
            k, c = concentration(failure_by_family)
            evaluation_total = len(evaluation["probes"])
            s = correct_evaluation / evaluation_total
            target_id = control["target_id"]
            target = selected_by_id.get(target_id) if target_id else None
            record = {
                "control_id": control_id,
                "target_id": target_id,
                "source_sha256": source_hash,
                "target_profile": target["profile"] if target else None,
                "expected_diagnostic_vector": control["expected_diagnostic_vector"],
                "observed_diagnostic_vector": failure_by_family,
                "k": k,
                "C": c,
                "evaluation_correct": correct_evaluation,
                "evaluation_total": evaluation_total,
                "S": s,
                "diagnostic_pass": sum(failure_by_family) == 0,
                "profile_match": failure_by_family == control["expected_diagnostic_vector"],
                "all_rows_valid": all(row["status"] in {"pass", "wrong"} for row in checked),
                "wall_seconds": wall,
                "guest_capture_sha256": transport["sha256"],
                "guest_capture_bytes": transport["bytes"],
                "rows": checked,
            }
            write_json(RUN / f"{control_id}.json", record)
            records.append(record)
            print(f"{control_id}: vector={failure_by_family} k={k} C={c} S={s:.6f} wall={wall:.1f}s", flush=True)
    summary = {
        "schema": 1,
        "status": "GATE1_CONTROL_EXECUTION_COMPLETE",
        "model_calls": 0,
        "generated_solvers": 0,
        "control_count": len(records),
        "total_wall_seconds": time.perf_counter() - started,
        "sandbox": str(SANDBOX),
        "python_base": str(PYTHON_BASE),
        "bank_hashes": {
            "diagnostic.json": sha256_file(BANKS / "diagnostic.json"),
            "evaluation.json": sha256_file(BANKS / "evaluation.json"),
            "MANIFEST.json": sha256_file(BANKS / "MANIFEST.json"),
        },
        "runner_hashes": {
            "python_adapter.py": sha256_file(RUNNER / "python_adapter.py"),
            "sandbox_suite_supervisor.ps1": sha256_file(RUNNER / "sandbox_suite_supervisor.ps1"),
        },
        "controls": [
            {
                "control_id": record["control_id"],
                "target_id": record["target_id"],
                "observed_diagnostic_vector": record["observed_diagnostic_vector"],
                "k": record["k"],
                "C": record["C"],
                "S": record["S"],
                "profile_match": record["profile_match"],
                "all_rows_valid": record["all_rows_valid"],
                "guest_capture_sha256": record["guest_capture_sha256"],
            }
            for record in records
        ],
    }
    write_json(RUN / "SUMMARY.json", summary)
    print(json.dumps({"run": str(RUN), "controls": len(records), "status": summary["status"]}, indent=2))


if __name__ == "__main__":
    main()
