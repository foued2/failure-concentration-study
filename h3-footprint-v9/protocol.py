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


def publish_job(staging: Path, job: dict[str, Any], body: bytes | None = None) -> Path:
    """Publish exactly one active job. `body` is written once per candidate."""
    staging.mkdir(parents=True, exist_ok=True)
    if body is not None:
        _atomic_write(staging / BODY_FILENAME, body)
    path = staging / JOB_FILENAME
    _atomic_write(path, json.dumps(job, sort_keys=True).encode("utf-8"))
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
