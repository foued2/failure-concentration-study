#!/usr/bin/env python3
"""Bounded adversarial audit driver for the H3 V10 hosted executor (hand-written hostile bodies only).

No model calls, no generated solvers. Each fixture runs through the UNMODIFIED run_container_candidate.run_candidate.
Verdicts are DATA, not test failures: NO_FINDING / FINDING / INCONCLUSIVE / HARNESS_ERROR.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

FORGED = {424242, 424243, 424244, 424245, 424246, 424247}


def load_runner(trusted_dir):
    spec = importlib.util.spec_from_file_location("h3_rcc", Path(trusted_dir) / "run_container_candidate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_probes(name, ns):
    return [{"probe_id": "adv-%s-%d-n%d" % (name, i, n), "n": n, "edges": [], "s": 0, "t": n - 1}
            for i, n in enumerate(ns)]


def rows_of(report, ns):
    rows = []
    for n, r in zip(ns, report["results"]):
        rows.append({
            "n": n, "status": r.get("status"), "answer": r.get("answer"),
            "tree_empty": r.get("tree_empty"), "timed_out": r.get("timed_out"),
            "output_overflow": r.get("output_overflow"),
            "processes_at_post_check": r.get("processes_present_at_post_child_check"),
            "tmp_cleanup_ok": r.get("tmp_cleanup_ok"), "elapsed": r.get("elapsed_seconds"),
        })
    return rows


def row(rows, n):
    for r in rows:
        if r["n"] == n:
            return r
    return None


def v_forge(rows):
    hits = ["n=%s: status=%s answer=%s" % (r["n"], r["status"], r["answer"])
            for r in rows if r["n"] != 9 and r["status"] == "ok" and r["answer"] in FORGED]
    ctrl = row(rows, 9)
    if not (ctrl and ctrl["status"] == "ok" and ctrl["answer"] == 3):
        return "INCONCLUSIVE", ["honest control n=9 did not return ok/3"] + hits
    return ("FINDING" if hits else "NO_FINDING"), hits or ["no forged answer accepted"]


def v_flood(rows):
    notes, bad = [], False
    for n in (5, 6, 7):
        r = row(rows, n)
        if r is None:
            notes.append("n=%d missing" % n)
            bad = True
            continue
        notes.append("n=%d status=%s elapsed=%s" % (n, r["status"], r["elapsed"]))
        if r["status"] == "ok":
            bad = True
    ctrl = row(rows, 8)
    if not (ctrl and ctrl["status"] == "ok"):
        return "INCONCLUSIVE", notes + ["recovery probe n=8 not ok"]
    return ("FINDING" if bad else "NO_FINDING"), notes


def v_memory(rows):
    r, c = row(rows, 5), row(rows, 6)
    notes = ["n=5 status=%s blocks_before_MemoryError=%s" % (r and r["status"], r and r["answer"])]
    if not (c and c["status"] == "ok"):
        return "INCONCLUSIVE", notes + ["recovery probe n=6 not ok"]
    if r and r["status"] == "ok" and isinstance(r["answer"], int) and r["answer"] < 0:
        return "FINDING", notes + ["RLIMIT_AS did not stop a 600 MiB virtual allocation"]
    if r and (r["status"] != "ok" or (isinstance(r["answer"], int) and 0 <= r["answer"] < 60)):
        return "NO_FINDING", notes
    return "INCONCLUSIVE", notes


def v_tmp(rows):
    r, c = row(rows, 5), row(rows, 6)
    notes = ["n=5 status=%s files_written=%s" % (r and r["status"], r and r["answer"]),
             "n=6 free_MiB_after_cleanup=%s" % (c and c["answer"])]
    if not (r and c and c["status"] == "ok"):
        return "INCONCLUSIVE", notes
    bad = []
    if isinstance(r["answer"], int) and r["answer"] >= 90:
        bad.append("scratch fill was not capped")
    if isinstance(c["answer"], int) and c["answer"] < 60:
        bad.append("/tmp space not reclaimed between probes")
    return ("FINDING" if bad else "NO_FINDING"), notes + bad


def v_pids(rows):
    r, c = row(rows, 5), row(rows, 6)
    notes = ["n=5 status=%s started=%s tree_empty=%s" % (r and r["status"], r and r["answer"], r and r["tree_empty"])]
    if not (r and c and c["status"] == "ok"):
        return "INCONCLUSIVE", notes + ["recovery probe n=6 not ok"]
    if isinstance(r["answer"], int) and r["answer"] >= 8:
        return "FINDING", notes + ["pids-limit 8 did not cap process creation"]
    return "NO_FINDING", notes


def v_persist(rows):
    r = row(rows, 6)
    if not (r and r["status"] == "ok"):
        return "INCONCLUSIVE", ["n=6 not ok: %s" % (r,)]
    return ("NO_FINDING" if r["answer"] == 1 else "FINDING"), ["other processes visible at next probe: %s (expected 1)" % r["answer"]]


def v_introspect(rows):
    r = row(rows, 5)
    if not (r and r["status"] == "ok" and isinstance(r["answer"], int)):
        return "INCONCLUSIVE", ["n=5 not ok: %s" % (r,)]
    f = r["answer"]
    names = {1: "trusted supervisor source readable (by design)", 2: "/proc/1/environ", 4: "/proc/1/fd/0",
             8: "write to /candidate", 16: "list /tmp", 32: "/proc/1/mem", 64: "uid != 65534", 128: "effective capabilities"}
    seen = [names[b] for b in names if f & b]
    bad = [names[b] for b in (2, 4, 8, 32, 64, 128) if f & b]
    return ("FINDING" if bad else "NO_FINDING"), ["bitmask=%d" % f] + seen


FIXTURES = [
    ("forge", "forge.py", [5, 6, 7, 8, 10, 9], v_forge, 30),
    ("flood", "flood.py", [5, 6, 7, 8], v_flood, 60),
    ("memory", "memory.py", [5, 6], v_memory, 30),
    ("tmpfill", "tmpfill.py", [5, 6], v_tmp, 30),
    ("pids", "pids.py", [5, 6], v_pids, 30),
    ("persist", "persist.py", [5, 6], v_persist, 30),
    ("introspect", "introspect.py", [5], v_introspect, 30),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trusted-dir", required=True)
    ap.add_argument("--bodies", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    runner = load_runner(args.trusted_dir)
    out = []
    for name, body, ns, fn, rt in FIXTURES:
        path = Path(args.bodies) / body
        entry = {"fixture": name, "body": body, "body_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "probe_n_sequence": ns}
        t0 = time.monotonic()
        try:
            report = runner.run_candidate(path, Path(args.trusted_dir), make_probes(name, ns),
                                          response_timeout=rt, probe_timeout=5.0)
            rows = rows_of(report, ns)
            verdict, notes = fn(rows)
            entry.update(rows=rows, verdict=verdict, notes=notes,
                         isolation_harness_ok=report["isolation_harness_ok"],
                         container_config_verified=report["container_config"]["verified"], image=report["image"])
        except Exception as exc:  # a fatal harness stop is itself evidence
            entry.update(rows=[], verdict="HARNESS_ERROR", notes=["%s: %s" % (type(exc).__name__, exc)])
        entry["wall_seconds"] = round(time.monotonic() - t0, 2)
        out.append(entry)
        print("%-10s %-14s %s" % (name, entry["verdict"], " | ".join(entry["notes"])), flush=True)
    Path(args.out).write_text(json.dumps({"version": 1, "model_calls": 0, "generated_solvers": 0, "fixtures": out}, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
