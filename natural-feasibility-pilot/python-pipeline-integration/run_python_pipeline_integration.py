"""End-to-end controlled Python/Sandbox calibration; never calls a model."""
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

REPO = Path(__file__).resolve().parents[2]
PILOT = REPO / "natural-feasibility-pilot"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(PILOT))
sys.path.insert(0, str(REPO))
PYTHON_BASE = Path.home() / "AppData/Roaming/uv/python/cpython-3.14-windows-x86_64-none"
SANDBOX = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32/WindowsSandbox.exe"
RUN = HERE / f"run-{time.strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:8]}"
SEED = 20261020
OUTPUT_CAP = 65536
TIMEOUT_MS = 10000

PATTERNS = {
    "pattern_zero": ([], [0, 0, 0, 0, 0, 0], 0, 0.0),
    "pattern_one_family": (["F1_0", "F1_1", "F1_2", "F1_3"], [4, 0, 0, 0, 0, 0], 4, 1.0),
    "pattern_two_families": (["F1_0", "F1_1", "F2_0", "F2_1"], [2, 2, 0, 0, 0, 0], 4, 0.5),
    "pattern_four_families": (["F1_0", "F2_0", "F3_0", "F4_0"], [1, 1, 1, 1, 0, 0], 4, 0.25),
}


def check_no_running_sandbox() -> None:
    r = subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                        "@(Get-Process WindowsSandbox,WindowsSandboxRemoteSession -ErrorAction SilentlyContinue).Count"],
                       capture_output=True, text=True, check=True)
    if int(r.stdout.strip() or "0"):
        raise RuntimeError("An existing Sandbox session is running; refusing to disturb it")


def make_solver_source(fail_ids: list[str]) -> str:
    ids = json.dumps(sorted(fail_ids), separators=(",", ":"))
    return f'''"""Hand-built calibration solver; exact-input failure injection only."""
import hashlib, heapq, json
FAILURE_IDS = set({ids})
def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges: adj[u].append((v, w))
    dist = [10**30] * n; dist[s] = 0; q = [(0, s)]
    while q:
        d, u = heapq.heappop(q)
        if d != dist[u]: continue
        if u == t: break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]: dist[v] = nd; heapq.heappush(q, (nd, v))
    answer = -1 if dist[t] == 10**30 else dist[t]
    value = {{"n": n, "edges": edges, "s": s, "t": t}}
    key = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    if key in FAILURE_IDS: answer = 0 if answer == -1 else answer + 1
    return answer
'''


CONTROL_SOURCES = {
    "access": '''def solve(n, edges, s, t):\\n    return 0\\n''',
    "crash": '''def solve(n, edges, s, t):\n    raise RuntimeError("controlled crash")\n''',
    "invalid": '''def solve(n, edges, s, t):\n    return "not-an-integer"\n''',
    "oversized": '''def solve(n, edges, s, t):\n    return "X" * 70000\n''',
    "timeout_tree": '''import os, subprocess, sys, time\ndef solve(n, edges, s, t):\n    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])\n    with open(os.environ["FC_CHILD_PID_FILE"], "w", encoding="ascii") as f: f.write(str(child.pid))\n    time.sleep(120)\n    return 0\n''',
    "memory": '''def solve(n, edges, s, t):\n    bytearray(256 * 1024 * 1024)\n    return 0\n''',
}


