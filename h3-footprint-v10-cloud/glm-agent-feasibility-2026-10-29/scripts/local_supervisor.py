#!/usr/bin/env python3
"""GLM-agent H3 exploratory pilot - isolated execution stage.

For every candidate_ready request in candidate-index.json:
  1. stage the candidate body (hash-verified) at /var/tmp/h3trusted/candidate/body.py
  2. preflight (phase=preflight) through the namespace boundary via the trusted
     candidate_child.py coordinator; invalid modules get no k (GATE.md rule)
  3. run the 30 frozen probes sequentially, one fresh namespace per probe,
     5.0s probe deadline, RLIMIT stack, session-scoped tree-leak check
  4. assemble a per-candidate execution report in the exact schema consumed by
     copilot_auto_pilot.run_scoring (candidate_sha256, probe_count, results[],
     all_trees_empty, isolation_harness_ok) plus sandbox-specific evidence fields.

This program is trusted code: it never executes candidate bodies itself and
never reads expected answers. Predictions remain untrusted.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import sys
import time
from typing import Any

HERE = Path(__file__).resolve().parent
NS_SETUP = HERE / "ns_setup.sh"
STAGE = Path("/var/tmp/h3trusted")
INDEX = HERE / "pilot-run" / "candidate-index.json"
REPORTS_DIR = HERE / "pilot-run" / "execution-reports"
EXEC_LOG = HERE / "pilot-run" / "execution-log.json"
INSTRUMENT_PATH = Path("/home/z/my-project/fcs-verify/h3-footprint-v3/instrument.py")

RESPONSE_TIMEOUT = 12.0      # host-side deadline for one H3PRED line (matches container default)
PROBE_TIMEOUT = "5.0"        # passed to candidate_child (matches GATE)
RLIMITS = [
    (resource.RLIMIT_AS, 384 * 1024 * 1024, 384 * 1024 * 1024),
    (resource.RLIMIT_CPU, 8, 9),
    (resource.RLIMIT_CORE, 0, 0),
    (resource.RLIMIT_NOFILE, 32, 32),
    (resource.RLIMIT_FSIZE, 1024 * 1024, 1024 * 1024),
]


def _preexec():
    for res, cur, mx in RLIMITS:
        resource.setrlimit(res, (cur, mx))


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def session_survivors(sid: int) -> list[int]:
    found = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        pid = int(entry)
        try:
            with open(f"/proc/{pid}/stat", "rb") as f:
                stat = f.read()
            tail = stat[stat.rindex(b")") + 2:].split()
            if int(tail[2]) == sid:
                found.append(pid)
        except (OSError, ValueError, IndexError):
            continue
    return found


def run_probe(scratch_id: str, payload: dict) -> dict:
    """One probe through the boundary; returns a supervisor record."""
    line = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode() + b"\n"
    cmd = ["unshare", "-r", "-m", "-n", "/bin/sh", str(NS_SETUP), scratch_id,
           "/usr/bin/python3", "-I", "-B", "/trusted/candidate_child.py",
           "--probe-timeout", PROBE_TIMEOUT]
    started = time.monotonic()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, preexec_fn=_preexec,
                            start_new_session=True)
    timed_out = overflow = False
    stdout = b""
    try:
        stdout, stderr = proc.communicate(input=line, timeout=RESPONSE_TIMEOUT)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            pass
        stdout, stderr = proc.communicate()
        rc = proc.returncode
    survivors = session_survivors(proc.pid)
    for pid in survivors:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
    if survivors:
        time.sleep(0.2)
        survivors = session_survivors(proc.pid)

    record: dict[str, Any] = {
        "probe_id": payload["probe_id"],
        "phase": payload.get("phase", "probe"),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "child_return_code": rc,
        "child_timed_out": timed_out,
        "child_stderr_bytes": len(stderr),
        "tree_empty": not survivors,
        "survivors_after_cleanup": survivors,
    }
    # parse the single H3PRED protocol line (untrusted prediction)
    pred = None
    lines = [l for l in stdout.decode("utf-8", "replace").splitlines() if l.startswith("H3PRED ")]
    if len(lines) == 1:
        try:
            item = json.loads(lines[0][len("H3PRED "):])
            if isinstance(item, dict) and item.get("v") == 1 and item.get("probe_id") == payload["probe_id"]:
                pred = item
        except json.JSONDecodeError:
            pred = None
    record["prediction_raw_status"] = (pred or {}).get("status")

    if timed_out:
        record["status"] = "timeout"
        record["answer_type"], record["answer"] = "none", None
    elif survivors:
        record["status"] = "process_tree_leak"
        record["fatal"] = True
        record["answer_type"], record["answer"] = "none", None
    elif pred is None or rc != 0:
        record["status"] = "invalid_child_output"
        record["answer_type"], record["answer"] = "none", None
    elif pred.get("status") == "ok" and pred.get("solver_output_overflow") is True:
        record["status"] = "output_overflow"
        record["answer_type"], record["answer"] = "none", None
    else:
        record["status"] = pred.get("status", "invalid_child_output")
        record["answer_type"] = pred.get("answer_type", "none")
        record["answer"] = pred.get("answer")
    record["solver_stdout_characters"] = (pred or {}).get("solver_stdout_characters")
    record["solver_stderr_characters"] = (pred or {}).get("solver_stderr_characters")
    return record


def main() -> int:
    sys.path.insert(0, str(INSTRUMENT_PATH.parent))
    import instrument  # trusted frozen instrument (probe inputs only)

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    probes = []
    for p in instrument.PROBES:
        probes.append({
            "probe_id": p["probe_id"], "phase": "probe", "n": p["n"],
            "edges": [list(e) for e in p["edges"]], "s": p["s"], "t": p["t"],
        })
    preflight_payload = {"probe_id": "preflight", "phase": "preflight",
                         "n": 1, "edges": [], "s": 0, "t": 0}

    staged_body = STAGE / "candidate" / "body.py"
    log: dict[str, Any] = {"candidates": {}, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    for rec in index["requests"]:
        if rec.get("status") != "candidate_ready":
            continue
        rid = rec["request_id"]
        body_bytes = (HERE / "pilot-run" / rec["body_path"]).read_bytes()
        assert hashlib.sha256(body_bytes).hexdigest() == rec["body_sha256"], f"body hash mismatch {rid}"
        staged_body.write_bytes(body_bytes)
        assert sha256_file(staged_body) == rec["body_sha256"], f"staging hash mismatch {rid}"

        cand_log: dict[str, Any] = {"body_sha256": rec["body_sha256"]}
        # preflight
        pf = run_probe(f"{rid}-pf", preflight_payload)
        cand_log["preflight"] = pf
        if not (pf["status"] == "ok" and pf.get("answer_type") == "callable"):
            reason = pf["status"] if pf["status"] != "invalid_child_output" else "import_or_load_error"
            cand_log["verdict"] = f"invalid_candidate_{reason}"
            log["candidates"][rid] = cand_log
            report = {
                "version": 1, "candidate_sha256": rec["body_sha256"],
                "sandbox": "glm-agent chroot-namespace boundary (see isolation-report.json)",
                "probe_count": 0, "results": [], "all_trees_empty": pf["tree_empty"],
                "preflight": pf, "preflight_passed": False,
                "candidate_generation_performed": False, "scoring_performed": False,
                "reference_answers_present": False, "host_repository_mounted": False,
                "api_keys_passed_to_child": False,
                "isolation_harness_ok": False,
            }
            (REPORTS_DIR / f"{rid}.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
            print(f"{rid}: invalid candidate ({reason}); no k assigned", flush=True)
            continue

        results = []
        fatal = False
        for p in probes:
            r = run_probe(f"{rid}-{p['probe_id']}", p)
            if r.get("fatal") or not r["tree_empty"]:
                fatal = True
            results.append({k: r[k] for k in (
                "probe_id", "phase", "status", "answer_type", "answer",
                "child_return_code", "child_timed_out", "tree_empty",
                "elapsed_seconds", "solver_stdout_characters", "solver_stderr_characters")})
        all_trees_empty = all(r["tree_empty"] for r in results) and not fatal
        report = {
            "version": 1, "candidate_sha256": rec["body_sha256"],
            "sandbox": "glm-agent chroot-namespace boundary (see isolation-report.json)",
            "probe_count": len(results), "results": results,
            "all_trees_empty": all_trees_empty,
            "preflight": pf, "preflight_passed": True,
            "candidate_generation_performed": False, "scoring_performed": False,
            "reference_answers_present": False, "host_repository_mounted": False,
            "api_keys_passed_to_child": False,
            "isolation_harness_ok": (not fatal) and len(results) == 30,
        }
        (REPORTS_DIR / f"{rid}.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        statuses = [r["status"] for r in results]
        cand_log["verdict"] = "executed_30_probes"
        cand_log["status_counts"] = {s: statuses.count(s) for s in set(statuses)}
        log["candidates"][rid] = cand_log
        print(f"{rid}: 30 probes done; statuses={ {s: statuses.count(s) for s in set(statuses)} }", flush=True)

    log["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EXEC_LOG.write_text(json.dumps(log, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("execution stage complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
