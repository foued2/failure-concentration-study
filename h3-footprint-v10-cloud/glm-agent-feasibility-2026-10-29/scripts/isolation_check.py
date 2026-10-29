#!/usr/bin/env python3
"""Isolation check for the GLM-agent H3 exploratory pilot.

Runs hostile hand-written controls through the namespace boundary BEFORE any
generated candidate is executed, per h3-footprint-v3 GATE.md ("the isolation
check must include a harmless probe demonstrating that a candidate cannot
write outside its scratch directory and cannot reach the network, plus the
mechanism used"). Mirrors the v10 hosted-prototype control battery:
network denial, repo/credential invisibility, write confinement, resource
limits, hostile grandchild timeout, and a hand-written correct control solver.

Writes isolation-report.json. Exits nonzero if any REQUIRED control fails.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
NS_SETUP = HERE / "ns_setup.sh"
STAGE = Path("/var/tmp/h3trusted")
OUT = HERE / "isolation-report.json"
REPO_CANARY = Path("/home/z/my-project/fcs-verify/PROTOCOL.md")
REPO_DIR = Path("/home/z/my-project")

RLIMITS = {
    "RLIMIT_AS": (384 * 1024 * 1024, 384 * 1024 * 1024),
    "RLIMIT_CPU": (8, 9),
    "RLIMIT_CORE": (0, 0),
    "RLIMIT_NOFILE": (32, 32),
    "RLIMIT_FSIZE": (1024 * 1024, 1024 * 1024),
}


def _preexec():
    resource.setrlimit(resource.RLIMIT_AS, RLIMITS["RLIMIT_AS"])
    resource.setrlimit(resource.RLIMIT_CPU, RLIMITS["RLIMIT_CPU"])
    resource.setrlimit(resource.RLIMIT_CORE, RLIMITS["RLIMIT_CORE"])
    resource.setrlimit(resource.RLIMIT_NOFILE, RLIMITS["RLIMIT_NOFILE"])
    resource.setrlimit(resource.RLIMIT_FSIZE, RLIMITS["RLIMIT_FSIZE"])


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
            # field 6 = session id; parse after final ')' to avoid comm spaces
            tail = stat[stat.rindex(b")") + 2 :].split()
            if int(tail[2]) == sid:
                found.append(pid)
        except (OSError, ValueError, IndexError):
            continue
    return found


def run_in_ns(scratch_id: str, argv: list[str], timeout: float = 30.0,
              stdin_bytes: bytes | None = None) -> dict:
    cmd = ["unshare", "-r", "-m", "-n", "/bin/sh", str(NS_SETUP), scratch_id] + argv
    started = time.monotonic()
    proc = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        preexec_fn=_preexec, start_new_session=True,
    )
    try:
        out, err = proc.communicate(input=stdin_bytes, timeout=timeout)
        rc, timed_out = proc.returncode, False
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            pass
        out, err = proc.communicate()
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
    return {
        "return_code": rc,
        "timed_out": timed_out,
        "stdout": out.decode("utf-8", "replace"),
        "stderr": err.decode("utf-8", "replace"),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "survivors_after_cleanup": survivors,
        "tree_empty": not survivors,
    }


# ---------------- hostile control payloads (hand-written, not generated) ----

C_NET = r"""
import socket
try:
    socket.create_connection(("140.82.121.4", 443), timeout=4)
    print("NET-RESULT: CONNECTED (ISOLATION FAIL)")
except Exception as e:
    print(f"NET-RESULT: blocked {type(e).__name__}")
try:
    socket.getaddrinfo("github.com", 443)
    print("DNS-RESULT: resolved (ISOLATION FAIL)")
except Exception as e:
    print(f"DNS-RESULT: blocked {type(e).__name__}")
"""

C_FS = r"""
import os
try:
    data = open("/home/z/my-project/PROTOCOL.md").read(50)
    print("REPO-READ: SUCCESS (ISOLATION FAIL)")
except Exception as e:
    print(f"REPO-READ: blocked {type(e).__name__}")
try:
    open("/home/z/my-project/.env").read(50)
    print("ENV-READ: SUCCESS (ISOLATION FAIL)")
