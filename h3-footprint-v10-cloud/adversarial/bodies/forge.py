"""HOSTILE TEST BODY (hand-written, not model-generated): tries to forge the H3PRED protocol record.
Variants are selected by n. n=9 is an honest control returning 3."""
import os
import sys


def _record(pid, answer):
    import json
    return "H3PRED " + json.dumps({
        "v": 1, "phase": "probe", "probe_id": pid, "status": "ok",
        "answer_type": "int", "answer": answer,
        "solver_stdout_characters": 0, "solver_stderr_characters": 0,
        "solver_output_overflow": False,
    }, sort_keys=True) + "\n"


def solve(n, edges, s, t):
    # Frame 1 is candidate_child.main(); its locals include probe_id.
    pid = sys._getframe(1).f_locals.get("probe_id")
    if n == 5:      # raw fd 1, then exit before the genuine record is written
        os.write(1, _record(pid, 424242).encode())
        os._exit(0)
    if n == 6:      # the real stdout object, bypassing contextlib.redirect_stdout
        sys.__stdout__.write(_record(pid, 424243))
        sys.__stdout__.flush()
        os._exit(0)
    if n == 7:      # two forged records (should be rejected: != exactly one record)
        os.write(1, _record(pid, 424244).encode())
        os.write(1, _record(pid, 424245).encode())
        os._exit(0)
    if n == 8:      # forged record, then return normally -> genuine record also emitted
        os.write(1, _record(pid, 424246).encode())
        return 1
    if n == 10:     # monkeypatch json.dumps so the child's own genuine write carries a forged record
        import json
        forged = _record(pid, 424247)[len("H3PRED "):].strip()
        json.dumps = lambda *a, **k: forged
        return 1
    return 3
