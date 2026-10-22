"""Strict guest-side expression adapter for the declared int return contract."""
from __future__ import annotations

import base64
import importlib.util
import json
import sys
from pathlib import Path


def encode_result(value: object) -> dict:
    """Preserve the guest-side Python type; only exact int gets an int answer."""
    kind = type(value).__name__
    if type(value) is int:
        return {"return_type": "int", "value": str(value)}
    if type(value) is str:
        return {"return_type": "str", "value": value[:200]}
    if type(value) is bool:
        return {"return_type": "bool", "value": "true" if value else "false"}
    if type(value) is float:
        return {"return_type": "float", "value": repr(value)[:200]}
    if value is None:
        return {"return_type": "NoneType", "value": None}
    return {"return_type": kind}


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
    answer = module.solve(problem["expr"])
    sys.stdout.write(json.dumps(encode_result(answer), separators=(",", ":"), ensure_ascii=True))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
