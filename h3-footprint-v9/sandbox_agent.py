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
from typing import Callable

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
             detail: str | None = None, state: dict | None = None) -> dict:
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
            if state is not None:
                record["state"] = state
            protocol.write_event(self.outbox, record)
            return record


class JobLoopState:
    """The last thing the job loop observed, in a bounded shape.

    The heartbeat copies this snapshot so a reader can see the loop's last known
    position, but only a ``poll_state`` event is written by the loop itself and
    therefore counts as evidence that the loop ran.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._state: dict = {
            "poll_count": 0,
            "last_poll_at": None,
            "scanned": False,
            "visible": [],
            "visible_count": 0,
            "outcome": "no_jobs",
            "last_job_id": None,
            "last_job_sequence": None,
            "error": None,
            "error_file": None,
        }

    def observe(self, *, scanned: bool, visible: list[str], visible_count: int,
                outcome: str, error: str | None = None,
                error_file: str | None = None) -> dict:
        with self._lock:
            self._state["poll_count"] += 1
            self._state["last_poll_at"] = time.time()
            self._state["scanned"] = bool(scanned)
            self._state["visible"] = [
                name[:protocol.EVENT_VISIBLE_NAME_LIMIT]
                for name in visible[:protocol.EVENT_VISIBLE_LIMIT]
            ]
            self._state["visible_count"] = int(visible_count)
            self._state["outcome"] = outcome
            self._state["error"] = error[:protocol.EVENT_STATE_ERROR_LIMIT] if error else None
            self._state["error_file"] = (
                error_file[:protocol.EVENT_VISIBLE_NAME_LIMIT] if error_file else None
            )
            return dict(self._state)

    def mark_job(self, job: dict) -> None:
        with self._lock:
            self._state["last_job_id"] = job["job_id"]
            self._state["last_job_sequence"] = job["sequence"]

    def snapshot(self) -> dict:
        with self._lock:
            return dict(self._state)


class Heartbeat(threading.Thread):
    """Prove the agent is alive between jobs, without touching the job protocol."""

    def __init__(self, log: EventLog, interval: float,
                 state: Callable[[], dict] | None = None) -> None:
        super().__init__(name="v9-heartbeat", daemon=True)
        self.log = log
        self.interval = max(0.2, float(interval))
        self.state = state
        self._stop = threading.Event()

    def run(self) -> None:
        while not self._stop.wait(self.interval):
            try:
                snapshot = self.state() if self.state is not None else None
                self.log.emit("heartbeat", phase="serve", detail="alive", state=snapshot)
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
                paths=supervisor.runtime_paths(inbox, outbox, scratch),
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


def _decide_immutable(scan: dict, expected_sequence: int,
                      handled_ids: set[str]) -> tuple[str, dict | None, str | None, str | None]:
    """Return (outcome, processable job, error, error file) for one scan.

    Fail closed: an incomplete scan, or any malformed, duplicate or conflicting
    request, blocks *all* execution for this poll, even if one expected-sequence
    file looks valid. A transient read failure is simply retried on the next
    poll; a permanent condition keeps blocking.
    """
    if not scan["scanned"]:
        return "error", None, scan["scan_error"], None
    if scan.get("truncated"):
        return "error", None, "scan_truncated", None
    errors = scan["errors"]
    if errors:
        return "error", None, errors[0]["detail"], errors[0]["file"]
    requests = scan["requests"]
    for job in requests:
        if job["sequence"] == expected_sequence:
            if job["job_id"] in handled_ids:
                return "only_handled", None, None, None
            return "new_job", job, None, None
    if not requests:
        return "no_jobs", None, None, None
    if any(job["sequence"] > expected_sequence for job in requests):
        return "out_of_order", None, None, None
    return "only_handled", None, None, None


def serve_immutable(inbox: Path, outbox: Path, scratch: Path, *, timeout: float,
                    memory_bytes: int, max_processes: int, max_jobs: int = 0,
                    poll: float = 0.1, events: EventLog | None = None,
                    state_interval: float = 2.0, state_max: int = 60,
                    runner: Callable | None = None,
                    state: JobLoopState | None = None,
                    max_polls: int = 0) -> int:
    """Serve the opt-in immutable request protocol.

    Every poll is decided from a fresh directory scan. The loop records what it
    saw even when it saw nothing new, so a later failure can distinguish an empty
    directory, a visible-but-already-handled request, a malformed request and a
    valid new one. Requests are processed in sequence, at most once, and a body
    is addressed by its content hash.

    ``state`` is shared with the heartbeat thread so the heartbeat reports the
    loop's last known snapshot rather than a detached, never-updated object.
    """
    inbox, outbox, scratch = Path(inbox), Path(outbox), Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    run = runner or supervisor.run_immutable_job
    state = state if state is not None else JobLoopState()
    handled: set[str] = set()
    last_sequence = 0
    done = 0
    polls = 0
    emitted = 0
    last_outcome: str | None = None
    next_state = 0.0

    while True:
        polls += 1
        scan = protocol.scan_immutable_jobs(inbox)
        outcome, job, error, error_file = _decide_immutable(
            scan, last_sequence + 1, handled
        )
        snapshot = state.observe(
            scanned=scan["scanned"], visible=scan["visible"],
            visible_count=scan["visible_count"], outcome=outcome,
            error=error, error_file=error_file,
        )
        now = time.monotonic()
        if (events is not None and emitted < state_max
                and (emitted == 0 or outcome != last_outcome or now >= next_state)):
            events.emit("poll_state", phase="serve", state=snapshot)
            emitted += 1
            last_outcome = outcome
            next_state = now + state_interval

        if job is None:
            if max_polls and polls >= max_polls:
                return done
            time.sleep(poll)
            continue

        if events is not None:
            events.emit("job_discovered", phase="serve", job=job)
            events.emit("job_started", phase="serve", job=job)
        body = protocol.immutable_body_path(inbox, job["body_sha256"])
        try:
            run(job, body, outbox, scratch, timeout=timeout,
                memory_bytes=memory_bytes, max_processes=max_processes,
                paths=supervisor.runtime_paths(inbox, outbox, scratch))
        except Exception as exc:  # noqa: BLE001 - the agent must record, not die
            if events is not None:
                events.emit("exception", phase="serve", job=job,
                            detail=f"{type(exc).__name__}: {exc}")
        else:
            if events is not None:
                events.emit("response_written", phase="serve", job=job)
        handled.add(job["job_id"])
        last_sequence = job["sequence"]
        state.mark_job(job)
        done += 1
        if max_jobs and done >= max_jobs:
            return done
        if max_polls and polls >= max_polls:
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
    parser.add_argument("--job-protocol", choices=("legacy", "immutable"),
                        default="legacy",
                        help="opt-in diagnostic request protocol (default: legacy job.json)")
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
                        detail=(f"mode=serve pid={os.getpid()} "
                                f"protocol={args.job_protocol}"))
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

    if args.job_protocol == "immutable":
        state = JobLoopState()
        heartbeat = (Heartbeat(events, args.heartbeat_interval, state=state.snapshot)
                     if events is not None else None)
        if heartbeat is not None:
            heartbeat.start()
        try:
            serve_immutable(inbox, outbox, scratch, timeout=args.timeout,
                            memory_bytes=args.memory_bytes,
                            max_processes=args.max_processes,
                            max_jobs=args.max_jobs, events=events, state=state)
        finally:
            if heartbeat is not None:
                heartbeat.stop()
        return

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
