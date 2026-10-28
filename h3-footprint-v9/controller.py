"""Host controller: the only component that owns reference data.

It never imports, compiles or executes candidate code. For each probe it:

  1. publishes exactly one active job (one body, one probe input),
  2. invokes the secret-free supervisor,
  3. requires the response record to match the job it published,
  4. requires the candidate process tree to be gone,
  5. only then compares the raw answer against the private oracle and advances.

A forged or tampered response can at most produce a wrong answer or an
invalidation. It cannot produce a correct answer, because the value it would
have to forge is not present anywhere in the Sandbox.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

import constants
import oracle
import protocol

HERE = Path(__file__).resolve().parent
SANDBOX_RUNTIME_FILES = ("supervisor.py", "child_runner.py", "protocol.py", "winjob.py")

# Infrastructure failures abort the run; candidate misbehaviour does not.
FATAL_STATUSES = {
    "boundary_error",
    "staging_mismatch",
}


class FatalBoundaryError(RuntimeError):
    """The measurement boundary failed; the run must stop, not be scored."""


def _invalid(reason: str, body_hash: str, group_id: str | None) -> dict[str, Any]:
    return {
        "body_sha256": body_hash,
        "group_id": group_id,
        "excluded": reason,
        "fails": None,
        "family_counts": None,
        "k": None,
        "C": None,
        "max_f": None,
        "eligible": False,
        "saturated": None,
        "probes_completed": 0,
    }


class Controller:
    def __init__(self, work_root: Path | str, *, python: str | None = None,
                 timeout: float = constants.PROBE_TIMEOUT_SECONDS,
                 preflight_timeout: float = constants.PREFLIGHT_TIMEOUT_SECONDS,
                 memory_bytes: int = constants.MEMORY_LIMIT_BYTES,
                 max_processes: int = constants.MAX_PROCESSES_PER_CANDIDATE) -> None:
        self.work_root = Path(work_root)
        self.work_root.mkdir(parents=True, exist_ok=True)
        self.runtime = self.work_root / "sandbox-runtime"
        self.python = python or sys.executable
        self.timeout = timeout
        self.preflight_timeout = preflight_timeout
        self.memory_bytes = memory_bytes
        self.max_processes = max_processes
        self._sequence = 0
        self._last_tree_empty = True
        self._install_runtime()

    def _install_runtime(self) -> None:
        """Build the Sandbox image: supervisor + child only, no oracle."""
        self.runtime.mkdir(parents=True, exist_ok=True)
        for name in SANDBOX_RUNTIME_FILES:
            shutil.copy2(HERE / name, self.runtime / name)

    # -- boundary helpers ----------------------------------------------------

    def _env(self, scratch: Path) -> dict[str, str]:
        keep = ("PATH", "SYSTEMROOT", "WINDIR", "SYSTEMDRIVE", "COMSPEC",
                "NUMBER_OF_PROCESSORS", "PROCESSOR_ARCHITECTURE",
                "USERNAME", "USERDOMAIN")
        env = {k: os.environ[k] for k in keep if k in os.environ}
        env.update({"TEMP": str(scratch), "TMP": str(scratch)})
        return env

    def _require_previous_tree_dead(self) -> None:
        if not self._last_tree_empty:
            raise FatalBoundaryError(
                "refusing to publish a new job: previous candidate process tree is not confirmed dead"
            )

    def _run_supervisor(self, staging: Path, response_dir: Path, scratch: Path,
                        timeout: float) -> dict[str, Any]:
        cmd = [
            self.python, "-I", str(self.runtime / "supervisor.py"),
            "--staging", str(staging),
            "--response-dir", str(response_dir),
            "--scratch", str(scratch),
            "--timeout", str(timeout),
            "--memory-bytes", str(self.memory_bytes),
            "--max-processes", str(self.max_processes),
        ]
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout + 30,
            encoding="utf-8", errors="replace", env=self._env(scratch), cwd=str(self.runtime),
        )
        job = protocol.read_job(staging)
        record = protocol.read_response(response_dir, job["job_id"])
        if record is None:
            raise FatalBoundaryError(
                "supervisor produced no response record: " + (proc.stderr or proc.stdout)[-500:]
            )
        return record

    def _publish(self, staging: Path, body: bytes, kind: str, probe_index: int | None,
                 job_input: dict | None) -> dict[str, Any]:
        self._require_previous_tree_dead()
        self._sequence += 1
        job = {
            "v9": protocol.JOB_SCHEMA,
            "job_id": uuid.uuid4().hex,
            "sequence": self._sequence,
            "kind": kind,
            "body_sha256": protocol.sha256_bytes(body),
            "probe_index": probe_index,
            "input": job_input,
            "limits": {
                "max_stdout_bytes": constants.MAX_CHILD_STDOUT_BYTES,
                "memory_bytes": self.memory_bytes,
                "max_processes": self.max_processes,
            },
        }
        protocol.publish_job(staging, job, body=body)
        return job

    def _verify(self, job: dict[str, Any], record: dict[str, Any]) -> None:
        checks = {
            "job_id": job["job_id"],
            "sequence": job["sequence"],
            "kind": job["kind"],
            "body_sha256": job["body_sha256"],
            "probe_index": job["probe_index"],
        }
        for key, expected in checks.items():
            if record.get(key) != expected:
                raise FatalBoundaryError(
                    f"response does not match published job: {key} {record.get(key)!r} != {expected!r}"
                )
        if record.get("tree_empty") is not True:
            self._last_tree_empty = False
            raise FatalBoundaryError("candidate process tree survived the probe")
        self._last_tree_empty = True
        if record["status"] in FATAL_STATUSES or record["status"].startswith("supervisor_error"):
            raise FatalBoundaryError(f"supervisor reported {record['status']}")

    # -- evaluation ----------------------------------------------------------

    def evaluate(self, body_path: Path | str, group_id: str | None = None) -> dict[str, Any]:
        body = Path(body_path).read_bytes()
        body_hash = protocol.sha256_bytes(body)

        case = self.work_root / "case"
        shutil.rmtree(case, ignore_errors=True)
        staging, response_dir, scratch = case / "staging", case / "response", case / "scratch"
        for path in (staging, response_dir, scratch):
            path.mkdir(parents=True, exist_ok=True)

        job = self._publish(staging, body, "preflight", None, None)
        record = self._run_supervisor(staging, response_dir, scratch, self.preflight_timeout)
        self._verify(job, record)
        if record["status"] != "ok":
            return _invalid("load_error:" + str(record.get("error") or record["status"]),
                            body_hash, group_id)

        fails: list[bool] = []
        for index, probe in enumerate(oracle.PROBES):
            job = self._publish(staging, body, "probe", index, oracle.probe_input(probe))
            record = self._run_supervisor(staging, response_dir, scratch, self.timeout)
            self._verify(job, record)

            if record["status"] in ("timeout", "error"):
                fails.append(True)
                continue
            if record["status"] != "ok":
                return _invalid(record["status"], body_hash, group_id)

            fails.append(not oracle.answer_is_correct(record.get("answer"), index))

        scored = oracle.score(fails)
        return {
            "body_sha256": body_hash,
            "group_id": group_id,
            "excluded": None,
            "fails": fails,
            "family_counts": scored["family_counts"],
            "k": scored["k"],
            "C": scored["C"],
            "max_f": scored["max_f"],
            "eligible": scored["eligible"],
            "saturated": scored["saturated"],
            "probes_completed": len(fails),
        }
