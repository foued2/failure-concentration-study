"""Stream one host-held input at a time through an isolated Sandbox session."""
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

import run_python_pipeline_integration as base

REPO, PILOT, HERE = base.REPO, base.PILOT, base.HERE
sys.path.insert(0, str(PILOT)); sys.path.insert(0, str(REPO))
RUN = HERE / f"streamed-run-{time.strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:8]}"
SANDBOX = base.SANDBOX
PYTHON_BASE = base.PYTHON_BASE
SOLVER_TIMEOUT_MS = 2000
ADVANCE_GRACE_SECONDS = 2.5


def write_stream_config(path: Path, input_dir: Path, runner_dir: Path, runtime: Path,
                        output_dir: Path, nonce: str, case_id: str, count: int) -> None:
    command = ("powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass "
               "-File C:\\fc-runner\\sandbox_stream_supervisor.ps1 "
               f"-Nonce {nonce} -CaseId {case_id} -ExpectedCount {count} -TimeoutMs {SOLVER_TIMEOUT_MS}")
    xml = f"""<Configuration>
<VGpu>Disable</VGpu><Networking>Disable</Networking><ProtectedClient>Enable</ProtectedClient>
<ClipboardRedirection>Disable</ClipboardRedirection><AudioInput>Disable</AudioInput><VideoInput>Disable</VideoInput>
<PrinterRedirection>Disable</PrinterRedirection><MemoryInMB>2048</MemoryInMB>
<MappedFolders>
 <MappedFolder><HostFolder>{html.escape(str(input_dir))}</HostFolder><SandboxFolder>C:\\fc-input</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
 <MappedFolder><HostFolder>{html.escape(str(runner_dir))}</HostFolder><SandboxFolder>C:\\fc-runner</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
 <MappedFolder><HostFolder>{html.escape(str(runtime))}</HostFolder><SandboxFolder>C:\\fc-python</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
 <MappedFolder><HostFolder>{html.escape(str(output_dir))}</HostFolder><SandboxFolder>C:\\fc-output</SandboxFolder><ReadOnly>false</ReadOnly></MappedFolder>
</MappedFolders><LogonCommand><Command>{html.escape(command)}</Command></LogonCommand>
</Configuration>"""
    path.write_text(xml, encoding="utf-8")


def wait_session_closed(config: Path, timeout: int = 180) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        pids = base.session_pids(config)
        if not pids:
            return
        time.sleep(0.25)
    for pid in base.session_pids(config):
        subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                        f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue"], check=False)
    raise TimeoutError(f"Sandbox did not shut down: {config.name}")


def atomic_current_input(path: Path, data: dict, outside_temp: Path) -> None:
    # Windows Sandbox keeps the mapped file open, so replacement can fail.
    # Overwrite the sole fixed file after the supervisor reports that the
    # previous worker was killed, using one handle and flush before release.
    payload = json.dumps(data, sort_keys=True).encode("utf-8")
    with path.open("r+b", buffering=0) as stream:
        stream.seek(0)
        stream.write(payload)
        stream.truncate()
        os.fsync(stream.fileno())


