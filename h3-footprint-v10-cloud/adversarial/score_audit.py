#!/usr/bin/env python3
"""Treat the execution report as untrusted input to score_smoke_report.score() and mutate it.

Run only in the scoring job. Verdict per mutation: REJECTED (scorer raised) or ACCEPTED (scorer returned PASS).
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_scorer():
    spec = importlib.util.spec_from_file_location("score_smoke_report", ROOT / "h3-footprint-v10-cloud" / "score_smoke_report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", required=True)
    ap.add_argument("--fixture-manifest", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    scorer = load_scorer()
    base = json.loads(Path(args.report).read_text(encoding="utf-8"))

    def mut(fn):
        obj = copy.deepcopy(base)
        fn(obj)
        return json.dumps(obj)

    def raw_bigint():
        obj = copy.deepcopy(base)
        obj["results"][3]["answer"] = -987654321
        return json.dumps(obj).replace("-987654321", "9" * 5000, 1)

    def raw_deep():
        return json.dumps(base)[:-1] + ', "deep": ' + "[" * 100000 + "]" * 100000 + "}"

    def swap(o):
        o["results"][0], o["results"][1] = o["results"][1], o["results"][0]

    # (name, text, expected) ; expected in {PASS, REJECT, REJECT_OR_RESOURCE_NOTE}
    cases = [
        ("baseline", json.dumps(base), "PASS"),
        ("answer_is_bool_true", mut(lambda o: o["results"][3].update(answer=True)), "REJECT"),
        ("answer_is_nan", mut(lambda o: o["results"][3].update(answer=float("nan"))), "REJECT"),
        ("answer_string", mut(lambda o: o["results"][3].update(answer="5")), "REJECT"),
        ("answer_5000_digit_int", raw_bigint(), "REJECT"),
        ("nesting_depth_100000", raw_deep(), "REJECT"),
        ("pad_20MiB", mut(lambda o: o.update(pad="A" * (20 * 1024 * 1024))), "REJECT_OR_RESOURCE_NOTE"),
        ("record_tree_empty_false_toplevel_true", mut(lambda o: o["results"][0].update(tree_empty=False)), "REJECT"),
        ("record_status_process_tree_leak", mut(lambda o: o["results"][0].update(status="process_tree_leak")), "REJECT"),
        ("records_swapped", mut(swap), "REJECT"),
        ("candidate_hash_mismatch", mut(lambda o: o.update(candidate_sha256="0" * 64)), "REJECT"),
        ("claims_reference_answers_present", mut(lambda o: o.update(reference_answers_present=True)), "REJECT"),
    ]
    results = []
    with tempfile.TemporaryDirectory() as td:
        for name, text, expected in cases:
            p = Path(td) / (name + ".json")
            p.write_text(text, encoding="utf-8")
            t0 = time.monotonic()
            try:
                r = scorer.score(p, Path(args.fixture_manifest))
                outcome, detail = "ACCEPTED", r.get("status")
            except Exception as exc:
                outcome, detail = "REJECTED", "%s: %s" % (type(exc).__name__, str(exc)[:120])
            dt = round(time.monotonic() - t0, 3)
            if expected == "PASS":
                verdict = "OK" if outcome == "ACCEPTED" else "CONTROL_BROKEN"
            elif expected == "REJECT":
                verdict = "NO_FINDING" if outcome == "REJECTED" else "FINDING"
            else:
                verdict = "NO_FINDING" if outcome == "REJECTED" else "NOTE_NO_SIZE_LIMIT"
            results.append({"case": name, "bytes": len(text), "outcome": outcome, "detail": detail, "seconds": dt, "verdict": verdict})
            print("%-42s %-9s %-20s %6.2fs %s" % (name, outcome, verdict, dt, detail), flush=True)
    Path(args.out).write_text(json.dumps({"version": 1, "scorer": "score_smoke_report.score", "cases": results}, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