def write_config(path: Path, guest_input: Path, guest_python: Path, guest_output: Path,
                 nonce: str, case_id: str, mode: str, timeout_ms: int) -> None:
    command = ("powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass "
               "-File C:\\fc-input\\sandbox_single_case_supervisor.ps1 "
               f"-Nonce {nonce} -CaseId fixture_{case_id} -Mode {mode} -TimeoutMs {timeout_ms}")
    xml = f"""<Configuration>
<VGpu>Disable</VGpu><Networking>Disable</Networking><ProtectedClient>Enable</ProtectedClient>
<ClipboardRedirection>Disable</ClipboardRedirection><AudioInput>Disable</AudioInput><VideoInput>Disable</VideoInput>
<PrinterRedirection>Disable</PrinterRedirection><MemoryInMB>2048</MemoryInMB>
<MappedFolders>
 <MappedFolder><HostFolder>{html.escape(str(guest_input))}</HostFolder><SandboxFolder>C:\\fc-input</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
 <MappedFolder><HostFolder>{html.escape(str(guest_python))}</HostFolder><SandboxFolder>C:\\fc-python</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
 <MappedFolder><HostFolder>{html.escape(str(guest_output))}</HostFolder><SandboxFolder>C:\\fc-output</SandboxFolder><ReadOnly>false</ReadOnly></MappedFolder>
</MappedFolders><LogonCommand><Command>{html.escape(command)}</Command></LogonCommand>
</Configuration>"""
    path.write_text(xml, encoding="utf-8")


def session_pids(config_path: Path) -> list[int]:
    pattern = str(config_path).replace("'", "''")
    command = ("@(Get-CimInstance Win32_Process -Filter \"Name='WindowsSandboxRemoteSession.exe'\" "
               f"| Where-Object {{$_.CommandLine -like '*{pattern}*'}} | ForEach-Object {{$_.ProcessId}}) -join ','")
    r = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], capture_output=True, text=True, check=True)
    return [int(x) for x in r.stdout.strip().split(",") if x.strip()]


def run_one(temp_root: Path, runtime: Path, inputs_root: Path, output_root: Path,
            case_id: str, problem: dict, solver_source: str, mode: str = "normal",
            timeout_ms: int = TIMEOUT_MS, ordinal: int = 0, total: int = 1) -> dict:
    nonce = uuid.uuid4().hex
    guest_input = inputs_root / case_id
    guest_output = output_root / case_id
    guest_input.mkdir()
    guest_output.mkdir()
    (guest_input / "current-input.json").write_text(json.dumps(problem, sort_keys=True), encoding="utf-8")
    (guest_input / "python_adapter.py").write_bytes((HERE / "python_adapter.py").read_bytes())
    (guest_input / "sandbox_single_case_supervisor.ps1").write_bytes((HERE / "sandbox_single_case_supervisor.ps1").read_bytes())
    (guest_input / "solver.py").write_text(solver_source, encoding="utf-8")
    config = temp_root / f"{case_id}.wsb"
    write_config(config, guest_input, runtime, guest_output, nonce, case_id, mode, timeout_ms)
    process = subprocess.Popen([str(SANDBOX), str(config)], creationflags=subprocess.CREATE_NO_WINDOW)
    capture_path = guest_output / "capture.json"
    error_path = guest_output / "guest-error.txt"
    deadline = time.monotonic() + 240
    while time.monotonic() < deadline:
        if capture_path.is_file(): break
        if error_path.is_file():
            break
        time.sleep(0.2)
    else:
        for pid in session_pids(config):
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue"], check=False)
        raise TimeoutError(f"Sandbox case produced no capture: {case_id}")
    while time.monotonic() < deadline and session_pids(config):
        time.sleep(0.25)
    if session_pids(config):
        for pid in session_pids(config):
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue"], check=False)
        raise TimeoutError(f"Sandbox session did not close: {case_id}")
    process.wait(timeout=5)
    if not capture_path.is_file():
        raise RuntimeError(f"Guest supervisor failed for {case_id}: {error_path.read_text(errors='replace') if error_path.exists() else 'no capture'}")
    from integration_runner import validate_capture_directory
    transport = validate_capture_directory(guest_output, nonce, f"fixture_{case_id}")
    row = transport["probe_rows"][0]
    if row["probe_id"] != "current-input":
        raise AssertionError(f"Unexpected single-input row for {case_id}")
    raw = base64.b64decode(row["stdout_b64"], validate=True)
    result = {"case_id": case_id, "nonce": nonce, "transport": row, "raw_stdout_b64": row["stdout_b64"],
              "raw_stderr_b64": row["stderr_b64"], "guest_capture_path": str(capture_path.relative_to(RUN)),
              "guest_capture_sha256": hashlib.sha256(capture_path.read_bytes()).hexdigest(),
              "input": problem, "mode": mode, "process_stdout_preview": raw[:256].decode("utf-8", errors="replace")}
    print(f"[{ordinal}/{total}] {case_id}: {row['status']}", flush=True)
    return result


