"""Record, reproducibly, whether this host can run Windows Sandbox.

The preflight and rendezvous gates cannot be marked PASS from a host that has no
Sandbox. This script writes the machine facts that justify leaving them NOT_RUN,
plus the exact failure of the launcher, so a reviewer can check the claim
instead of trusting a summary.

    python evidence/record_sandbox_availability.py
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V9 = HERE.parent
sys.path.insert(0, str(V9))

import backend  # noqa: E402


def powershell(expression: str) -> str:
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", expression],
            capture_output=True, text=True, timeout=120,
            encoding="utf-8", errors="replace",
        )
        return (proc.stdout or "").strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return f"<error: {type(exc).__name__}: {exc}>"


def main() -> int:
    exe = Path(os.environ.get("WINDIR", r"C:\Windows")) / "System32" / "WindowsSandbox.exe"
    launch_error = None
    try:
        backend.launch_sandbox(HERE / "nonexistent.wsb")
    except BaseException as exc:  # noqa: BLE001 - the point is to record it
        launch_error = f"{type(exc).__name__}: {exc}"

    report = {
        "recorded_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
        "host_identity": backend.current_identity(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "caption": powershell("(Get-CimInstance Win32_OperatingSystem).Caption"),
            "windows_sandbox_exe": str(exe),
            "windows_sandbox_exe_present": exe.is_file(),
            "hvhost_service": powershell("(Get-Service hvhost -ErrorAction SilentlyContinue).Status"),
            "vmcompute_service": powershell("(Get-Service vmcompute -ErrorAction SilentlyContinue).Status"),
            "hypervisor_present": powershell(
                "(Get-CimInstance Win32_ComputerSystem).HypervisorPresent"),
            "sandbox_packages": powershell(
                "(Get-ChildItem \"$env:WINDIR\\servicing\\Packages\" -Filter '*Sandbox*' "
                "-ErrorAction SilentlyContinue | Measure-Object).Count"),
        },
        "launch_attempt": launch_error,
        "conclusion": None,
        "sandbox_gates": ["sandbox_isolation_report", "sandbox_rendezvous_ordering",
                          "sandbox_agent_acceptance"],
    }
    present = report["platform"]["windows_sandbox_exe_present"]
    report["conclusion"] = (
        "Windows Sandbox is launchable on this host" if present
        else "Windows Sandbox is not available on this host: WindowsSandbox.exe is absent. "
             "The optional feature is present but disabled (see "
             "sandbox-capability-2026-10-28.json); enabling it requires an elevated session. "
             "The preflight and rendezvous cannot run here and their gates must stay NOT_RUN."
    )
    target = HERE / "sandbox-unavailable-2026-10-28.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