except Exception as e:
    print(f"ENV-READ: blocked {type(e).__name__}")
try:
    os.listdir("/proc")
    print("PROC-LISTING: SUCCESS (visible)")
except Exception as e:
    print(f"PROC-LISTING: blocked {type(e).__name__}")
print("ROOT-LISTING:", sorted(os.listdir("/")))
"""

C_WRITE = r"""
import os
try:
    with open("/home/z/escape-test.txt", "w") as f:
        f.write("x" * 100)
    print("WROTE /home/z/escape-test.txt (UNEXPECTED)")
except Exception as e:
    print(f"HOME-WRITE: blocked {type(e).__name__}")
try:
    with open("/tmp/escape-test.txt", "w") as f:
        f.write("y" * 100)
    print("WROTE /tmp/escape-test.txt (view tmpfs, discarded at ns exit)")
except Exception as e:
    print(f"TMP-WRITE: blocked {type(e).__name__}")
with open(os.path.join(os.environ["HOME"], "scratch-write.txt"), "w") as f:
    f.write("ok")
print("WROTE scratch file (allowed)")
print("ROOT-LISTING:", sorted(os.listdir("/")))
"""

C_MEM = r"""
try:
    blob = bytearray(512 * 1024 * 1024)
    print("MEM-RESULT: allocated 512MB (ISOLATION FAIL)")
except (MemoryError, KeyboardInterrupt) as e:
    print(f"MEM-RESULT: blocked {type(e).__name__}")