def host_outcome(result: dict, problem: dict) -> dict:
    from integration_runner import CaptureRejected, parse_worker_scalar
    from study.sssp import dijkstra_ref
    row = result["transport"]
    oracle = dijkstra_ref(problem["n"], [tuple(e) for e in problem["edges"]], problem["s"], problem["t"])
    expected = -1 if oracle is None else oracle
    parsed = None
    error = None
    correct = False
    if row["status"] == "complete" and row["exit_code"] == 0 and not row["timed_out"]:
        try:
            parsed = parse_worker_scalar(row)
            correct = parsed == expected
        except CaptureRejected as exc:
            error = str(exc)
    else:
        error = row["status"]
    return {"input": problem, "oracle_output": expected, "solver_output": parsed,
            "correct": correct, "status": "pass" if correct else ("wrong" if parsed is not None else ("invalid" if error and row["status"] == "complete" else row["status"])),
            "error": error, "raw_stdout_b64": result["raw_stdout_b64"], "raw_stderr_b64": result["raw_stderr_b64"],
            "tree_terminated": row["tree_terminated"], "timed_out": row["timed_out"], "exit_code": row["exit_code"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="development cap; full run when omitted")
    args = parser.parse_args()
    if not SANDBOX.is_file() or not PYTHON_BASE.is_dir():
        raise RuntimeError("Windows Sandbox or Python base runtime unavailable")
    check_no_running_sandbox()
    diagnostic = json.loads((PILOT / "diagnostic_battery.json").read_text(encoding="utf-8"))
    evaluation = json.loads((PILOT / "evaluation_bank.json").read_text(encoding="utf-8"))
    from pilot_tool import input_id, body_id
    from study.features import family_counts, concentration
    from study.families import FAMILY_ORDER
    diag_ids = {r["input_id"] for r in diagnostic}; eval_ids = {r["input_id"] for r in evaluation}
    if len(diag_ids) != 30 or len(eval_ids) != 20 or diag_ids & eval_ids:
        raise AssertionError("Existing diagnostic/evaluation input uniqueness or separation failed")
    RUN.mkdir(parents=True, exist_ok=False)
    (RUN / "guest-captures").mkdir(); (RUN / "host-authoritative").mkdir(); (HERE / "fixtures").mkdir(exist_ok=True)
    ids_by_probe = {r["probe_id"]: r["input_id"] for r in diagnostic}
    body_sources: dict[str, str] = {}
    for name, (fail_probes, expected_counts, expected_k, expected_c) in PATTERNS.items():
        source = make_solver_source([ids_by_probe[x] for x in fail_probes])
        body_sources[name] = source
        (HERE / "fixtures" / f"{name}.py").write_text(source, encoding="utf-8")
    for mode, source in CONTROL_SOURCES.items():
        (HERE / "fixtures" / f"control_{mode}.py").write_text(source, encoding="utf-8")
    (RUN / "fixture_manifest.json").write_text(json.dumps({"status": "HAND_BUILT_SOFTWARE_CONTROLS_ONLY",
        "patterns": {name: {"failed_probe_ids": spec[0], "expected_family_counts": spec[1], "expected_k": spec[2], "expected_C": spec[3],
                             "body_id": body_id(body_sources[name])} for name, spec in PATTERNS.items()},
        "diagnostic_input_count": len(diagnostic), "evaluation_input_count": len(evaluation),
        "full_diagnostic_evaluation_overlap": 0, "model_calls": 0}, indent=2) + "\n", encoding="utf-8")

    # Each guest call gets exactly one current input. Both complete input suites,
    # oracle code, expected labels, and host records remain outside mapped folders.
    raw_diagnostics = {name: [] for name in PATTERNS}
    raw_evaluations = {name: [] for name in PATTERNS}
    outcome_diagnostics = {name: [] for name in PATTERNS}
    outcome_evaluations = {name: [] for name in PATTERNS}
    controls: dict[str, dict] = {}
    total = len(PATTERNS) * (len(diagnostic) + len(evaluation)) + len(CONTROL_SOURCES)
    if args.limit:
        total = min(total, args.limit)
    completed = 0
    with tempfile.TemporaryDirectory(prefix="fc-pipeline-temp-") as temp:
        temp_root = Path(temp); runtime = temp_root / "python"
        shutil.copytree(PYTHON_BASE, runtime, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        inputs_root = temp_root / "inputs"; inputs_root.mkdir()
        for name in PATTERNS:
            for item in diagnostic:
                if args.limit and completed >= args.limit: break
                case_id = f"diag-{name}-{item['probe_id']}"
                res = run_one(temp_root, runtime, inputs_root, RUN / "guest-captures", case_id,
                              item["input"], body_sources[name], ordinal=completed + 1, total=total)
                row = host_outcome(res, item["input"])
                row.update({"body_name": name, "body_id": body_id(body_sources[name]), "probe_id": item["probe_id"],
                            "family": item["family"], "input_id": item["input_id"], "raw_capture_path": res["guest_capture_path"]})
                raw_diagnostics[name].append(res); outcome_diagnostics[name].append(row); completed += 1
            if args.limit and completed >= args.limit: break
        if not (args.limit and completed >= args.limit):
            for name in PATTERNS:
                for item in evaluation:
                    if args.limit and completed >= args.limit: break
                    case_id = f"eval-{name}-{item['hid']}"
                    res = run_one(temp_root, runtime, inputs_root, RUN / "guest-captures", case_id,
                                  item["input"], body_sources[name], ordinal=completed + 1, total=total)
                    row = host_outcome(res, item["input"])
                    row.update({"body_name": name, "body_id": body_id(body_sources[name]), "hid": item["hid"],
                                "input_id": item["input_id"], "raw_capture_path": res["guest_capture_path"]})
                    raw_evaluations[name].append(res); outcome_evaluations[name].append(row); completed += 1
                if args.limit and completed >= args.limit: break
        if not (args.limit and completed >= args.limit):
            control_problem = diagnostic[0]["input"]
            control_timeout = 1200
            for mode in CONTROL_SOURCES:
                if args.limit and completed >= args.limit: break
                case_id = f"control-{mode}"
                res = run_one(temp_root, runtime, inputs_root, RUN / "guest-captures", case_id,
                              control_problem, CONTROL_SOURCES[mode], mode=mode,
                              timeout_ms=control_timeout if mode == "timeout_tree" else TIMEOUT_MS,
                              ordinal=completed + 1, total=total)
                row = res["transport"]
                if mode == "invalid":
                    try:
                        from integration_runner import parse_worker_scalar
                        parse_worker_scalar(row)
                        host_status = "FAIL_ACCEPTED_INVALID"
                    except Exception:
                        host_status = "invalid_rejected"
                elif mode == "oversized": host_status = "oversized_rejected" if row["status"] == "overflow" else "FAIL_NOT_OVERFLOW"
                elif mode == "timeout_tree": host_status = "timeout_tree_terminated" if row["status"] == "timeout" and row["tree_terminated"] else "FAIL_TIMEOUT_TREE"
                elif mode == "crash": host_status = "crash_recorded" if row["status"] == "crash" and row["exit_code"] not in (None, 0) else "FAIL_CRASH"
                elif mode == "memory": host_status = "memory_limit_recorded" if row["status"] == "crash" and row["exit_code"] not in (None, 0) else "FAIL_MEMORY"
                else: host_status = "observed"
                controls[mode] = {"host_status": host_status, "transport": row, "raw_capture_path": res["guest_capture_path"],
                                  "input_id": input_id(control_problem), "tree_terminated": row["tree_terminated"]}
                completed += 1

    summaries = {}
    for name, (_, expected_counts, expected_k, expected_c) in PATTERNS.items():
        records = outcome_diagnostics[name]
        fails = [r["status"] != "pass" for r in records]
        counts = family_counts(fails); k, c = concentration(fails)
        summaries[name] = {"diagnostic_rows": len(records), "family_counts": [counts[f] for f in FAMILY_ORDER],
                           "k": k, "C": c, "expected_family_counts": expected_counts,
                           "expected_k": expected_k, "expected_C": expected_c,
                           "pattern_pass": len(records) == 30 and [counts[f] for f in FAMILY_ORDER] == expected_counts and k == expected_k and c == expected_c,
                           "evaluation_rows": len(outcome_evaluations[name]),
                           "evaluation_correct_count": sum(r["correct"] for r in outcome_evaluations[name]),
                           "evaluation_all_pass": len(outcome_evaluations[name]) == 20 and all(r["correct"] for r in outcome_evaluations[name])}
        (RUN / "host-authoritative" / f"diagnostic-{name}.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        (RUN / "host-authoritative" / f"evaluation-{name}.json").write_text(json.dumps(outcome_evaluations[name], indent=2) + "\n", encoding="utf-8")
    (RUN / "host-authoritative" / "protocol-controls.json").write_text(json.dumps(controls, indent=2) + "\n", encoding="utf-8")
    all_complete = completed == total and all(s["pattern_pass"] and s["evaluation_all_pass"] for s in summaries.values())
    controls_pass = all(c["host_status"] in {"invalid_rejected", "oversized_rejected", "timeout_tree_terminated", "crash_recorded", "memory_limit_recorded"} for c in controls.values())
    report = {"status": "PASS" if all_complete and controls_pass else "FAIL_OR_INCOMPLETE",
              "scope": "controlled_python_software_calibration_only", "model_generated_code_executed": False,
              "generation_attempts": 0, "solver_outcomes": 0, "sandbox_sessions": completed,
              "diagnostic_inputs_per_pattern": len(diagnostic), "evaluation_inputs_per_pattern": len(evaluation),
              "worker_mapped_full_diagnostic_battery": False, "worker_mapped_full_evaluation_bank": False,
              "worker_mapped_oracle_or_host_records": False, "host_computed_oracle_and_features": True,
              "patterns": summaries, "protocol_controls": controls,
              "qualification": "This tests controlled fixture behavior and the measured boundary. It does not test natural solvers, predictive value, or resistance to Sandbox escapes."}
    (RUN / "INTEGRATION_RESULTS.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# End-to-end Python/Sandbox calibration", "", f"Status: **{report['status']}**", "",
             "Controlled hand-built fixtures only. No model-generated code ran.", "",
             "| Python fixture | Diagnostic counts | k | C | Evaluation correct | Result |", "|---|---:|---:|---:|---:|---|"]
    for name, x in summaries.items():
        lines.append(f"| {name} | {x['family_counts']} | {x['k']} | {x['C']} | {x['evaluation_correct_count']}/20 | {'PASS' if x['pattern_pass'] and x['evaluation_all_pass'] else 'FAIL'} |")
    lines += ["", f"Sandbox calls: {completed}. Each guest received one current input only; the complete diagnostic battery, evaluation bank, oracle, and host records were never mapped.",
              "", "Protocol controls:", ""]
    for mode, result in controls.items(): lines.append(f"- `{mode}`: **{result['host_status']}**; tree terminated={result['tree_terminated']}.")
    lines += ["", "Host-side oracle outputs, correctness labels, six family counts, k, and C were computed outside the guest. These controls do not establish a natural-solver effect or resistance to a Sandbox escape.", ""]
    (RUN / "INTEGRATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    manifest = {"run_id": RUN.name, "result_file": "INTEGRATION_RESULTS.json", "status": report["status"],
                "capture_count": len(list((RUN / "guest-captures").glob("*/capture.json"))),
                "host_records": [p.name for p in (RUN / "host-authoritative").iterdir()]}
    (RUN / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_directory": str(RUN), "status": report["status"], "completed": completed,
                      "patterns": summaries, "controls": {k: v["host_status"] for k, v in controls.items()}}, indent=2), flush=True)
    if report["status"] != "PASS": raise SystemExit(1)


if __name__ == "__main__":
    main()
