"""One authorized Codex solver smoke request and two suite-level Sandbox runs."""
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

REPO = Path(__file__).resolve().parents[1]
PILOT = Path(__file__).resolve().parent
PIPELINE = PILOT / "python-pipeline-integration"
sys.path.insert(0, str(PILOT)); sys.path.insert(0, str(REPO)); sys.path.insert(0, str(PIPELINE))

import run_python_pipeline_integration as previous
from integration_runner import CaptureRejected, parse_worker_scalar, validate_capture_directory
from pilot_tool import body_id, input_id
from source_policy import screen_source
from study.families import FAMILY_ORDER
from study.features import concentration, family_counts
from study.sssp import dijkstra_ref

PROMPT = ("Write one Python implementation of a function `solve(n, edges, s, t)` that computes the shortest path distance from node `s` to node `t` in a directed graph with non-negative integer edge weights. Nodes are integers `0` through `n-1`. `edges` is a list of `(u, v, w)` tuples; parallel edges and self-loops may occur. Return the minimum total weight of any directed path from `s` to `t` as an integer, or `-1` if `t` is unreachable. Make the function self-contained and use only the Python standard library. Do not read files, access the network, or print. Return only Python source code defining `solve`, with no Markdown fences, explanation, example usage, or tests. Write the first solution that comes to mind; do not self-review or revise it.")
CODEX_PS = Path.home() / "AppData/Local/JetBrains/PyCharm2026.2/acp-agents/codex-acp/2.2.2/node_modules/.bin/codex.ps1"
RUN = PILOT / "generation-smoke-2026-10-21"


def write_config(path: Path, inputs: Path, runner: Path, runtime: Path, output: Path,
                 nonce: str, case_id: str) -> None:
    command = ("powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass "
               f"-File C:\\fc-runner\\sandbox_suite_supervisor.ps1 -Nonce {nonce} "
               f"-CaseId {case_id} -TimeoutMs 10000")
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


def execute_suite(temp: Path, suite_name: str, case_id: str, entries: list[dict],
                  source: str, runtime: Path) -> tuple[dict, float]:
    output = RUN / "guest-captures" / suite_name
    output.mkdir(parents=True, exist_ok=False)
    input_dir = temp / f"inputs-{suite_name}"; runner_dir = temp / f"runner-{suite_name}"
    input_dir.mkdir(); runner_dir.mkdir()
    (input_dir / "suite.json").write_text(json.dumps({"requests": entries}, separators=(",", ":")), encoding="utf-8")
    shutil.copy2(PIPELINE / "python_adapter.py", runner_dir / "python_adapter.py")
    shutil.copy2(PIPELINE / "sandbox_suite_supervisor.ps1", runner_dir / "sandbox_suite_supervisor.ps1")
    (runner_dir / "solver.py").write_text(source, encoding="utf-8")
    nonce = uuid.uuid4().hex
    config = temp / f"{suite_name}.wsb"
    write_config(config, input_dir, runner_dir, runtime, output, nonce, case_id)
    process = subprocess.Popen([str(previous.SANDBOX), str(config)], creationflags=subprocess.CREATE_NO_WINDOW)
    started = time.perf_counter()
    capture = output / "capture.json"; guest_error = output / "guest-error.txt"
    deadline = time.monotonic() + 900
    while time.monotonic() < deadline:
        if capture.is_file() or guest_error.is_file():
            break
        time.sleep(0.2)
    else:
        raise TimeoutError(f"Sandbox suite did not produce a result: {suite_name}")
    while time.monotonic() < deadline and previous.session_pids(config):
        time.sleep(0.25)
    if previous.session_pids(config):
        raise TimeoutError(f"Sandbox suite did not close: {suite_name}")
    process.wait(timeout=10)
    elapsed = time.perf_counter() - started
    if guest_error.exists():
        raise RuntimeError(f"guest supervisor failed: {guest_error.read_text(errors='replace')}")
    transport = validate_capture_directory(output, nonce, case_id)
    expected_ids = [item["probe_id"] for item in entries]
    if [row["probe_id"] for row in transport["probe_rows"]] != expected_ids:
        raise CaptureRejected("capture rows do not match the input order")
    return transport, elapsed


