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
    expected = instrument.expected_values()
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            solve = load(path)
    except BaseException as exc:
        print(json.dumps({"load_error": f"{type(exc).__name__}: {exc}", "fails": [True] * 30}))
        return
    fails = []
    for p in instrument.PROBES:
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                out = solve(p["n"], p["edges"], p["s"], p["t"])
            bad = isinstance(out, bool) or not isinstance(out, int) or out != expected[p["probe_id"]]
        except BaseException:
            bad = True
        fails.append(bool(bad))
    print(json.dumps({"load_error": None, "fails": fails}))


if __name__ == "__main__":
    main()