"""

# hostile pipeline control: solve() spawns a grandchild looper, prints spam,
# then sleeps past the probe timeout — must yield status=timeout, tree_empty.
C_HOSTILE_BODY = r'''
import subprocess, time, sys
def solve(n, edges, s, t):
    p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)"])
    for _ in range(100000):
        print("spam" * 100)
        time.sleep(0.5)
    return 0
'''

# hand-written correct control solver (reference dijkstra, mirrors instrument)
C_CONTROL_BODY = r'''
import heapq
def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [10**30] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1 if dist[t] == 10**30 else dist[t]
'''


def main() -> int:
    report: dict = {
        "kind": "glm_agent_h3_pilot_isolation_check",
        "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mechanism": (
            "unshare -r -m -n (private user+mount+network namespace) + fresh "
            "size-capped tmpfs over /home/z /root /var/tmp /tmp /dev/shm /run + "
            "minimal chroot view root (read-only /usr /lib /lib64 /dev/null binds, "
            "candidate body at /candidate, trusted harness at /trusted, no /proc) + "
            "env -i + RLIMIT_AS 384MiB / RLIMIT_CPU 8s / RLIMIT_FSIZE 1MiB / "
            "RLIMIT_NOFILE 32 + per-probe 5s deadline with killpg + session-scoped "
            "process-tree leak check + host-side tamper canaries"
        ),
        "deviations_from_container_reference": [
            "No Docker runtime in this sandbox; namespace/tmpfs/chroot/rlimit stack used instead (pinned python:3.14-slim container replaced by host CPython 3.13.5 at /usr/bin/python3).",
            "Child runs as mapped-root inside the private user namespace (newuidmap unavailable), so in-namespace root could in principle attempt umount of overlays or a double-chroot escape; the static forbidden-import filter (os/ctypes/subprocess...) blocks accepted candidates from attempting it, the view root exposes no /proc, and host-side canaries make any successful escape detectable. Residual accepted and monitored for this exploratory pilot only.",
            "Process-tree leak check is scoped to the child session id, not container-global PIDs.",
        ],
        "controls": {},
        "host_canaries": {},
    }

    # host canaries before any execution
    canary_before = sha256_file(REPO_CANARY)
    home_before = sorted(p.name for p in REPO_DIR.iterdir())

    controls = report["controls"]

    # C1 network
    r = run_in_ns("c1", ["/usr/bin/python3", "-c", C_NET])
    net_ok = "NET-RESULT: blocked" in r["stdout"] and "DNS-RESULT: blocked" in r["stdout"]
    controls["C1_network_denied"] = {**r, "pass": net_ok, "required": True}

    # C2 repo/credential invisibility
    r = run_in_ns("c2", ["/usr/bin/python3", "-c", C_FS])
    fs_ok = ("REPO-READ: blocked" in r["stdout"] and "ENV-READ: blocked" in r["stdout"]
             and "PROC-LISTING: blocked" in r["stdout"])
    controls["C2_repo_hidden"] = {**r, "pass": fs_ok, "required": True}

    # C3 write confinement (host must be unchanged afterwards)
    r = run_in_ns("c3", ["/usr/bin/python3", "-c", C_WRITE])
    home_after = sorted(p.name for p in REPO_DIR.iterdir())
    controls["C3_write_confined"] = {
        **r,
        "host_home_listing_unchanged": home_after == home_before,
        "pass": ("HOME-WRITE: blocked" in r["stdout"]
                 and "WROTE scratch file (allowed)" in r["stdout"]
                 and home_after == home_before),
        "required": True,
    }

    # C4 memory cap
    r = run_in_ns("c4", ["/usr/bin/python3", "-c", C_MEM])
    controls["C4_memory_capped"] = {**r, "pass": "MEM-RESULT: blocked" in r["stdout"], "required": True}

    # C5 hostile pipeline control (grandchild + spam + sleep) through candidate_child
    (STAGE / "candidate").mkdir(parents=True, exist_ok=True)
    (STAGE / "candidate" / "body.py").write_text(C_HOSTILE_BODY)
    payload = json.dumps({"probe_id": "hostile-ctl", "phase": "probe", "n": 2,
                          "edges": [[0, 1, 1]], "s": 0, "t": 1}) + "\n"
    r = run_in_ns(
        "c5",
        ["/usr/bin/python3", "-I", "-B", "/trusted/candidate_child.py",
         "--probe-timeout", "5.0"],
        timeout=30.0, stdin_bytes=payload.encode(),
    )
    h3pred = next((l for l in r["stdout"].splitlines() if l.startswith("H3PRED ")), None)
    rec = json.loads(h3pred[len("H3PRED "):]) if h3pred else {}
    controls["C5_hostile_timeout_control"] = {
        **r, "prediction_record": rec,
        "pass": rec.get("status") == "timeout" and r["tree_empty"],
        "required": True,
    }

    # C6 correct control solver through the full pipeline (harness sanity)
    (STAGE / "candidate" / "body.py").write_text(C_CONTROL_BODY)
    payload = json.dumps({"probe_id": "control-ctl", "phase": "probe", "n": 4,
                          "edges": [[0, 1, 1], [1, 2, 1], [2, 3, 1]], "s": 0, "t": 3}) + "\n"
    r = run_in_ns(
        "c6",
        ["/usr/bin/python3", "-I", "-B", "/trusted/candidate_child.py",
         "--probe-timeout", "5.0"],
        timeout=30.0, stdin_bytes=payload.encode(),
    )
    h3pred = next((l for l in r["stdout"].splitlines() if l.startswith("H3PRED ")), None)
    rec = json.loads(h3pred[len("H3PRED "):]) if h3pred else {}
    controls["C6_control_solver_correct"] = {
        **r, "prediction_record": rec,
        "pass": rec.get("status") == "ok" and rec.get("answer") == 3 and rec.get("answer_type") == "int",
        "required": True,
    }

    # host canaries after all controls
    report["host_canaries"] = {
        "repo_canary_file": str(REPO_CANARY),
        "canary_sha256_before": canary_before,
        "canary_sha256_after": sha256_file(REPO_CANARY),
        "canary_unchanged": canary_before == sha256_file(REPO_CANARY),
        "host_home_listing_unchanged": sorted(p.name for p in REPO_DIR.iterdir()) == home_before,
    }

    report["all_required_pass"] = all(
        c["pass"] for c in controls.values() if c.get("required")
    )
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {k: {"pass": v["pass"], "status_or_rc": (
        v.get("prediction_record", {}).get("status") or v["return_code"])}
        for k, v in controls.items()}
    print(json.dumps({"all_required_pass": report["all_required_pass"],
                      "canary_unchanged": report["host_canaries"]["canary_unchanged"],
                      "controls": summary}, indent=2))
    return 0 if report["all_required_pass"] and report["host_canaries"]["canary_unchanged"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