def outcome(raw: dict, entry: dict, source: str, phase: str) -> dict:
    problem = entry["input"]
    oracle_raw = dijkstra_ref(problem["n"], [tuple(edge) for edge in problem["edges"]], problem["s"], problem["t"])
    oracle = -1 if oracle_raw is None else oracle_raw
    parsed = None; error = None; correct = False
    if raw["status"] == "complete" and raw["exit_code"] == 0 and not raw["timed_out"]:
        try:
            parsed = parse_worker_scalar(raw)
            correct = parsed == oracle
        except CaptureRejected as exc:
            error = str(exc)
    else:
        error = raw["status"]
    status = "pass" if correct else "wrong" if parsed is not None else "invalid" if raw["status"] == "complete" else raw["status"]
    return {"phase": phase, "probe_id": entry.get("probe_id") or entry.get("hid"), "family": entry.get("family"),
            "input_id": entry.get("input_id") or input_id(problem), "input": problem,
            "status": status, "solver_output": parsed, "oracle_output": oracle, "correct": correct,
            "error": error, "raw_stdout_b64": raw["stdout_b64"], "raw_stderr_b64": raw["stderr_b64"],
            "exit_code": raw["exit_code"], "timed_out": raw["timed_out"],
            "tree_terminated": raw["tree_terminated"], "worker_elapsed_ms": raw.get("elapsed_ms")}


