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
import tempfile
import threading
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


class EventLog:
    """Write diagnostic events as uniquely named files in the outbox.

    Each event is a new file written directly and closed: a mapped folder rejects
    ``os.replace`` while the Sandbox runs, and the host must never see a
    half-written record under the final name. Sequence numbers are monotone per
    process, so the host can order events without trusting the guest clock.

    This is telemetry, not evidence of isolation. A heartbeat proves the agent
    is alive; it proves nothing about what the candidate could reach.
    """

    def __init__(self, outbox: Path, nonce: str, *, pid: int | None = None) -> None:
        self.outbox = Path(outbox)
        self.nonce = nonce
        self.pid = int(pid or os.getpid())
        self.seq = 0
        self._lock = threading.Lock()

    def emit(self, event: str, *, phase: str, job: dict | None = None,
             detail: str | None = None) -> dict:
        with self._lock:
            self.seq += 1
            record = {
                "v9": protocol.JOB_SCHEMA,
                "nonce": self.nonce,
                "pid": self.pid,
                "seq": self.seq,
                "event": event,
                "phase": phase,
                "timestamp": time.time(),
                "job_id": job.get("job_id") if job else None,
                "job_sequence": job.get("sequence") if job else None,
                "detail": detail[:protocol.EVENT_DETAIL_LIMIT] if detail else None,
            }
            protocol.write_event(self.outbox, record)
            return record


class Heartbeat(threading.Thread):
    """Prove the agent is alive between jobs, without touching the job protocol."""

    def __init__(self, log: EventLog, interval: float) -> None:
        super().__init__(name="v9-heartbeat", daemon=True)
        self.log = log
        self.interval = max(0.2, float(interval))
        self._stop = threading.Event()

    def run(self) -> None:
        while not self._stop.wait(self.interval):
            try:
                self.log.emit("heartbeat", phase="serve", detail="alive")
            except OSError:
                return

    def stop(self) -> None:
        self._stop.set()


def wait_for_session(inbox: Path, timeout: float, poll: float = 0.1) -> dict | None:
    """Wait for the host to publish session.json.

    The Sandbox may start the LogonCommand before the controller has written the
    session. Exiting immediately in that case made launch order mandatory; this
    makes either order work.
    """
    path = Path(inbox) / SESSION
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass
        time.sleep(poll)
    return None


def handshake(inbox: Path, outbox: Path, session: dict | None = None,
              mode: str = "serve") -> dict:
    """Echo the host's nonce together with our own observed identity."""
    if session is None:
        session = json.loads((Path(inbox) / SESSION).read_text(encoding="utf-8"))
    ident = winjob.identity()
    record = {
        "v9": protocol.JOB_SCHEMA,
        "nonce": session["nonce"],
        "mode": mode,
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
          poll: float = 0.1, events: EventLog | None = None) -> int:
    """Execute each newly published job exactly once.

    The loop records what it sees. If the host rewrites ``job.json`` and the
    guest's view of the mapping stays stale, the agent keeps seeing the job it
    already handled; the heartbeat continues but no ``job_discovered`` appears
    for the new job. That distinction is the whole point of the instrumentation.
    """
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
        if events is not None:
            events.emit("job_discovered", phase="serve", job=job)
            events.emit("job_started", phase="serve", job=job)
        try:
            supervisor.run_job(
                inbox, outbox, scratch,
                timeout=timeout, memory_bytes=memory_bytes, max_processes=max_processes,
                lock_staging=False, lock_response=False,
            )
        except Exception as exc:  # noqa: BLE001 - the agent must record, not die
            if events is not None:
                events.emit("exception", phase="serve", job=job,
                            detail=f"{type(exc).__name__}: {exc}")
        else:
            if events is not None:
                events.emit("response_written", phase="serve", job=job)
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
    parser.add_argument("--session-timeout", type=float, default=300.0,
                        help="how long to wait for the host to publish session.json")
    parser.add_argument("--handshake-only", action="store_true",
                        help="prove identity and echo the nonce, then exit; serves no job")
    parser.add_argument("--heartbeat-interval", type=float, default=2.0,
                        help="seconds between liveness events in serve mode (default: 2)")
    parser.add_argument("--allow-host", action="store_true",
                        help="local testing only; the host handshake will reject it")
    args = parser.parse_args()

    check_environment(args.allow_host)
    inbox, outbox = Path(args.inbox), Path(args.outbox)

    session = wait_for_session(inbox, args.session_timeout)
    if session is None:
        print(json.dumps({
            "status": "boundary_error",
            "error": "no_session",
            "detail": f"session.json did not appear within {args.session_timeout:.0f}s",
            "user": winjob.identity()["user"],
            "inside_sandbox": winjob.identity()["inside_sandbox"],
        }, sort_keys=True), file=sys.stderr)
        raise SystemExit(3)

    events = None
    if not args.handshake_only:
        # Created before the handshake so a crash during startup is visible too.
        events = EventLog(outbox, session["nonce"])
        try:
            events.emit("agent_start", phase="startup",
                        detail=f"mode=serve pid={os.getpid()}")
        except OSError:
            events = None

    handshake(inbox, outbox, session,
              mode="preflight" if args.handshake_only else "serve")
    if args.handshake_only:
        return

    # The scratch directory must be on the guest's local disk: a mapped folder
    # cannot take an integrity label, so icacls fails there and the supervisor
    # refuses to run the child (status boundary_error).
    scratch = (Path(args.scratch) if args.scratch
               else Path(tempfile.gettempdir()) / "h3-scratch")

    heartbeat = Heartbeat(events, args.heartbeat_interval) if events is not None else None
    if heartbeat is not None:
        heartbeat.start()
    try:
        serve(inbox, outbox, scratch, timeout=args.timeout,
              memory_bytes=args.memory_bytes, max_processes=args.max_processes,
              max_jobs=args.max_jobs, events=events)
    finally:
        if heartbeat is not None:
            heartbeat.stop()


if __name__ == "__main__":
    main()
