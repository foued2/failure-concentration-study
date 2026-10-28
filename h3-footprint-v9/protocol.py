"""On-disk job/response protocol shared by the host controller and the
secret-free Sandbox supervisor.

Only two payloads ever cross the boundary:

  job.json  - {job_id, sequence, kind, body_sha256, probe_index, input, limits}
  response  - raw observed child status/output, keyed to job_id

Neither contains an expected answer, a family label, or a probe bank.

An opt-in diagnostic variant replaces the single ``job.json`` with one immutable
``job-<sequence>-<job_id>.json`` per request and a content-addressed body under
``bodies/<sha256>.py``. Nothing in that variant is renamed or overwritten. It is
selected explicitly (``--job-protocol immutable``) and is not the default.
"""

from __future__ import annotations

import getpass
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

JOB_SCHEMA = 1
BODY_FILENAME = "body.py"
JOB_FILENAME = "job.json"
RESPONSE_DIRNAME = "response"

# Experimental, opt-in request protocol. Each job is published under a new,
# immutable filename and is never overwritten or renamed; bodies are keyed by
# their content hash. This exists to test whether in-place updates are the reason
# the guest never saw the second job. It is not the default path.
IMMUTABLE_JOB_PREFIX = "job-"
IMMUTABLE_BODY_DIRNAME = "bodies"
IMMUTABLE_JOB_RE = re.compile(r"^job-(\d{6})-([0-9a-f]{32})\.json$")
IMMUTABLE_VISIBLE_LIMIT = 8
IMMUTABLE_SCAN_LIMIT = 256


class ImmutableJobError(ValueError):
    """A request file is malformed, duplicated, out of order or not immutable."""

    def __init__(self, category: str, detail: str = "") -> None:
        self.category = category
        super().__init__(f"{category}: {detail}" if detail else category)

# Diagnostic telemetry written by the guest agent. It is deliberately *not* part
# of the job protocol: each event is a new, uniquely named file, so the guest
# never has to rename anything inside a mapped folder. Telemetry is evidence of
# what the agent did, never proof that isolation holds.
EVENT_PREFIX = "event-"
EVENT_NAMES = (
    "agent_start",
    "heartbeat",
    "poll_state",
    "job_discovered",
    "job_started",
    "response_written",
    "exception",
)
EVENT_PHASES = ("startup", "handshake", "serve")
EVENT_LIMIT_BYTES = 4096
EVENT_DETAIL_LIMIT = 512

# Bounded job-loop observation carried by ``poll_state`` events, and copied into
# a heartbeat as the last known snapshot. It describes what the loop saw; it is
# not a claim about mapped-folder guarantees.
EVENT_STATE_KEYS = (
    "poll_count",
    "last_poll_at",
    "scanned",
    "visible",
    "visible_count",
    "outcome",
    "last_job_id",
    "last_job_sequence",
    "error",
    "error_file",
)
EVENT_STATE_OUTCOMES = ("new_job", "only_handled", "no_jobs", "out_of_order", "error")
EVENT_VISIBLE_LIMIT = 8
EVENT_VISIBLE_NAME_LIMIT = 64
EVENT_STATE_ERROR_LIMIT = 160


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def _direct_write(path: Path, data: bytes) -> None:
    """Write the final name in place, with no temporary file and no rename.

    A folder mapped into a *running* Windows Sandbox rejects ``os.replace`` with
    ``WinError 32`` (the guest's view holds the source file), so the host cannot
    use the atomic rename path there. The reader is still protected by ordering:
    the body is flushed and closed before ``job.json`` appears, and the agent
    retries any job it cannot parse yet.
    """
    with open(path, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())


def publish_job(staging: Path, job: dict[str, Any], body: bytes | None = None, *,
                atomic: bool = True) -> Path:
    """Publish exactly one active job. `body` is written once per candidate."""
    write = _atomic_write if atomic else _direct_write
    staging.mkdir(parents=True, exist_ok=True)
    if body is not None:
        write(staging / BODY_FILENAME, body)
    path = staging / JOB_FILENAME
    write(path, json.dumps(job, sort_keys=True).encode("utf-8"))
    return path


def read_job(staging: Path) -> dict[str, Any]:
    job = json.loads((staging / JOB_FILENAME).read_text(encoding="utf-8"))
    if job.get("v9") != JOB_SCHEMA:
        raise ValueError("unsupported job schema")
    return job


# -- immutable per-job request protocol ---------------------------------------


