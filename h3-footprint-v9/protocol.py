"""On-disk job/response protocol shared by the host controller and the
secret-free Sandbox supervisor.

Only two payloads ever cross the boundary:

  job.json  - {job_id, sequence, kind, body_sha256, probe_index, input, limits}
  response  - raw observed child status/output, keyed to job_id

Neither contains an expected answer, a family label, or a probe bank.
"""

from __future__ import annotations

import getpass
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

JOB_SCHEMA = 1
BODY_FILENAME = "body.py"
JOB_FILENAME = "job.json"
RESPONSE_DIRNAME = "response"

# Diagnostic telemetry written by the guest agent. It is deliberately *not* part
# of the job protocol: each event is a new, uniquely named file, so the guest
# never has to rename anything inside a mapped folder. Telemetry is evidence of
# what the agent did, never proof that isolation holds.
EVENT_PREFIX = "event-"
EVENT_NAMES = (
    "agent_start",
    "heartbeat",
    "job_discovered",
    "job_started",
    "response_written",
    "exception",
)
EVENT_PHASES = ("startup", "handshake", "serve")
EVENT_LIMIT_BYTES = 4096
EVENT_DETAIL_LIMIT = 512


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
