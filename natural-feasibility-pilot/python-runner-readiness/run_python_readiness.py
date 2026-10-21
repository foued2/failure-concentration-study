"""Run harmless Python/input-isolation controls in Windows Sandbox only."""
from __future__ import annotations

import base64
import hashlib
import html
import json
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path


HERE = Path(__file__).resolve().parent
PILOT = HERE.parent
REPO = PILOT.parent
BASE_PYTHON = Path.home() / "AppData/Roaming/uv/python/cpython-3.14-windows-x86_64-none"
SANDBOX = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32/WindowsSandbox.exe"
RUN = HERE / f"run-{time.strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:8]}"
OUTPUT_CAP = 65536


def check_no_running_sandbox() -> None:
    r = subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                        "@(Get-Process WindowsSandbox,WindowsSandboxRemoteSession -ErrorAction SilentlyContinue).Count"],
                       capture_output=True, text=True, check=True)
    if int(r.stdout.strip() or "0"):
        raise RuntimeError("Existing Sandbox session detected; refusing to disturb it")


def main() -> None:
    if not SANDBOX.is_file() or not BASE_PYTHON.is_dir():
        raise RuntimeError("Windows Sandbox or the configured Python base runtime is unavailable")
    check_no_running_sandbox()
    RUN.mkdir(parents=True, exist_ok=False)
    capture_dir = RUN / "guest-output"
    records_dir = RUN / "host-authoritative"
    capture_dir.mkdir(); records_dir.mkdir()
    with tempfile.TemporaryDirectory(prefix="fc-python-sbx-") as tmp:
        root = Path(tmp); guest_input = root / "input"; guest_python = root / "python"
        guest_input.mkdir()
        # Only one harmless current input and the fixture/supervisor are made
        # available. No project root, diagnostic battery, hidden bank, oracle,
        # or trusted records are copied into the guest.
        shutil.copy2(HERE / "python_worker_fixture.py", guest_input / "python_worker_fixture.py")
        shutil.copy2(HERE / "sandbox_python_supervisor.ps1", guest_input / "sandbox_python_supervisor.ps1")
        (guest_input / "current-input.json").write_text(json.dumps({"expected_answer": 42}), encoding="utf-8")
        shutil.copytree(BASE_PYTHON, guest_python, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        nonce = uuid.uuid4().hex
        config_path = root / "python-readiness.wsb"
        command = ("powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "
                   "C:\\fc-input\\sandbox_python_supervisor.ps1 -Nonce " + nonce)
        xml = f"""<Configuration>
  <VGpu>Disable</VGpu><Networking>Disable</Networking><ProtectedClient>Enable</ProtectedClient>
  <ClipboardRedirection>Disable</ClipboardRedirection><AudioInput>Disable</AudioInput><VideoInput>Disable</VideoInput>
  <PrinterRedirection>Disable</PrinterRedirection><MemoryInMB>2048</MemoryInMB>
  <MappedFolders>
    <MappedFolder><HostFolder>{html.escape(str(guest_input))}</HostFolder><SandboxFolder>C:\\fc-input</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
    <MappedFolder><HostFolder>{html.escape(str(guest_python))}</HostFolder><SandboxFolder>C:\\fc-python</SandboxFolder><ReadOnly>true</ReadOnly></MappedFolder>
    <MappedFolder><HostFolder>{html.escape(str(capture_dir))}</HostFolder><SandboxFolder>C:\\fc-output</SandboxFolder><ReadOnly>false</ReadOnly></MappedFolder>
  </MappedFolders><LogonCommand><Command>{html.escape(command)}</Command></LogonCommand>
</Configuration>"""
        config_path.write_text(xml, encoding="utf-8")
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in guest_input.iterdir()}
        proc = subprocess.Popen([str(SANDBOX), str(config_path)], creationflags=subprocess.CREATE_NO_WINDOW)
        capture = capture_dir / "python-capture.json"
        deadline = time.monotonic() + 300
        while time.monotonic() < deadline and not capture.exists():
            time.sleep(0.25)
        if not capture.is_file():
            raise TimeoutError("Python Sandbox did not write a capture within five minutes")
        # Wait for the exact Sandbox process group to close before reading its
        # writable mapping. The launched GUI exits before the guest does.
        while time.monotonic() < deadline:
            q = subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                                "@(Get-Process WindowsSandboxRemoteSession -ErrorAction SilentlyContinue).Count"],
                               capture_output=True, text=True, check=True)
            if int(q.stdout.strip() or "0") == 0:
                break
            time.sleep(0.5)
        else:
            raise TimeoutError("Sandbox session did not close after capture")
        proc.wait(timeout=5)
        unexpected = sorted(p.name for p in capture_dir.iterdir() if p.name != "python-capture.json")
        capture_bytes = capture.read_bytes()
        transport = json.loads(capture_bytes.decode("utf-8", errors="strict"))
        if transport.get("nonce") != nonce:
            raise AssertionError("Capture nonce mismatch")
        by_mode = {x["mode"]: x for x in transport["cases"]}
        expected_modes = {"normal", "access", "forge", "malformed", "oversized", "crash", "timeout_tree", "memory"}
        if set(by_mode) != expected_modes:
            raise AssertionError(f"Missing/extra cases: {set(by_mode) ^ expected_modes}")
        checks: list[dict] = []

        def add(name: str, passed: bool, detail: str) -> None:
            checks.append({"check": name, "result": "PASS" if passed else "FAIL", "detail": detail})

        raw = base64.b64decode(by_mode["normal"]["stdout_b64"], validate=True)
        add("python_runtime_and_current_input", by_mode["normal"]["status"] == "complete" and raw == b"42\r\n",
            f"status={by_mode['normal']['status']}, stdout={raw!r}")
        access = json.loads(base64.b64decode(by_mode["access"]["stdout_b64"], validate=True).decode("utf-8"))
        attempted_paths = [x["path"] for x in access["read_attempts"]]
        add("input_isolation", by_mode["access"]["status"] == "complete" and
            len(attempted_paths) == 6 and not access["readable_protected_paths"],
            json.dumps(access, sort_keys=True))
        forge = by_mode["forge"]
        forged_entries = set(transport.get("worker_visible_output_entries", []))
        add("guest_forgery_is_untrusted", forge["status"] == "complete" and
            {"python-capture.json", "forged-extra.json"}.issubset(forged_entries) and
            transport["nonce"] == nonce and len(transport["cases"]) == 8 and
            not (records_dir / "trusted-records.json").exists(),
            f"worker attempted the exact capture filename; supervisor replaced it with nonce-bound eight-case capture; host trusted records remained host-owned; worker files={sorted(forged_entries)}")
        malformed = base64.b64decode(by_mode["malformed"]["stdout_b64"], validate=True)
        add("malformed_output_retained_as_raw_untrusted_bytes", by_mode["malformed"]["status"] == "complete" and malformed == b"\xff\xfe\xfa\n",
            f"raw={malformed!r}; host does not parse it as a record")
        add("oversized_output_capped", by_mode["oversized"]["status"] == "overflow" and by_mode["oversized"]["overflow"] and
            len(base64.b64decode(by_mode["oversized"]["stdout_b64"], validate=True)) == 0,
            f"status={by_mode['oversized']['status']}; overflow={by_mode['oversized']['overflow']}; cap={OUTPUT_CAP}")
        add("crash_recorded", by_mode["crash"]["status"] == "crash" and by_mode["crash"]["exit_code"] not in (None, 0),
            f"status={by_mode['crash']['status']}; exit={by_mode['crash']['exit_code']}")
        timeout = by_mode["timeout_tree"]
        add("timeout_kills_entire_python_process_tree", timeout["timed_out"] and timeout["tree_terminated"] and timeout["status"] == "timeout",
            f"timed_out={timeout['timed_out']}; child_pid={timeout['child_pid']}; tree_terminated={timeout['tree_terminated']}")
        memory = by_mode["memory"]
        add("job_memory_limit_enforced", memory["status"] == "crash" and memory["exit_code"] not in (None, 0),
            f"status={memory['status']}; exit={memory['exit_code']}; job_limit=128 MiB; attempted=256 MiB")
        expected_guest_forgery = ["forged-extra.json"]
        add("guest_sidecar_detected_as_untrusted", unexpected == expected_guest_forgery,
            f"unexpected guest files={unexpected}; only the deliberate harmless forgery is expected")
        add("readonly_input_mount_unchanged", before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in guest_input.iterdir()},
            "Host-side input fixture hashes match after Sandbox exit")
        host_record = {"source": "host_reconstruction_from_untrusted_capture", "nonce": nonce,
                       "normal_fixture_expected_answer": 42, "normal_fixture_stdout": raw.decode("ascii", errors="strict").strip(),
                       "normal_fixture_correct": raw.strip() == b"42", "k": None, "C": None,
                       "note": "No diagnostic battery or oracle was mounted; this readiness check validates only transport and input visibility."}
        (records_dir / "host-authoritative-readiness.json").write_text(json.dumps(host_record, indent=2) + "\n", encoding="utf-8")
        summary = {"status": "PASS" if all(c["result"] == "PASS" for c in checks) else "BLOCKED",
                   "generation_attempts": 0, "solver_outcomes": 0, "checks": checks,
                   "sandbox_capture_sha256": hashlib.sha256(capture_bytes).hexdigest(),
                   "host_record_sha256": hashlib.sha256((records_dir / "host-authoritative-readiness.json").read_bytes()).hexdigest(),
                   "privacy_boundary": "single current input plus Python runtime and harmless fixture; no project, probes, evaluation inputs, oracle, or prior records mapped",
                   "runner_status": "pilot_not_authorized_by_this_check"}
        (RUN / "RESULTS.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        md = ["# Python Runner Readiness Check", "", f"Status: **{summary['status']}**", "",
              "No model-written solver was generated or executed. This used only harmless hand-built Python fixtures.", "",
              "| Check | Result | Evidence |", "|---|---|---|"]
        md.extend(f"| {c['check']} | {c['result']} | {c['detail'].replace('|', '\\|')} |" for c in checks)
        md += ["", "The Sandbox received one current test input, a read-only Python runtime and fixture, and a writable untrusted capture mount. It did not receive the repository, diagnostic battery, evaluation bank, oracle, or host authoritative records. Host-side records were written only after session closure.",
               "", "This validates the tested configuration and harmless fixtures only. It does not establish resistance to Sandbox escapes or validate a production diagnostic runner.",
               "", f"Generation attempts: **0**. Solver outcomes: **0**."]
        (RUN / "REPORT.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