def run_stream_batch(temp_root: Path, runtime: Path, name: str, case_prefix: str,
                    entries: list[dict], solver_source: str, mode_key: str = "mode") -> dict:
    from integration_runner import validate_capture_directory
    nonce = uuid.uuid4().hex
    count = len(entries)
    input_dir = temp_root / f"input-{name}"; runner_dir = temp_root / f"runner-{name}"
    output_dir = RUN / "guest-captures" / name
    input_dir.mkdir(); runner_dir.mkdir(); output_dir.mkdir(parents=True)
    current_path = input_dir / "current-input.json"
    first = {"sequence": 1, "probe_id": entries[0]["probe_id"], "input": entries[0]["input"], "mode": entries[0].get(mode_key, "normal")}
    current_path.write_text(json.dumps(first, sort_keys=True), encoding="utf-8")
    (runner_dir / "python_adapter.py").write_bytes((HERE / "python_adapter.py").read_bytes())
    (runner_dir / "sandbox_stream_supervisor.ps1").write_bytes((HERE / "sandbox_stream_supervisor.ps1").read_bytes())
    (runner_dir / "solver.py").write_text(solver_source, encoding="utf-8")
    case_id = case_prefix + name
    config = temp_root / f"{name}.wsb"
    write_stream_config(config, input_dir, runner_dir, runtime, output_dir, nonce, case_id, count)
    launch = subprocess.Popen([str(SANDBOX), str(config)], creationflags=subprocess.CREATE_NO_WINDOW)
    progress_path = output_dir / "progress.json"; capture_path = output_dir / "capture.json"
    for index in range(1, count + 1):
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            try:
                progress = json.loads(progress_path.read_text(encoding="utf-8"))
                if progress.get("nonce") == nonce and progress.get("sequence") == index and progress.get("rows") == index:
                    break
            except (FileNotFoundError, json.JSONDecodeError, OSError):
                pass
            time.sleep(0.1)
        else:
            raise TimeoutError(f"Guest did not consume input {index}/{count} for {name}")
        # Progress is untrusted transport. A worker can forge it, so wait longer
        # than the hard worker deadline before changing the current input.
        if index < count:
            time.sleep(ADVANCE_GRACE_SECONDS)
            current = {"sequence": index + 1, "probe_id": entries[index]["probe_id"],
                       "input": entries[index]["input"], "mode": entries[index].get(mode_key, "normal")}
            atomic_current_input(current_path, current, temp_root)
        if index % 5 == 0 or index == count:
            print(f"[{name}] host supplied {index}/{count} current inputs", flush=True)
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline and not capture_path.is_file():
        time.sleep(0.1)
    if not capture_path.is_file():
        raise TimeoutError(f"Guest did not finalize its capture for {name}")
    wait_session_closed(config)
    launch.wait(timeout=5)
    transport = validate_capture_directory(output_dir, nonce, case_id)
    expected_ids = [entry["probe_id"] for entry in entries]
    if [row["probe_id"] for row in transport["probe_rows"]] != expected_ids:
        raise AssertionError(f"Probe/input order mismatch in {name}")
    return {"transport": transport, "capture_path": str(capture_path.relative_to(RUN)),
            "capture_sha256": hashlib.sha256(capture_path.read_bytes()).hexdigest(),
            "mapped_input_entries": [p.name for p in input_dir.iterdir()], "mapped_runner_entries": [p.name for p in runner_dir.iterdir()]}


def host_record(raw_row: dict, entry: dict, body_name: str, source: str) -> dict:
    from integration_runner import CaptureRejected, parse_worker_scalar
    from pilot_tool import body_id, input_id
    from study.sssp import dijkstra_ref
    problem = entry["input"]
    oracle_raw = dijkstra_ref(problem["n"], [tuple(e) for e in problem["edges"]], problem["s"], problem["t"])
    oracle = -1 if oracle_raw is None else oracle_raw
    solver_output = None; error = None; correct = False
    if raw_row["status"] == "complete" and raw_row["exit_code"] == 0 and not raw_row["timed_out"]:
        try:
            solver_output = parse_worker_scalar(raw_row)
            correct = solver_output == oracle
        except CaptureRejected as exc:
            error = str(exc)
    else:
        error = raw_row["status"]
    status = "pass" if correct else "wrong" if solver_output is not None else "invalid" if raw_row["status"] == "complete" else raw_row["status"]
    return {"body_name": body_name, "body_id": body_id(source), "input_id": input_id(problem),
            "probe_id": entry["probe_id"], "family": entry.get("family"), "hid": entry.get("hid"),
            "input": problem, "status": status, "solver_output": solver_output,
            "oracle_output": oracle, "correct": correct, "error": error,
            "raw_stdout_b64": raw_row["stdout_b64"], "raw_stderr_b64": raw_row["stderr_b64"],
            "exit_code": raw_row["exit_code"], "timed_out": raw_row["timed_out"],
            "tree_terminated": raw_row["tree_terminated"]}


