from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path

# Capture trusted references before the candidate module is imported. The
# candidate shares this process, so it can replace sys.stdout, json.dumps, or
# sys.argv; the worker must still emit exactly one nonce-tagged line to the
# parent. The parent, not this process, owns the expected values and decides
# whether a probe failed.
_STDOUT = sys.stdout
_DUMPS = json.dumps


def _emit(nonce: str, payload: dict) -> None:
    _STDOUT.write(nonce + " " + _DUMPS(payload, sort_keys=True) + "\n")
    _STDOUT.flush()


def load(path: Path):
    spec = importlib.util.spec_from_file_location("candidate", path)
    if spec is None or spec.loader is None:
        raise ImportError("no loader")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, "solve", None)
    if not callable(fn):
        raise AttributeError("missing solve")
    return fn


def _emit_answer(nonce: str, probe_index: int, out) -> None:
    try:
        _emit(nonce, {"phase": "probe", "probe_index": probe_index, "answer": out})
    except BaseException:
        _emit(nonce, {"phase": "probe", "probe_index": probe_index, "error": "unserializable"})


def main() -> None:
    if len(sys.argv) < 3:
        _emit("", {"phase": "harness", "error": "usage: candidate.py --preflight NONCE | --probe INDEX PROBE_JSON NONCE"})
        return
    path = Path(sys.argv[1])
    mode = sys.argv[2]

    if mode == "--preflight":
        if len(sys.argv) != 4:
            _emit("", {"phase": "harness", "error": "preflight requires a nonce"})
            return
        nonce = sys.argv[3]
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                load(path)
            _emit(nonce, {"phase": "preflight", "valid": True, "load_error": None})
        except BaseException as exc:
            _emit(nonce, {"phase": "load", "valid": False, "load_error": f"{type(exc).__name__}: {exc}"})
        return

    if mode != "--probe" or len(sys.argv) != 6:
        _emit("", {"phase": "harness", "error": "usage: candidate.py --preflight NONCE | --probe INDEX PROBE_JSON NONCE"})
        return

    nonce = sys.argv[5]
    try:
        probe_index = int(sys.argv[3])
        probe = json.loads(sys.argv[4])
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            solve = load(path)
    except BaseException as exc:
        _emit(nonce, {"phase": "load", "load_error": f"{type(exc).__name__}: {exc}"})
        return

    edges = [tuple(edge) if isinstance(edge, (list, tuple)) else edge for edge in probe["edges"]]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            out = solve(probe["n"], edges, probe["s"], probe["t"])
    except BaseException as exc:
        _emit(nonce, {"phase": "probe", "probe_index": probe_index, "error": type(exc).__name__})
        return
    _emit_answer(nonce, probe_index, out)


if __name__ == "__main__":
    main()
