"""Guest-side adapter. Receives one graph on stdin; no suite data is present."""
from __future__ import annotations

import base64
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    wire = sys.stdin.buffer.readline().strip()
    if wire.startswith(b"\xef\xbb\xbf"):
        wire = wire[3:]
    request = json.loads(base64.b64decode(wire, validate=True).decode("utf-8"))
    mode = request.get("mode", "normal")
    if mode == "access":
        protected = [
            Path(r"C:\fc-input\diagnostic_battery.json"),
            Path(r"C:\fc-input\evaluation_bank.json"),
            Path(r"C:\fc-runner\dijkstra_ref.py"),
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
        entries = sorted(p.name for p in Path(r"C:\fc-input").iterdir())
        sys.stdout.write(json.dumps({"read_attempts": attempts, "readable": [x["path"] for x in attempts if x["result"] == "READABLE"], "input_entries": entries}) + "\n")
        return 0
    if mode == "crash":
        raise RuntimeError("controlled crash")
    if mode == "invalid":
        sys.stdout.write("not-an-integer\n")
        return 0
    if mode == "oversized":
        sys.stdout.write("X" * 70000)
        return 0
    if mode == "timeout_tree":
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
        Path(os.environ["FC_CHILD_PID_FILE"]).write_text(str(child.pid), encoding="ascii")
        time.sleep(120)
        return 0
    if mode == "memory":
        bytearray(256 * 1024 * 1024)
        return 0
    problem = request.get("input", request)
    source = Path(r"C:\fc-runner\solver.py")
    spec = importlib.util.spec_from_file_location("calibration_solver", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("calibration solver could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    answer = module.solve(int(problem["n"]), [tuple(e) for e in problem["edges"]],
                          int(problem["s"]), int(problem["t"]))
    if isinstance(answer, str):
        sys.stdout.write(answer)
    else:
        sys.stdout.write(str(answer))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
