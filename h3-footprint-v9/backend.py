"""Execution backends: how a published job actually reaches a supervisor.

The controller does not decide *how* a job runs; a transport does. This exists
because the previous revision quietly ran ``supervisor.py`` with the local
Python interpreter while the report described a host/Sandbox boundary.

There are exactly two transports:

``HostLocalTransport``
    Runs the supervisor as a local child process. This is **not** an isolation
    boundary. A low-integrity child running as the same user can still read the
    host repository, including ``oracle.py`` and the frozen
    ``expected_values.json``. ``tests/test_boundary.py::HostBoundaryExposure``
    measures this and asserts the read succeeds, so the weakness is a recorded
    fact rather than an assumption. Rows produced here are marked
    ``authorized: false`` and are never study evidence.

``WindowsSandboxTransport``
    The one-item broker. The host publishes one job into a read-only mapped
    folder, a Sandbox-side agent executes it, and the answer comes back through a
    writable mapped folder. It is usable only after a nonce handshake in which
    the agent proves, from its own token, that it is running inside Windows
    Sandbox.

``Controller.evaluate_authorized`` refuses every transport whose
``isolation_verified`` is not true, so candidate evaluation cannot proceed on
the strength of the local backend.
"""

from __future__ import annotations

import json
import ntpath
import os
import re
import stat
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

import protocol
import winjob

HANDLE_HELLO = "hello.json"
HANDLE_SESSION = "session.json"
RESPONSE_LIMIT_BYTES = 64 * 1024
RESPONSE_STATUSES = {
    "ok", "error", "timeout", "load_error", "output_limit",
    "staging_mismatch", "boundary_error",
}


class FatalBoundaryError(RuntimeError):
    """The measurement boundary failed; the run must stop, not be scored."""


class BoundaryNotEstablished(FatalBoundaryError):
    """Evaluation was attempted on a transport that cannot attest isolation."""


class SandboxConfigError(ValueError):
    """A .wsb config would not launch, or would not enforce the boundary."""


def current_identity() -> dict:
    return winjob.identity()


def validate_handshake(record: dict, nonce: str) -> dict[str, bool]:
    """Every check must pass before a transport may claim Sandbox isolation."""
    return {
        "nonce": record.get("nonce") == nonce,
        "inside_sandbox": record.get("inside_sandbox") is True,
        "account": str(record.get("user", "")).split("\\")[-1].lower() == "wdagutilityaccount",
    }


def _env(scratch: Path) -> dict[str, str]:
    keep = ("PATH", "SYSTEMROOT", "WINDIR", "SYSTEMDRIVE", "COMSPEC",
            "NUMBER_OF_PROCESSORS", "PROCESSOR_ARCHITECTURE", "USERNAME", "USERDOMAIN")
    env = {k: os.environ[k] for k in keep if k in os.environ}
    env.update({"TEMP": str(scratch), "TMP": str(scratch)})
    return env


class HostLocalTransport:
    """Development transport. Explicitly not an isolation boundary."""

    name = "host-local"
    requires_sandbox = False
    isolation_verified = False

    def __init__(self, runtime: Path, python: str | None = None) -> None:
        self.runtime = Path(runtime)
        self.python = python or sys.executable

    def attestation(self) -> dict[str, Any]:
        return {
            "verified": False,
            "transport": self.name,
            "reason": (
                "host-local execution: the candidate runs as the same OS user, so "
                "the host repository and its reference data are readable"
            ),
            "identity": current_identity(),
        }

    def execute(self, staging: Path, response_dir: Path, scratch: Path, *,
                timeout: float, memory_bytes: int, max_processes: int) -> dict[str, Any]:
        cmd = [
            self.python, "-I", str(self.runtime / "supervisor.py"),
            "--staging", str(staging),
            "--response-dir", str(response_dir),
            "--scratch", str(scratch),
            "--timeout", str(timeout),
            "--memory-bytes", str(memory_bytes),
            "--max-processes", str(max_processes),
        ]
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout + 30,
            encoding="utf-8", errors="replace", env=_env(scratch), cwd=str(self.runtime),
        )
        job = protocol.read_job(staging)
        record = protocol.read_response(response_dir, job["job_id"])
        if record is None:
            raise FatalBoundaryError(
                "supervisor produced no response record: " + (proc.stderr or proc.stdout)[-500:]
            )
        return record


