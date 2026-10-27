from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import instrument  # noqa: E402


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


def main() -> None:
    path = Path(sys.argv[1])
    mode = sys.argv[2] if len(sys.argv) > 2 else "--preflight"
    if mode == "--preflight":
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                load(path)
            print(json.dumps({"phase": "preflight", "valid": True, "load_error": None}))
        except BaseException as exc:
            print(json.dumps({"phase": "load", "valid": False, "load_error": f"{type(exc).__name__}: {exc}"}))
        return

    if mode != "--probe" or len(sys.argv) != 4:
        print(json.dumps({"phase": "harness", "error": "usage: candidate.py --preflight | --probe INDEX"}))
        return
    try:
        probe_index = int(sys.argv[3])
        if not 0 <= probe_index < len(instrument.PROBES):
            raise IndexError("probe index out of range")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            solve = load(path)
    except BaseException as exc:
        print(json.dumps({"phase": "load", "load_error": f"{type(exc).__name__}: {exc}"}))
        return

    p = instrument.PROBES[probe_index]
    expected_path = HERE / "expected_values.json"
    expected = json.loads(expected_path.read_text(encoding="utf-8"))[p["probe_id"]]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            out = solve(p["n"], p["edges"], p["s"], p["t"])
        bad = isinstance(out, bool) or not isinstance(out, int) or out != expected
    except BaseException:
        bad = True
    print(json.dumps({"phase": "probe", "probe_index": probe_index, "fail": bool(bad), "load_error": None}))


if __name__ == "__main__":
    main()