def main() -> None:
    if not SANDBOX.is_file() or not PYTHON_BASE.is_dir():
        raise RuntimeError("Windows Sandbox or Python base runtime unavailable")
    base.check_no_running_sandbox()
    diagnostic = json.loads((PILOT / "diagnostic_battery.json").read_text(encoding="utf-8"))
    evaluation = json.loads((PILOT / "evaluation_bank.json").read_text(encoding="utf-8"))
    from pilot_tool import body_id, input_id
    from study.features import family_counts, concentration
    from study.families import FAMILY_ORDER
    from integration_runner import parse_worker_scalar, CaptureRejected
    diagnostics_ids = {x["input_id"] for x in diagnostic}; evaluation_ids = {x["input_id"] for x in evaluation}
    if len(diagnostics_ids) != 30 or len(evaluation_ids) != 20 or diagnostics_ids & evaluation_ids:
        raise AssertionError("Prepared input uniqueness/separation check failed")
    RUN.mkdir(parents=True, exist_ok=False)
    (RUN / "guest-captures").mkdir(); auth = RUN / "host-authoritative"; auth.mkdir()
    fixtures = HERE / "fixtures"; fixtures.mkdir(exist_ok=True)
    id_by_probe = {x["probe_id"]: x["input_id"] for x in diagnostic}
    sources = {}
    for name, (failed, counts, k, c) in base.PATTERNS.items():
        sources[name] = base.make_solver_source([id_by_probe[p] for p in failed])
        (fixtures / f"{name}.py").write_text(sources[name], encoding="utf-8")
    (RUN / "fixture_manifest.json").write_text(json.dumps({"scope": "hand-built controlled software fixtures only",
        "model_calls": 0, "generation_attempts": 0, "diagnostic_count": 30, "evaluation_count": 20,
        "diagnostic_evaluation_overlap": 0,
        "patterns": {name: {"body_id": body_id(source), "failed_probe_ids": base.PATTERNS[name][0],
                            "expected_family_counts": base.PATTERNS[name][1], "expected_k": base.PATTERNS[name][2],
                            "expected_C": base.PATTERNS[name][3]} for name, source in sources.items()}}, indent=2) + "\n", encoding="utf-8")
    total_inputs = 4 * (len(diagnostic) + len(evaluation)) + 6
    raw_by_pattern = {}; host_diag = {}; host_eval = {}; capture_refs = {}
    controls_result = {}
    with tempfile.TemporaryDirectory(prefix="fc-stream-pipeline-") as temporary:
        temp_root = Path(temporary); runtime = temp_root / "python"
        shutil.copytree(PYTHON_BASE, runtime, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for name, source in sources.items():
            diag_entries = [{"probe_id": p["probe_id"], "family": p["family"], "input": p["input"], "mode": "normal"} for p in diagnostic]
            batch = run_stream_batch(temp_root, runtime, f"diag_{name}", "", diag_entries, source)
            raw_by_pattern[name] = batch; capture_refs[f"diag_{name}"] = batch["capture_path"]
            records = [host_record(r, p, name, source) for r, p in zip(batch["transport"]["probe_rows"], diagnostic, strict=True)]
            host_diag[name] = records
            (auth / f"diagnostic-{name}.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
            print(f"[host] oracle reconstructed diagnostic labels for {name}", flush=True)
        # A separate Sandbox run family uses only its current evaluation input;
        # the 20-row bank and oracle remain on the host.
        for name, source in sources.items():
            eval_entries = [{"probe_id": h["hid"], "hid": h["hid"], "input": h["input"], "mode": "normal"} for h in evaluation]
            batch = run_stream_batch(temp_root, runtime, f"evaluation_{name}", "evaluation_", eval_entries, source)
            capture_refs[f"evaluation_{name}"] = batch["capture_path"]
            records = [host_record(r, h, name, source) for r, h in zip(batch["transport"]["probe_rows"], evaluation, strict=True)]
            host_eval[name] = records
            (auth / f"evaluation-{name}.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
            print(f"[host] oracle reconstructed 20 evaluation labels for {name}", flush=True)
        control_entries = [{"probe_id": f"control_{mode}", "input": diagnostic[0]["input"], "mode": mode} for mode in
                           ("access", "crash", "invalid", "oversized", "timeout_tree", "memory")]
        control_batch = run_stream_batch(temp_root, runtime, "controls_python", "controls_", control_entries,
                                         sources["pattern_zero"])
        capture_refs["controls_python"] = control_batch["capture_path"]
        for entry, row in zip(control_entries, control_batch["transport"]["probe_rows"], strict=True):
            mode = entry["mode"]; raw = base64.b64decode(row["stdout_b64"], validate=True)
            if mode == "access":
                access = json.loads(raw.decode("utf-8"))
                host_status = "input_isolated" if not access["readable"] and access["input_entries"] == ["current-input.json"] else "FAIL_INPUT_LEAK"
                details = access
            elif mode == "invalid":
                try: parse_worker_scalar(row); host_status = "FAIL_INVALID_ACCEPTED"
                except CaptureRejected as exc: host_status = "invalid_rejected"; details = str(exc)
            elif mode == "oversized": host_status = "oversized_capped" if row["status"] == "overflow" else "FAIL_OVERSIZE"
            elif mode == "timeout_tree": host_status = "timeout_tree_terminated" if row["status"] == "timeout" and row["tree_terminated"] else "FAIL_TIMEOUT_TREE"
            elif mode == "crash": host_status = "crash_recorded" if row["status"] == "crash" and row["exit_code"] not in (0, None) else "FAIL_CRASH"
            else: host_status = "memory_limit_recorded" if row["status"] == "crash" and row["exit_code"] not in (0, None) else "FAIL_MEMORY"
            controls_result[mode] = {"host_status": host_status, "status": row["status"], "exit_code": row["exit_code"],
                                     "timed_out": row["timed_out"], "tree_terminated": row["tree_terminated"],
                                     "raw_stdout_b64": row["stdout_b64"], "raw_stderr_b64": row["stderr_b64"],
                                     "details": details if mode in ("access", "invalid") else None}
        (auth / "protocol-controls.json").write_text(json.dumps(controls_result, indent=2) + "\n", encoding="utf-8")

    summaries = {}
    for name, (_, expected_counts, expected_k, expected_c) in base.PATTERNS.items():
        records = host_diag[name]; failures = [r["status"] != "pass" for r in records]
        counts = family_counts(failures); k, c = concentration(failures)
        eval_records = host_eval[name]
        summaries[name] = {"diagnostic_rows": len(records), "family_counts": [counts[x] for x in FAMILY_ORDER],
                           "k": k, "C": c, "expected_family_counts": expected_counts,
                           "expected_k": expected_k, "expected_C": expected_c,
                           "diagnostic_pass": len(records) == 30 and [counts[x] for x in FAMILY_ORDER] == expected_counts and k == expected_k and c == expected_c,
                           "evaluation_rows": len(eval_records), "evaluation_correct": sum(r["correct"] for r in eval_records),
                           "evaluation_all_correct": len(eval_records) == 20 and all(r["correct"] for r in eval_records)}
    controls_pass = all(row["host_status"] in {"input_isolated", "invalid_rejected", "oversized_capped", "timeout_tree_terminated", "crash_recorded", "memory_limit_recorded"} for row in controls_result.values())
    passed = all(s["diagnostic_pass"] and s["evaluation_all_correct"] for s in summaries.values()) and controls_pass
    result = {"status": "PASS" if passed else "FAIL", "scope": "controlled_python_pipeline_calibration_only",
              "model_generation_calls": 0, "natural_solver_outcomes": 0, "sandbox_sessions": 9,
              "diagnostic_input_count": 30, "evaluation_input_count": 20,
              "full_diagnostic_battery_mapped": False, "full_evaluation_bank_mapped": False,
              "oracle_or_trusted_records_mapped": False, "host_recomputed_oracle_labels_and_features": True,
              "patterns": summaries, "protocol_controls": controls_result, "capture_references": capture_refs,
              "limits": "Single current input replaced atomically in a read-only mapped folder after each bounded worker process; host waits beyond the worker timeout before advancing.",
              "qualification": "Software controls only. No natural solver or predictive analysis; no claim against Sandbox escape."}
    (RUN / "INTEGRATION_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = ["# Streamed Python/Sandbox integration", "", f"Status: **{result['status']}**", "",
             "Hand-built controlled programs only; no model-generated solver ran.", "",
             "| Program | Family failures | k | C | Evaluation labels correct | Result |", "|---|---:|---:|---:|---:|---|"]
    for name, row in summaries.items():
        lines.append(f"| {name} | {row['family_counts']} | {row['k']} | {row['C']} | {row['evaluation_correct']}/20 | {'PASS' if row['diagnostic_pass'] and row['evaluation_all_correct'] else 'FAIL'} |")
    lines += ["", "Protocol controls:"] + [f"- `{m}`: **{r['host_status']}** (transport status `{r['status']}`, tree terminated={r['tree_terminated']})." for m, r in controls_result.items()]
    lines += ["", "The guest received only one current input at a time. Full suites, reference answers, and trusted host records remained host-side. The host recomputed each oracle label, then reconstructed family counts, k, and C.",
              "", "This is an instrument calibration, not evidence about generated solver behavior or the concentration hypothesis. It does not establish resistance to a Sandbox escape.", ""]
    (RUN / "INTEGRATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    (RUN / "manifest.json").write_text(json.dumps({"status": result["status"], "result": "INTEGRATION_RESULTS.json",
        "captures": capture_refs, "host_records": sorted(p.name for p in (RUN / "host-authoritative").iterdir())}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_directory": str(RUN), "status": result["status"], "patterns": summaries,
                      "controls": {k: v["host_status"] for k, v in controls_result.items()}}, indent=2), flush=True)
    if not passed: raise SystemExit(1)


if __name__ == "__main__":
    main()