class WindowsSandboxTransport:
    """One-item broker over two mapped folders.

    Ordering guarantee: the host publishes job N+1 only after it has received
    response N, and the supervisor publishes a response only after verifying
    that the candidate job object reports zero active processes. A descendant
    that survived N therefore cannot observe N+1.
    """

    name = "windows-sandbox"
    requires_sandbox = True

    def __init__(self, *, handshake_timeout: float = 180.0,
                 response_slack: float = 120.0,
                 job_protocol: str = "legacy") -> None:
        if job_protocol not in ("legacy", "immutable"):
            raise ValueError(f"unknown job protocol {job_protocol!r}")
        self.handshake_timeout = handshake_timeout
        self.response_slack = response_slack
        self.job_protocol = job_protocol
        self._attestation: dict[str, Any] | None = None

    @property
    def isolation_verified(self) -> bool:
        return bool(self._attestation and self._attestation.get("verified"))

    @property
    def nonce(self) -> str | None:
        """The nonce this session was opened with, if any."""
        return getattr(self, "_nonce", None)

    @property
    def outbox(self) -> Path | None:
        """The writable mapping, where responses and events appear."""
        return getattr(self, "_outbox", None)

    def attestation(self) -> dict[str, Any]:
        return self._attestation or {
            "verified": False, "transport": self.name, "reason": "handshake not performed",
        }

    def prepare(self, inbox: Path, outbox: Path) -> str:
        """Write a nonce into the inbox and return it.

        The nonce prevents a stale ``hello.json`` from a previous session being
        replayed as evidence for this one.
        """
        inbox, outbox = Path(inbox), Path(outbox)
        inbox.mkdir(parents=True, exist_ok=True)
        outbox.mkdir(parents=True, exist_ok=True)
        nonce = uuid.uuid4().hex
        protocol._atomic_write(
            inbox / HANDLE_SESSION,
            json.dumps({"v9": protocol.JOB_SCHEMA, "nonce": nonce}, sort_keys=True).encode("utf-8"),
        )
        hello = outbox / HANDLE_HELLO
        if hello.exists():
            hello.unlink()
        self._nonce = nonce
        self._outbox = outbox
        return nonce

    def await_handshake(self) -> dict[str, Any]:
        nonce = getattr(self, "_nonce", None)
        outbox = getattr(self, "_outbox", None)
        if nonce is None or outbox is None:
            raise BoundaryNotEstablished("handshake awaited before prepare()")

        hello = outbox / HANDLE_HELLO
        deadline = time.monotonic() + self.handshake_timeout
        record: dict[str, Any] | None = None
        while time.monotonic() < deadline:
            if hello.exists():
                try:
                    record = json.loads(hello.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    record = None
                if record is not None:
                    break
            time.sleep(0.1)

        if record is None:
            raise BoundaryNotEstablished(
                "no Sandbox handshake: the agent did not write hello.json within "
                f"{self.handshake_timeout:.0f}s"
            )

        checks = validate_handshake(record, nonce)
        verified = all(checks.values())
        self._attestation = {
            "verified": verified,
            "transport": self.name,
            "handshake": "nonce+account",
            "checks": checks,
            "agent": {k: record.get(k) for k in ("user", "computer", "pid", "nonce")},
        }
        if not verified:
            raise BoundaryNotEstablished(
                "Sandbox handshake failed its checks: "
                + ", ".join(f"{k}={v}" for k, v in checks.items())
            )
        return self._attestation

    def start(self, inbox: Path, outbox: Path) -> dict[str, Any]:
        self.prepare(inbox, outbox)
        return self.await_handshake()

    def execute(self, staging: Path, response_dir: Path, scratch: Path, *,
                timeout: float, memory_bytes: int, max_processes: int) -> dict[str, Any]:
        if not self.isolation_verified:
            raise BoundaryNotEstablished(
                "the Sandbox transport has no verified attestation; refusing to execute"
            )
        if self.job_protocol == "immutable":
            scan = protocol.scan_immutable_jobs(staging)
            if scan["errors"]:
                raise FatalBoundaryError(
                    "immutable request is unusable: "
                    + "; ".join(f"{item['file']}: {item['error']}" for item in scan["errors"])
                )
            if not scan["requests"]:
                raise FatalBoundaryError("no immutable request is visible in the staging folder")
            job = scan["requests"][-1]
        else:
            job = protocol.read_job(staging)
        path = protocol.response_path(Path(response_dir), job["job_id"])
        deadline = time.monotonic() + timeout + self.response_slack
        while time.monotonic() < deadline:
            if path.exists():
                # The outbox is candidate-writable, so the file is untrusted
                # input: bounded size, no reparse point, strict schema. A file
                # that exists but is invalid is tampering, not a late response.
                return read_trusted_response(path, job["job_id"])
            time.sleep(0.1)
        raise FatalBoundaryError(
            f"no Sandbox response for job {job['job_id']} within {timeout + self.response_slack:.0f}s"
        )

    def preflight(self, inbox: Path, outbox: Path, *, launch: Any = None) -> dict[str, Any]:
        """Handshake only. Never publishes a job and never evaluates anything.

        ``prepare`` writes ``session.json`` *before* ``launch`` runs, so the agent
        can never start against a missing session. The agent also polls for the
        session, so either order works; this ordering is the deterministic one.
        """
        inbox, outbox = Path(inbox), Path(outbox)
        self.prepare(inbox, outbox)
        session = json.loads((inbox / HANDLE_SESSION).read_text(encoding="utf-8"))

        launched = launch() if launch is not None else None
        attestation = self.await_handshake()

        jobs = sorted(p.name for p in inbox.glob("job.json"))
        responses = sorted(p.name for p in outbox.glob("response-*.json"))
        if jobs or responses:
            raise BoundaryNotEstablished(
                "preflight must not run a job, but found job files "
                f"{jobs} and response files {responses}"
            )

        return {
            "transport": self.name,
            "nonce": session["nonce"],
            "session_written_before_launch": True,
            "launched": launched,
            "attestation": attestation,
            "jobs_published": 0,
            "response_files": [],
            "evaluation_attempted": False,
            "started": time.time(),
        }


# -- what crosses back ---------------------------------------------------------
# The outbox is written by whatever runs inside the Sandbox, so the host has to
# treat it as hostile input, not as data from its own supervisor.


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = os.stat(path, follow_symlinks=False).st_file_attributes
    except (OSError, AttributeError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def validate_response(record: Any, job_id: str | None = None) -> dict[str, Any]:
    """Strict schema for a response that crossed the boundary."""
    if not isinstance(record, dict):
        raise FatalBoundaryError("response is not a JSON object")
    checks = (
        ("v9", int), ("job_id", str), ("sequence", int), ("kind", str),
        ("body_sha256", str), ("status", str), ("tree_empty", bool),
    )
    for key, expected in checks:
        if key not in record:
            raise FatalBoundaryError(f"response is missing {key!r}")
        value = record[key]
        if expected is bool:
            if not isinstance(value, bool):
                raise FatalBoundaryError(f"response field {key!r} is not a boolean")
        elif isinstance(value, bool) or not isinstance(value, expected):
            raise FatalBoundaryError(
                f"response field {key!r} has type {type(value).__name__}"
            )
    answer = record.get("answer")
    if answer is not None and (isinstance(answer, bool) or not isinstance(answer, int)):
        raise FatalBoundaryError(f"response answer has type {type(answer).__name__}")
    if record["v9"] != protocol.JOB_SCHEMA:
        raise FatalBoundaryError("response schema version mismatch")
    if not re.fullmatch(r"[0-9a-f]{32}", record["job_id"]):
        raise FatalBoundaryError("response job_id is not a 32-hex id")
    if not re.fullmatch(r"[0-9a-f]{64}", record["body_sha256"]):
        raise FatalBoundaryError("response body_sha256 is not a 64-hex hash")
    if record["status"] not in RESPONSE_STATUSES:
        raise FatalBoundaryError(f"response status {record['status']!r} is not a known status")
    if job_id is not None and record["job_id"] != job_id:
        raise FatalBoundaryError(
            f"response is for job {record['job_id']}, expected {job_id}"
        )
    if not isinstance(record.get("raw_stdout", ""), str):
        raise FatalBoundaryError("response raw_stdout is not text")
    return record


def read_trusted_response(path: Path, job_id: str | None = None) -> dict[str, Any]:
    path = Path(path)
    if _is_reparse_point(path):
        raise FatalBoundaryError("response file is a reparse point (symlink or junction)")
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise FatalBoundaryError(f"cannot stat response: {exc}") from exc
    if size > RESPONSE_LIMIT_BYTES:
        raise FatalBoundaryError(
            f"response file is {size} bytes, over the {RESPONSE_LIMIT_BYTES}-byte limit"
        )
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FatalBoundaryError(f"response is not valid JSON: {type(exc).__name__}") from exc
    return validate_response(record, job_id)


# -- guest telemetry -----------------------------------------------------------
# The agent writes liveness and lifecycle records into the same outbox as the
# responses, so they arrive through the same untrusted channel and get the same
# treatment: bounded size, no reparse points, an exact schema, correlation with
# the session, and no authority. Telemetry can explain a failure; it can never
# establish isolation.

EVENT_LIMIT_BYTES = protocol.EVENT_LIMIT_BYTES
EVENT_NAME_RE = re.compile(r"^event-([0-9a-f]{32})-(\d{1,10})-(\d{6})-([a-z_]+)\.json$")
_EVENT_HEX32 = re.compile(r"[0-9a-f]{32}")
_EVENT_REQUIRED_KEYS = frozenset({
    "v9", "nonce", "pid", "seq", "event", "phase",
    "timestamp", "job_id", "job_sequence", "detail",
})
_EVENT_OPTIONAL_KEYS = frozenset({"state"})
_EVENT_STATE_KEYS = frozenset(protocol.EVENT_STATE_KEYS)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_event_state(state: Any) -> dict[str, Any]:
    """Strict, bounded shape for a job-loop snapshot."""
    if not isinstance(state, dict):
        raise FatalBoundaryError("event state is not a JSON object")
    keys = set(state)
    if keys != _EVENT_STATE_KEYS:
        missing = sorted(_EVENT_STATE_KEYS - keys)
        extra = sorted(keys - _EVENT_STATE_KEYS)
        raise FatalBoundaryError(
            f"event state keys differ (missing={missing}, unexpected={extra})"
        )
    poll_count = state["poll_count"]
    if not _is_int(poll_count) or poll_count < 0:
        raise FatalBoundaryError("event state poll_count is not a non-negative integer")
    last_poll_at = state["last_poll_at"]
    if poll_count == 0:
        if last_poll_at is not None:
            raise FatalBoundaryError("event state has a poll time but no completed poll")
    elif (isinstance(last_poll_at, bool) or not isinstance(last_poll_at, (int, float))
            or last_poll_at <= 0):
        raise FatalBoundaryError("event state last_poll_at is not a positive number")
    if not isinstance(state["scanned"], bool):
        raise FatalBoundaryError("event state scanned is not a boolean")
    visible = state["visible"]
    if not isinstance(visible, list) or len(visible) > protocol.EVENT_VISIBLE_LIMIT:
        raise FatalBoundaryError("event state visible is not a bounded list")
    for name in visible:
        if not isinstance(name, str) or len(name) > protocol.EVENT_VISIBLE_NAME_LIMIT:
            raise FatalBoundaryError("event state visible entry is not bounded text")
    visible_count = state["visible_count"]
    if not _is_int(visible_count) or visible_count < len(visible):
        raise FatalBoundaryError("event state visible_count is inconsistent")
    if state["outcome"] not in protocol.EVENT_STATE_OUTCOMES:
        raise FatalBoundaryError(f"event state outcome {state['outcome']!r} is not allowed")
    last_job_id = state["last_job_id"]
    if last_job_id is not None and (
        not isinstance(last_job_id, str) or not _EVENT_HEX32.fullmatch(last_job_id)
    ):
        raise FatalBoundaryError("event state last_job_id is neither null nor 32-hex")
    last_job_sequence = state["last_job_sequence"]
    if last_job_sequence is not None and (
        not _is_int(last_job_sequence) or last_job_sequence < 1
    ):
        raise FatalBoundaryError("event state last_job_sequence is neither null nor positive")
    error = state["error"]
    if error is not None and (
        not isinstance(error, str) or len(error) > protocol.EVENT_STATE_ERROR_LIMIT
    ):
        raise FatalBoundaryError("event state error is neither null nor bounded text")
    error_file = state["error_file"]
    if error_file is not None and (
        not isinstance(error_file, str)
        or len(error_file) > protocol.EVENT_VISIBLE_NAME_LIMIT
    ):
        raise FatalBoundaryError("event state error_file is neither null nor bounded text")
    return state


def validate_event(record: Any, *, nonce: str,
                   expected_pid: int | None = None) -> dict[str, Any]:
    """Strict schema for a guest diagnostic event."""
    if not isinstance(record, dict):
        raise FatalBoundaryError("event is not a JSON object")
    keys = set(record)
    missing = sorted(_EVENT_REQUIRED_KEYS - keys)
    extra = sorted(keys - _EVENT_REQUIRED_KEYS - _EVENT_OPTIONAL_KEYS)
    if missing or extra:
        raise FatalBoundaryError(
            f"event keys differ (missing={missing}, unexpected={extra})"
        )
    if record["v9"] != protocol.JOB_SCHEMA or not _is_int(record["v9"]):
        raise FatalBoundaryError("event schema version mismatch")
    if not isinstance(record["nonce"], str) or not _EVENT_HEX32.fullmatch(record["nonce"]):
        raise FatalBoundaryError("event nonce is not a 32-hex id")
    if record["nonce"] != nonce:
        raise FatalBoundaryError("event nonce does not match the session")
    if not _is_int(record["pid"]) or record["pid"] <= 0:
        raise FatalBoundaryError("event pid is not a positive integer")
    if expected_pid is not None and record["pid"] != expected_pid:
        raise FatalBoundaryError(
            f"event pid {record['pid']} does not match the attested agent {expected_pid}"
        )
    if not _is_int(record["seq"]) or record["seq"] < 1:
        raise FatalBoundaryError("event seq is not a positive integer")
    if record["event"] not in protocol.EVENT_NAMES:
        raise FatalBoundaryError(f"event name {record['event']!r} is not allowed")
    if record["phase"] not in protocol.EVENT_PHASES:
        raise FatalBoundaryError(f"event phase {record['phase']!r} is not allowed")
    timestamp = record["timestamp"]
    if isinstance(timestamp, bool) or not isinstance(timestamp, (int, float)) or timestamp <= 0:
        raise FatalBoundaryError("event timestamp is not a positive number")
    job_id = record["job_id"]
    if job_id is not None and (
        not isinstance(job_id, str) or not _EVENT_HEX32.fullmatch(job_id)
    ):
        raise FatalBoundaryError("event job_id is neither null nor a 32-hex id")
    job_sequence = record["job_sequence"]
    if job_sequence is not None and (
        not _is_int(job_sequence) or job_sequence < 1
    ):
        raise FatalBoundaryError("event job_sequence is neither null nor a positive integer")
    detail = record["detail"]
    if detail is not None and (
        not isinstance(detail, str) or len(detail) > protocol.EVENT_DETAIL_LIMIT
    ):
        raise FatalBoundaryError("event detail is neither null nor bounded text")
    if record["event"] == "poll_state" and "state" not in record:
        raise FatalBoundaryError("poll_state event has no state")
    if "state" in record:
        if record["event"] not in ("heartbeat", "poll_state"):
            raise FatalBoundaryError(
                "event state is only allowed on heartbeat or poll_state"
            )
        validate_event_state(record["state"])
        if record["event"] == "poll_state" and record["state"]["poll_count"] < 1:
            raise FatalBoundaryError("poll_state event has no completed poll")
    return record


def read_trusted_event(path: Path, *, nonce: str,
                       expected_pid: int | None = None) -> dict[str, Any]:
    """Read one event and prove its name agrees with its content."""
    path = Path(path)
    match = EVENT_NAME_RE.fullmatch(path.name)
    if match is None:
        raise FatalBoundaryError(f"event filename {path.name!r} is malformed")
    if _is_reparse_point(path):
        raise FatalBoundaryError("event file is a reparse point (symlink or junction)")
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise FatalBoundaryError(f"cannot stat event: {exc}") from exc
    if size > EVENT_LIMIT_BYTES:
        raise FatalBoundaryError(
            f"event file is {size} bytes, over the {EVENT_LIMIT_BYTES}-byte limit"
        )
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FatalBoundaryError(f"event is not valid JSON: {type(exc).__name__}") from exc
    validate_event(record, nonce=nonce, expected_pid=expected_pid)
    name_nonce, name_pid, name_seq, name_event = match.groups()
    if (name_nonce, int(name_pid), int(name_seq), name_event) != (
        record["nonce"], record["pid"], record["seq"], record["event"]
    ):
        raise FatalBoundaryError(
            "event filename disagrees with its content "
            f"({path.name!r} vs nonce/pid/seq/event in the record)"
        )
    return record


def collect_events(outbox: Path, nonce: str, expected_pid: int | None = None) -> dict[str, Any]:
    """Validate every event for this session; report what cannot be trusted.

    A file that is still being written is retried briefly. Anything that stays
    unreadable, carries another nonce, or breaks the schema becomes an anomaly
    rather than an exception: the caller is running a diagnostic and has to be
    able to record *why* the telemetry is unusable.
    """
    outbox = Path(outbox)
    events: list[dict[str, Any]] = []
    anomalies: list[dict[str, str]] = []
    foreign = 0
    if not outbox.is_dir():
        return {"events": [], "anomalies": [{"file": "", "error": "outbox_missing"}],
                "foreign_events": 0, "max_seq": 0, "started_at": None}
    for path in sorted(outbox.iterdir()):
        if not (path.name.startswith(protocol.EVENT_PREFIX) and path.name.endswith(".json")):
            continue
        if EVENT_NAME_RE.fullmatch(path.name) is None:
            anomalies.append({"file": path.name, "error": "malformed_event_name"})
            continue
        if EVENT_NAME_RE.fullmatch(path.name).group(1) != nonce:  # type: ignore[union-attr]
            foreign += 1
            continue
        record = None
        error = ""
        for attempt in range(3):
            try:
                record = read_trusted_event(path, nonce=nonce, expected_pid=expected_pid)
                break
            except FatalBoundaryError as exc:
                error = str(exc)
                if "not valid JSON" in error and attempt < 2:
                    time.sleep(0.05)
                    continue
                break
        if record is None:
            anomalies.append({"file": path.name, "error": error})
        else:
            events.append(record)
    events.sort(key=lambda item: item["seq"])
    for previous, current in zip(events, events[1:]):
        if current["seq"] <= previous["seq"]:
            anomalies.append({
                "file": "",
                "error": f"event sequence is not strictly increasing at seq {current['seq']}",
            })
    pids = sorted({event["pid"] for event in events})
    if len(pids) > 1:
        anomalies.append({"file": "", "error": f"multiple agent pids {pids}"})
    return {
        "events": events,
        "anomalies": anomalies,
        "foreign_events": foreign,
        "max_seq": events[-1]["seq"] if events else 0,
        "started_at": events[0]["timestamp"] if events else None,
        "agent_pids": pids,
    }


# -- .wsb configuration --------------------------------------------------------
# Windows maps a folder into the guest at the Desktop of WDAGUtilityAccount
# unless SandboxFolder says otherwise, so the path is always explicit here.

SANDBOX_DESKTOP = r"C:\Users\WDAGUtilityAccount\Desktop"
SANDBOX_INBOX_NAME = "h3-in"
SANDBOX_OUTBOX_NAME = "h3-out"
SANDBOX_PYTHON_NAME = "h3-py"


def _tokens(command: str) -> list[str]:
    return [quoted or bare for quoted, bare in re.findall(r'"([^"]*)"|(\S+)', command)]


def _norm(path: str) -> str:
    return ntpath.normcase(ntpath.normpath(path))


def _under(path: str, folder: str) -> bool:
    path, folder = _norm(path), _norm(folder)
    return path == folder or path.startswith(folder.rstrip("\\") + "\\")


SANDBOX_CONFIG_TEMPLATE = """<Configuration>
  <Networking>Disable</Networking>
  <ClipboardRedirection>Disable</ClipboardRedirection>
  <vGPU>Disable</vGPU>
  <AudioInput>Disable</AudioInput>
  <VideoInput>Disable</VideoInput>
  <PrinterRedirection>Disable</PrinterRedirection>
  <MemoryInMB>{memory_mb}</MemoryInMB>
  <MappedFolders>
{mappings}
  </MappedFolders>
  <LogonCommand>
    <Command>{command}</Command>
  </LogonCommand>
</Configuration>
"""

MAPPING_TEMPLATE = """    <MappedFolder>
      <HostFolder>{host}</HostFolder>
      <SandboxFolder>{sandbox}</SandboxFolder>
      <ReadOnly>{readonly}</ReadOnly>
    </MappedFolder>"""


def sandbox_config_xml(inbox: Path, outbox: Path, *, python_root: Path,
                       mode: str = "preflight", job_protocol: str = "legacy",
                       sandbox_root: str = SANDBOX_DESKTOP,
                       python_exe_name: str = "python.exe",
                       memory_mb: int = 4096) -> str:
    """Config for Windows Sandbox.

    ``python_root`` is mandatory and is mapped read-only, because the Sandbox
    base image ships no interpreter and an unmapped interpreter path is a config
    that cannot start. The previous revision emitted ``C:\\h3-py\\python.exe``
    while mapping only the inbox and outbox, so the agent could never launch.

    ``job_protocol`` selects the opt-in diagnostic request protocol. Legacy stays
    the default so an ordinary config is unchanged.
    """
    if mode not in ("preflight", "serve"):
        raise SandboxConfigError(f"unknown mode {mode!r}")
    if job_protocol not in ("legacy", "immutable"):
        raise SandboxConfigError(f"unknown job protocol {job_protocol!r}")
    if mode == "preflight" and job_protocol != "legacy":
        raise SandboxConfigError("a handshake-only config cannot select a job protocol")
    python_root = Path(python_root)

    sandbox_inbox = ntpath.join(sandbox_root, SANDBOX_INBOX_NAME)
    sandbox_outbox = ntpath.join(sandbox_root, SANDBOX_OUTBOX_NAME)
    sandbox_python = ntpath.join(sandbox_root, SANDBOX_PYTHON_NAME)
    python_exe = ntpath.join(sandbox_python, python_exe_name)
    agent = ntpath.join(sandbox_inbox, "sandbox_agent.py")

    mappings = "\n".join([
        MAPPING_TEMPLATE.format(host=escape(str(inbox)), sandbox=escape(sandbox_inbox),
                                readonly="true"),
        MAPPING_TEMPLATE.format(host=escape(str(outbox)), sandbox=escape(sandbox_outbox),
                                readonly="false"),
        MAPPING_TEMPLATE.format(host=escape(str(python_root)), sandbox=escape(sandbox_python),
                                readonly="true"),
    ])

    tail = ""
    if mode == "preflight":
        tail = " --handshake-only"
    elif job_protocol == "immutable":
        tail = " --job-protocol immutable"
    command = (
        f'"{python_exe}" "{agent}" --inbox "{sandbox_inbox}" '
        f'--outbox "{sandbox_outbox}"{tail}'
    )

    return SANDBOX_CONFIG_TEMPLATE.format(
        memory_mb=int(memory_mb), mappings=mappings, command=escape(command)
    )


def verify_sandbox_config(xml: str, *, mode: str | None = None,
                          job_protocol: str = "legacy") -> dict[str, Any]:
    """Parse the emitted config and prove it is launchable *and* bounded.

    This is deliberately independent of how the XML was built: it reads what
    would be handed to Windows Sandbox and checks the guest-side paths, not the
    host intent.
    """
    import xml.etree.ElementTree as ET

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as exc:
        raise SandboxConfigError(f"config is not valid XML: {exc}") from exc

    folders = []
    for folder in root.findall("MappedFolders/MappedFolder"):
        folders.append({
            "host": folder.findtext("HostFolder") or "",
            "sandbox": folder.findtext("SandboxFolder") or "",
            "readonly": (folder.findtext("ReadOnly") or "").strip().lower() == "true",
        })
    command = root.findtext("LogonCommand/Command") or ""
    tokens = _tokens(command)

    read_only = [f["sandbox"] for f in folders if f["readonly"]]
    writable = [f["sandbox"] for f in folders if not f["readonly"]]
    host_paths = [f["host"] for f in folders]

    exe = tokens[0] if tokens else ""
    agent = next((t for t in tokens if t.lower().endswith("sandbox_agent.py")), "")

    checks = {
        "parses": True,
        "networking_disabled": (root.findtext("Networking") or "").strip().lower() == "disable",
        "clipboard_disabled": (root.findtext("ClipboardRedirection") or "").strip().lower() == "disable",
        "vgpu_disabled": (root.findtext("vGPU") or "").strip().lower() == "disable",
        "audio_input_disabled": (root.findtext("AudioInput") or "").strip().lower() == "disable",
        "video_input_disabled": (root.findtext("VideoInput") or "").strip().lower() == "disable",
        "printer_disabled": (root.findtext("PrinterRedirection") or "").strip().lower() == "disable",
        "outbox_is_the_only_writable_mapping": len(writable) == 1,
        "at_least_one_read_only_mapping": len(read_only) >= 1,
        "interpreter_mapped_read_only": bool(exe) and any(_under(exe, f) for f in read_only),
        "agent_mapped_read_only": bool(agent) and any(_under(agent, f) for f in read_only),
        "interpreter_is_python": ntpath.basename(exe).lower().startswith("python"),
        "guest_paths_absolute": all(
            ntpath.isabs(f["sandbox"]) and not f["sandbox"].startswith("\\\\") for f in folders
        ),
        "guest_paths_unique": len({_norm(f["sandbox"]) for f in folders}) == len(folders),
        "no_host_path_in_command": not any(
            host and _norm(host) in _norm(command) for host in host_paths
        ),
        "handshake_only_matches_mode": (
            mode is None
            or ("--handshake-only" in command) == (mode == "preflight")
        ),
        "job_protocol_matches": (
            ("--job-protocol immutable" in command) == (job_protocol == "immutable")
        ),
    }
    violations = [name for name, ok in checks.items() if not ok]
    return {"ok": not violations, "checks": checks, "violations": violations,
            "mappings": folders, "command": command}


def interpreter_preflight(python_root: Path, exe_name: str = "python.exe") -> dict[str, Any]:
    """Check, on the host, that the mapped interpreter is actually runnable.

    A mapped Windows *venv* usually keeps absolute paths in ``pyvenv.cfg`` and
    ``python*._pth``, so the portable/embeddable distribution is the supported
    option. The check is about presence and portability, not a guarantee.
    """
    python_root = Path(python_root)
    exe = python_root / exe_name
    files = sorted(p.name for p in python_root.iterdir()) if python_root.is_dir() else []
    lowered = [name.lower() for name in files]
    has_stdlib_zip = any(name.startswith("python") and name.endswith(".zip") for name in lowered)
    has_runtime_dll = any(name.startswith("python3") and name.endswith(".dll") for name in lowered)
    checks = {
        "directory_exists": python_root.is_dir(),
        "interpreter_present": exe.is_file(),
        "stdlib_zip_present": has_stdlib_zip,
        "runtime_dll_present": has_runtime_dll,
        "no_venv_marker": "pyvenv.cfg" not in lowered,
    }
    violations = [name for name, ok in checks.items() if not ok]
    return {"ok": not violations, "checks": checks, "violations": violations,
            "python_root": str(python_root), "python_exe": str(exe),
            "files": files[:40]}


def launch_sandbox(wsb: Path) -> dict[str, Any]:
    """Start Windows Sandbox with this config, detached from the controller."""
    exe = Path(os.environ.get("WINDIR", r"C:\Windows")) / "System32" / "WindowsSandbox.exe"
    if not exe.is_file():
        raise FatalBoundaryError(
            f"Windows Sandbox is not installed on this host ({exe} is absent); "
            "the preflight cannot run here"
        )
    flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    proc = subprocess.Popen([str(exe), str(wsb)], close_fds=True, creationflags=flags)
    return {"launched": True, "pid": proc.pid, "exe": str(exe), "config": str(wsb)}
