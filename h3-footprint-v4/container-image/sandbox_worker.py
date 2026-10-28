from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any

# Preserve the write primitive before importing untrusted candidate source.
_SAFE_WRITE = os.write
_RESULT_PREFIX = b"H3V4_RESULT "


def _emit(payload: dict[str, Any]) -> None:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    _SAFE_WRITE(1, _RESULT_PREFIX + data + b"\n")


def _is_json_primitive(value: Any) -> bool:
    if value is None or type(value) in (str, int, float, bool):
        return True
    if type(value) is list:
        return all(_is_json_primitive(x) for x in value)
    if type(value) is dict:
        return all(type(k) is str and _is_json_primitive(v) for k, v in value.items())
    return False


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("h3v4_candidate", path)
    if spec is None or spec.loader is None:
        raise ImportError("candidate module has no loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    solve = getattr(module, "solve", None)
    if not callable(solve):
        raise AttributeError("candidate has no callable solve")
    return solve


def main() -> int:
    # Read the complete one-probe message before importing the candidate.
    try:
        request = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        mode = request.get("mode")
        candidate_path = Path(request.get("candidate", "/candidate/solve.py"))
        if candidate_path != Path("/candidate/solve.py"):
            raise ValueError("candidate path is fixed")
        if mode not in ("preflight", "probe", "fixture"):
            raise ValueError("unsupported mode")
    except BaseException as exc:
        _emit({"status": "request_error", "error_type": type(exc).__name__})
        return 2

    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            solve = _load(candidate_path)
    except BaseException as exc:
        _emit({
            "status": "load_error",
            "error_type": type(exc).__name__,
            "error": str(exc)[:200],
        })
        return 0

    if mode == "preflight":
        _emit({"status": "preflight_ok"})
        return 0

    probe = request.get("probe")
    if not isinstance(probe, dict):
        _emit({"status": "request_error", "error_type": "invalid_probe"})
        return 2

    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            value = solve(probe["n"], probe["edges"], probe["s"], probe["t"])
    except BaseException as exc:
        _emit({
            "status": "runtime_error",
            "error_type": type(exc).__name__,
            "error": str(exc)[:200],
        })
        return 0

    if mode == "fixture":
        if not _is_json_primitive(value):
            _emit({"status": "fixture_result_error", "type": "non_json_value"})
            return 0
        _emit({"status": "fixture_ok", "value": value})
        return 0

    # Never stringify or call methods on an arbitrary candidate return object.
    if type(value) is int:
        _emit({"status": "ok", "answer_type": "int", "answer": value})
    elif type(value) is bool:
        _emit({"status": "ok", "answer_type": "bool", "answer": None})
    else:
        _emit({"status": "ok", "answer_type": "non_int", "answer": None})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
