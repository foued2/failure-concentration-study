"""Sandbox-side broker agent.

Runs inside Windows Sandbox, as ``WDAGUtilityAccount``, with the host repository
absent from its filesystem view. It holds no reference data: it reads one job
from the read-only inbox mapping, hands it to the secret-free supervisor, and
writes one raw response to the writable outbox mapping.

The agent refuses to start unless its own token says it is inside Windows
Sandbox. ``--allow-host`` exists only so the handshake and job loop can be
exercised in unit tests; it also makes the agent report
``inside_sandbox: false``, which the host handshake then rejects.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import protocol  # noqa: E402
import supervisor  # noqa: E402
import winjob  # noqa: E402

HELLO = "hello.json"
SESSION = "session.json"


def check_environment(allow_host: bool = False) -> dict:
    ident = winjob.identity()
    if not ident["inside_sandbox"] and not allow_host:
        raise SystemExit(
            "refusing to serve: this process is not running inside Windows Sandbox "
            f"(account={ident['user']!r}). The host repository would be readable."
        )
    return ident


def handshake(inbox: Path, outbox: Path) -> dict:
    """Echo the host's nonce together with our own observed identity."""
    session = json.loads((Path(inbox) / SESSION).read_text(encoding="utf-8"))
    ident = winjob.identity()
    record = {
        "v9": protocol.JOB_SCHEMA,
        "nonce": session["nonce"],
        "pid": os.getpid(),
        "user": ident["user"],
        "computer": ident["computer"],
        "inside_sandbox": ident["inside_sandbox"],
        "source": ident["source"],
        "time": time.time(),
    }
    Path(outbox).mkdir(parents=True, exist_ok=True)
    protocol._atomic_write(
        Path(outbox) / HELLO, json.dumps(record, sort_keys=True).encode("utf-8")
    )
    return record


def serve(inbox: Path, outbox: Path, scratch: Path, *, timeout: float,
          memory_bytes: int, max_processes: int, max_jobs: int = 0,
          poll: float = 0.1) -> int:
    """Execute each newly published job exactly once."""
    inbox, outbox, scratch = Path(inbox), Path(outbox), Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    handled: str | None = None
    done = 0
    while True:
        try:
            job = protocol.read_job(inbox)
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            time.sleep(poll)
            continue
        if job["job_id"] == handled:
            time.sleep(poll)
            continue
        supervisor.run_job(
            inbox, outbox, scratch,
            timeout=timeout, memory_bytes=memory_bytes, max_processes=max_processes,
            lock_staging=False, lock_response=False,
        )
        handled = job["job_id"]
        done += 1
        if max_jobs and done >= max_jobs:
            return done


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inbox", required=True)
    parser.add_argument("--outbox", required=True)
    parser.add_argument("--scratch", default=None)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--memory-bytes", type=int, default=512 * 1024 * 1024)
    parser.add_argument("--max-processes", type=int, default=16)
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--allow-host", action="store_true",
                        help="local testing only; the host handshake will reject it")
    args = parser.parse_args()

    check_environment(args.allow_host)
    inbox, outbox = Path(args.inbox), Path(args.outbox)
    handshake(inbox, outbox)
    scratch = Path(args.scratch) if args.scratch else outbox / "scratch"
    serve(inbox, outbox, scratch, timeout=args.timeout,
          memory_bytes=args.memory_bytes, max_processes=args.max_processes,
          max_jobs=args.max_jobs)


if __name__ == "__main__":
    main()