def immutable_job_filename(sequence: int, job_id: str) -> str:
    if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
        raise ImmutableJobError("bad_sequence", repr(sequence))
    if not isinstance(job_id, str) or not re.fullmatch(r"[0-9a-f]{32}", job_id):
        raise ImmutableJobError("bad_job_id", repr(job_id))
    return f"{IMMUTABLE_JOB_PREFIX}{sequence:06d}-{job_id}.json"


def immutable_body_relpath(body_sha256: str) -> str:
    if not isinstance(body_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", body_sha256):
        raise ImmutableJobError("bad_body_hash", repr(body_sha256))
    return f"{IMMUTABLE_BODY_DIRNAME}/{body_sha256}.py"


def immutable_body_path(inbox: Path, body_sha256: str) -> Path:
    return Path(inbox) / immutable_body_relpath(body_sha256)


def _exclusive_write(path: Path, data: bytes) -> None:
    """Create a file that must not already exist; write, flush and close it."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    fd = os.open(path, flags, 0o600)
    try:
        fh = os.fdopen(fd, "wb")
        fd = -1
        try:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        finally:
            fh.close()
    finally:
        if fd != -1:
            os.close(fd)


def _validate_job_payload(job: Any) -> dict[str, Any]:
    if not isinstance(job, dict):
        raise ImmutableJobError("bad_schema", "job is not an object")
    if job.get("v9") != JOB_SCHEMA or isinstance(job.get("v9"), bool):
        raise ImmutableJobError("bad_schema", "unsupported version")
    for key, expected in (("job_id", str), ("kind", str), ("body_sha256", str)):
        if not isinstance(job.get(key), expected):
            raise ImmutableJobError("bad_schema", f"{key} has the wrong type")
    sequence = job.get("sequence")
    if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
        raise ImmutableJobError("bad_sequence", repr(sequence))
    immutable_job_filename(sequence, job["job_id"])
    immutable_body_relpath(job["body_sha256"])
    if not isinstance(job.get("input"), dict):
        raise ImmutableJobError("bad_schema", "input is not an object")
    return job


def publish_immutable_job(inbox: Path, job: dict[str, Any], body: bytes) -> Path:
    """Publish one request under a name that can never be reused.

    Ordering matches the legacy publisher: the immutable body is written and
    closed first, then the final job filename appears. Nothing is renamed and
    nothing is overwritten, so a guest that rescans cannot observe a torn update
    of an existing request.
    """
    inbox = Path(inbox)
    job = _validate_job_payload(job)
    if sha256_bytes(body) != job["body_sha256"]:
        raise ImmutableJobError("body_hash_mismatch", job["job_id"])

    inbox.mkdir(parents=True, exist_ok=True)
    body_path = immutable_body_path(inbox, job["body_sha256"])
    body_path.parent.mkdir(parents=True, exist_ok=True)
    if body_path.exists():
        if body_path.read_bytes() != body:
            raise ImmutableJobError("body_conflict", body_path.name)
    else:
        try:
            _exclusive_write(body_path, body)
        except FileExistsError:
            if body_path.read_bytes() != body:
                raise ImmutableJobError("body_conflict", body_path.name) from None

    path = inbox / immutable_job_filename(job["sequence"], job["job_id"])
    try:
        _exclusive_write(path, json.dumps(job, sort_keys=True).encode("utf-8"))
    except FileExistsError:
        raise ImmutableJobError("job_already_exists", path.name) from None
    return path


def read_immutable_job(path: Path, *, expected_sequence: int | None = None) -> dict[str, Any]:
    """Parse a request and prove its filename agrees with its payload."""
    path = Path(path)
    match = IMMUTABLE_JOB_RE.fullmatch(path.name)
    if match is None:
        raise ImmutableJobError("bad_filename", path.name)
    name_sequence, name_job_id = int(match.group(1)), match.group(2)
    try:
        job = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ImmutableJobError("unreadable", f"{path.name}: {type(exc).__name__}") from exc
    job = _validate_job_payload(job)
    if job["sequence"] != name_sequence or job["job_id"] != name_job_id:
        raise ImmutableJobError(
            "filename_payload_mismatch",
            f"{path.name} vs sequence={job['sequence']} job_id={job['job_id']}",
        )
    if expected_sequence is not None and job["sequence"] != expected_sequence:
        raise ImmutableJobError(
            "out_of_order", f"{path.name} is sequence {job['sequence']}, expected {expected_sequence}"
        )
    return job


def scan_immutable_jobs(inbox: Path) -> dict[str, Any]:
    """List and parse request files once, without trusting any of them.

    A file that is still being written shows up as an ``unreadable`` error and is
    retried on the next poll by the caller; it is never executed. Duplicate ids
    and two different ids claiming the same sequence are errors, not races to
    resolve silently.
    """
    inbox = Path(inbox)
    result: dict[str, Any] = {
        "scanned": False, "visible": [], "visible_count": 0,
        "requests": [], "errors": [], "truncated": False, "scan_error": None,
    }
    try:
        names = sorted(
            child.name for child in inbox.iterdir()
            if child.is_file()
            and child.name.startswith(IMMUTABLE_JOB_PREFIX)
            and child.name.endswith(".json")
        )
    except OSError as exc:
        result["scan_error"] = type(exc).__name__
        return result

    result["scanned"] = True
    result["visible_count"] = len(names)
    result["visible"] = names[:IMMUTABLE_VISIBLE_LIMIT]
    if len(names) > IMMUTABLE_SCAN_LIMIT:
        result["truncated"] = True
        names = names[:IMMUTABLE_SCAN_LIMIT]

    by_id: dict[str, dict[str, Any]] = {}
    by_sequence: dict[int, dict[str, Any]] = {}
    for name in names:
        try:
            job = read_immutable_job(inbox / name)
        except ImmutableJobError as exc:
            result["errors"].append({"file": name, "error": exc.category, "detail": str(exc)[:160]})
            continue
        if job["job_id"] in by_id:
            result["errors"].append({
                "file": name, "error": "duplicate_job_id",
                "detail": f"job_id {job['job_id']} already seen in {by_id[job['job_id']]['sequence']}",
            })
            continue
        if job["sequence"] in by_sequence:
            result["errors"].append({
                "file": name, "error": "conflicting_sequence",
                "detail": f"sequence {job['sequence']} already used by {by_sequence[job['sequence']]['job_id']}",
            })
            continue
        by_id[job["job_id"]] = job
        by_sequence[job["sequence"]] = job
    result["requests"] = [by_sequence[key] for key in sorted(by_sequence)]
    return result


def response_path(response_dir: Path, job_id: str) -> Path:
    return response_dir / f"response-{job_id}.json"


def write_response_exclusive(response_dir: Path, record: dict[str, Any]) -> Path:
    """Publish a response that cannot overwrite an existing one."""
    response_dir.mkdir(parents=True, exist_ok=True)
    path = response_path(response_dir, record["job_id"])
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, json.dumps(record, sort_keys=True).encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    return path


def read_response(response_dir: Path, job_id: str) -> dict[str, Any] | None:
    path = response_path(response_dir, job_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def event_filename(nonce: str, pid: int, seq: int, name: str) -> str:
    """Name an event so its order and origin are readable without its content."""
    if name not in EVENT_NAMES:
        raise ValueError(f"unknown event name {name!r}")
    return f"{EVENT_PREFIX}{nonce}-{int(pid)}-{int(seq):06d}-{name}.json"


def write_event(directory: Path, record: dict[str, Any]) -> Path:
    """Publish one diagnostic event as a new file.

    A mapped folder rejects renames, so the final name is written directly and
    closed. Nothing is ever overwritten: the sequence number is unique per agent
    process, which is why a duplicate name means two writers.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / event_filename(
        record["nonce"], record["pid"], record["seq"], record["event"]
    )
    _direct_write(path, json.dumps(record, sort_keys=True).encode("utf-8"))
    return path


# --- Windows directory lock -------------------------------------------------
# A candidate must not be able to write or replace the response record or the
# active job while it runs. Read-only mappings are not a write boundary.


def _icacls(path: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["icacls", str(path), *args],
        capture_output=True, text=True, timeout=60,
        encoding="utf-8", errors="replace",
    )


def current_user() -> str:
    return os.environ.get("USERNAME") or os.environ.get("USER") or getpass.getuser()


def lock_dir(path: Path) -> dict[str, Any]:
    if sys.platform != "win32":
        return {"ok": True, "skipped": "non-windows"}
    user = current_user()
    if not user:
        return {"ok": False, "errors": ["no USERNAME"]}
    proc = _icacls(path, "/deny", f"{user}:(OI)(CI)(WD,AD,DE,DC)")
    return {"ok": proc.returncode == 0, "errors": [proc.stderr.strip()] if proc.returncode else []}


def unlock_dir(path: Path) -> dict[str, Any]:
    if sys.platform != "win32":
        return {"ok": True, "skipped": "non-windows"}
    user = current_user()
    proc = _icacls(path, "/remove:d", user, "/T")
    return {"ok": proc.returncode == 0, "errors": [proc.stderr.strip()] if proc.returncode else []}


def wait_for(predicate, timeout: float, interval: float = 0.02) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()