def main() -> None:
    if RUN.exists():
        raise FileExistsError(RUN)
    if not previous.SANDBOX.is_file() or not previous.PYTHON_BASE.is_dir() or not CODEX_PS.is_file():
        raise RuntimeError("Codex CLI, Sandbox, or Python runtime is unavailable")
    previous.check_no_running_sandbox()
    RUN.mkdir(); (RUN / "guest-captures").mkdir(); (RUN / "host-authoritative").mkdir()
    (RUN / "prompt.txt").write_text(PROMPT + "\n", encoding="utf-8")
    (RUN / "generation-config.json").write_text(json.dumps({
        "date": "2026-10-21", "codex_cli_version": "0.160.1", "model_selector": "gpt-6-luna",
        "backend_version": None, "immutable_snapshot": None, "sampling_settings": "not exposed; defaults unavailable",
        "invocation": "codex exec --ephemeral --sandbox read-only --model gpt-6-luna --json --output-last-message <file>",
        "scope": "one trivial task smoke request, not a pilot attempt", "generation_inputs_exposed": False,
    }, indent=2) + "\n", encoding="utf-8")

    last = RUN / "generated-response.txt"
    command = ["powershell.exe", "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(CODEX_PS),
               "exec", "--ephemeral", "--sandbox", "read-only", "--model", "gpt-6-luna", "--json",
               "--output-last-message", str(last), "-C", str(RUN), PROMPT]
    generation_started = time.perf_counter()
    result = subprocess.run(command, capture_output=True, text=True, timeout=600, cwd=RUN)
    generation_seconds = time.perf_counter() - generation_started
    (RUN / "generation-events.jsonl").write_text(result.stdout, encoding="utf-8")
    (RUN / "generation-stderr.txt").write_text(result.stderr, encoding="utf-8")
    if result.returncode != 0 or not last.is_file():
        (RUN / "SMOKE_REPORT.md").write_text(f"# Generated solver smoke test\n\nStatus: **HOLD**. Codex CLI returned {result.returncode}; no solver was executed.\n", encoding="utf-8")
        raise SystemExit("generation smoke request failed; see retained smoke artifacts")
    source = last.read_text(encoding="utf-8")
    body_file = RUN / "generated-solver.py"; body_file.write_text(source, encoding="utf-8")
    screen = screen_source(source)
    screen_record = {"accepted": screen.accepted, "reasons": screen.reasons,
                     "body_id": body_id(source), "source_bytes": len(source.encode("utf-8"))}
    (RUN / "source-screen.json").write_text(json.dumps(screen_record, indent=2) + "\n", encoding="utf-8")
    if not screen.accepted:
        (RUN / "SMOKE_REPORT.md").write_text("# Generated solver smoke test\n\nStatus: **HOLD**. The returned source was rejected by the static policy screen; no Sandbox execution occurred.\n\n" + "\n".join(f"- {reason}" for reason in screen.reasons) + "\n", encoding="utf-8")
        raise SystemExit("source-policy screen rejected the generated response")

    diagnostic = json.loads((PILOT / "diagnostic_battery.json").read_text(encoding="utf-8"))
    evaluation = json.loads((PILOT / "evaluation_bank.json").read_text(encoding="utf-8"))
    if len({item["input_id"] for item in diagnostic}) != 30 or len({item["input_id"] for item in evaluation}) != 20 or {x["input_id"] for x in diagnostic} & {x["input_id"] for x in evaluation}:
        raise RuntimeError("existing diagnostic/evaluation input integrity failed")
    diag_requests = [{"probe_id": item["probe_id"], "input": item["input"]} for item in diagnostic]
    eval_requests = [{"probe_id": item["hid"], "input": item["input"]} for item in evaluation]
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="fc-suite-smoke-") as td:
        temp = Path(td); runtime = temp / "python"
        shutil.copytree(previous.PYTHON_BASE, runtime, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        diag_transport, diag_wall = execute_suite(temp, "diagnostic", "diagnostic_smoke", diag_requests, source, runtime)
        diag_records = [outcome(raw, item, source, "diagnostic") for raw, item in zip(diag_transport["probe_rows"], diagnostic, strict=True)]
        eval_transport, eval_wall = execute_suite(temp, "evaluation", "evaluation_smoke", eval_requests, source, runtime)
        eval_records = [outcome(raw, item, source, "evaluation") for raw, item in zip(eval_transport["probe_rows"], evaluation, strict=True)]
    failures = [record["status"] != "pass" for record in diag_records]
    counts = family_counts(failures); k, c = concentration(failures)
    (RUN / "host-authoritative" / "diagnostic.json").write_text(json.dumps({"rows": diag_records,
        "family_counts": counts, "family_order": FAMILY_ORDER, "k": k, "C": c}, indent=2) + "\n", encoding="utf-8")
    (RUN / "host-authoritative" / "evaluation.json").write_text(json.dumps(eval_records, indent=2) + "\n", encoding="utf-8")
    diag_times = [float(row.get("elapsed_ms", 0)) for row in diag_transport["probe_rows"]]
    eval_times = [float(row.get("elapsed_ms", 0)) for row in eval_transport["probe_rows"]]
    total_seconds = diag_wall + eval_wall
    estimated_100_seconds = 100 * (total_seconds + generation_seconds)
    report = {"status": "PASS" if len(diag_records) == 30 and len(eval_records) == 20 and all(r["tree_terminated"] for r in diag_records + eval_records) else "HOLD",
        "model_generation_attempts": 0, "separate_smoke_requests": 1, "body_id": body_id(source),
        "diagnostic_rows": len(diag_records), "evaluation_rows": len(eval_records), "family_counts": counts,
        "k": k, "C": c, "evaluation_correct": sum(r["correct"] for r in eval_records),
        "generation_seconds": generation_seconds, "diagnostic_suite_wall_seconds": diag_wall,
        "evaluation_suite_wall_seconds": eval_wall, "one_solver_50_input_seconds": total_seconds,
        "average_worker_ms": {"diagnostic": sum(diag_times) / max(1, len(diag_times)),
                              "evaluation": sum(eval_times) / max(1, len(eval_times))},
        "estimated_100_attempts_seconds": estimated_100_seconds,
        "estimated_100_attempts_hours": estimated_100_seconds / 3600,
        "estimated_100_assumption": "linear repetition of this one generation duration plus this one solver's 50-input Sandbox runtime; excludes contention and between-generation variation",
        "source_policy": screen_record, "input_visibility": "the full current suite is guest-readable in that suite's session; this is an explicitly accepted exploratory limitation; suites are separate",
        "networking_disabled": True, "project_and_credentials_mapped": False,
        "reference_oracle_mapped": False, "host_computed_labels_and_features": True}
    (RUN / "SMOKE_RESULTS.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    text = ["# Generated solver smoke test", "", f"Status: **{report['status']}**", "",
            f"Diagnostic: {len(diag_records)}/30 rows; family failures {counts}; k={k}; C={c}.",
            f"Evaluation: {len(eval_records)}/20 rows; correct {report['evaluation_correct']}/20.",
            f"One solver, 50 inputs: {total_seconds:.2f}s (diagnostic {diag_wall:.2f}s; evaluation {eval_wall:.2f}s).",
            f"Estimated 100 attempts: {estimated_100_seconds/3600:.2f} hours, linear estimate including one generation smoke duration.",
            f"Per-worker mean: diagnostic {report['average_worker_ms']['diagnostic']:.1f}ms; evaluation {report['average_worker_ms']['evaluation']:.1f}ms.",
            "", "This is a single generated smoke body, not a feasibility pilot attempt or evidence for the concentration hypothesis.",
            "The full input bank for each phase was visible to the guest during that phase. Static source screening is a best-effort filter, not a security boundary. The model prompt contained no test inputs.", ""]
    (RUN / "SMOKE_REPORT.md").write_text("\n".join(text), encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)
    if report["status"] != "PASS":
        raise SystemExit("full 50-input smoke evaluation incomplete")


if __name__ == "__main__":
    main()
