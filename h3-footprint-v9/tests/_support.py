from __future__ import annotations

import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import constants  # noqa: E402
import oracle  # noqa: E402
import protocol  # noqa: E402
import supervisor  # noqa: E402

FIXTURES = HERE / "fixtures"


def fixture(name: str) -> Path:
    return FIXTURES / name


def direct_job(body_path: Path, workdir: Path, *, timeout: float = 1.0,
               kind: str = "probe", index: int = 0,
               max_processes: int = 8) -> tuple[dict, Path, Path, Path]:
    body = body_path.read_bytes()
    staging, response, scratch = workdir / "staging", workdir / "response", workdir / "scratch"
    job = {
        "v9": protocol.JOB_SCHEMA,
        "job_id": uuid.uuid4().hex,
        "sequence": 1,
        "kind": kind,
        "body_sha256": protocol.sha256_bytes(body),
        "probe_index": index if kind == "probe" else None,
        "input": oracle.probe_input(oracle.PROBES[index]) if kind == "probe" else None,
        "limits": {
            "max_stdout_bytes": constants.MAX_CHILD_STDOUT_BYTES,
            "memory_bytes": constants.MEMORY_LIMIT_BYTES,
            "max_processes": max_processes,
        },
    }
    protocol.publish_job(staging, job, body=body)
    return job, staging, response, scratch


def run_direct(body_path: Path, workdir: Path, *, timeout: float = 1.0,
               index: int = 0, max_processes: int = 8) -> dict:
    job, staging, response, scratch = direct_job(
        body_path, workdir, timeout=timeout, index=index, max_processes=max_processes
    )
    return supervisor.run_job(
        staging, response, scratch, timeout=timeout,
        memory_bytes=constants.MEMORY_LIMIT_BYTES, max_processes=max_processes,
    )
