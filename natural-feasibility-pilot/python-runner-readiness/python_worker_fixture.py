"""Harmless Python controls for the Sandbox runner-readiness check only."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
import base64


def main() -> int:
    mode = sys.argv[1]
    wire = sys.stdin.buffer.readline().strip()
    if wire.startswith(b"\xef\xbb\xbf"):
        wire = wire[3:]
    request = json.loads(base64.b64decode(wire, validate=True).decode("utf-8"))
    if mode == "normal":
        print(request["expected_answer"])
        return 0
    if mode == "access":
        protected = [
            Path(r"C:\fc-input\diagnostic_battery.json"),
            Path(r"C:\fc-input\evaluation_bank.json"),
            Path(r"C:\fc-input\dijkstra_ref.py"),
            Path(r"C:\fc-input\trusted-records.json"),
            Path(r"C:\fc-output\trusted-records.json"),
            Path(r"C:\Users\pakla\PycharmProjects\failure-concentration-study\README.md"),
        ]
        attempts = []
        for candidate in protected:
            try:
                candidate.read_bytes()
                attempts.append({"path": str(candidate), "result": "READABLE"})
            except OSError as exc:
                attempts.append({"path": str(candidate), "result": type(exc).__name__})
        print(json.dumps({"read_attempts": attempts,
                          "readable_protected_paths": [x["path"] for x in attempts if x["result"] == "READABLE"]}))
        return 0
    if mode == "forge":
        output = Path(r"C:\fc-output")
        output.mkdir(exist_ok=True)
        (output / "python-capture.json").write_text('{"trusted":true,"k":999,"C":1}\n', encoding="utf-8")
        (output / "forged-extra.json").write_text('{"correct":true}\n', encoding="utf-8")
        print(request["expected_answer"])
        return 0
    if mode == "malformed":
        sys.stdout.buffer.write(b"\xff\xfe\xfa\n")
        return 0
    if mode == "oversized":
        sys.stdout.write("X" * 70000)
        return 0
    if mode == "crash":
        return 73
    if mode == "timeout_tree":
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
        Path(os.environ["FC_CHILD_PID_FILE"]).write_text(str(child.pid), encoding="ascii")
        time.sleep(120)
        return 0
    if mode == "memory":
        # The worker job caps this process tree; this request stays well below
        # the Sandbox's 2 GiB ceiling and is expected to exceed the 128 MiB job.
        bytearray(256 * 1024 * 1024)
        print("unexpected-allocation-success")
        return 0
    raise ValueError(f"unknown control mode: {mode}")


if __name__ == "__main__":
    raise SystemExit(main())
