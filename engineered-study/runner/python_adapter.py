from __future__ import annotations

import base64
import importlib.util
import json
import sys
from pathlib import Path


def main() -> int:
    wire = sys.stdin.buffer.readline().strip()
    if wire.startswith(b"\xef\xbb\xbf"):
        wire = wire[3:]
    request = json.loads(base64.b64decode(wire, validate=True).decode("utf-8"))
    problem = request.get("input", request)
    source = Path(r"C:\fc-runner\solver.py")
    spec = importlib.util.spec_from_file_location("strict_solver", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("solver could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    answer = module.solve(problem["text"])
    if type(answer) is int:
        payload = {"return_type": "int", "value": str(answer)}
    else:
        payload = {"return_type": type(answer).__name__, "value": None}
    sys.stdout.write(json.dumps(payload, separators=(",", ":"), ensure_ascii=True))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
