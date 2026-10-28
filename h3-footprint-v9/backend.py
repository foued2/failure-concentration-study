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
import os
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


class FatalBoundaryError(RuntimeError):
    """The measurement boundary failed; the run must stop, not be scored."""


class BoundaryNotEstablished(FatalBoundaryError):
    """Evaluation was attempted on a transport that cannot attest isolation."""


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
                 response_slack: float = 120.0) -> None:
        self.handshake_timeout = handshake_timeout
        self.response_slack = response_slack
        self._attestation: dict[str, Any] | None = None

    @property
    def isolation_verified(self) -> bool:
        return bool(self._attestation and self._attestation.get("verified"))

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
        job = protocol.read_job(staging)
        path = protocol.response_path(Path(response_dir), job["job_id"])
        deadline = time.monotonic() + timeout + self.response_slack
        while time.monotonic() < deadline:
            if path.exists():
                try:
                    return json.loads(path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    pass
            time.sleep(0.1)
        raise FatalBoundaryError(
            f"no Sandbox response for job {job['job_id']} within {timeout + self.response_slack:.0f}s"
        )


SANDBOX_CONFIG_TEMPLATE = """<Configuration>
  <Networking>Disable</Networking>
  <ClipboardRedirection>Disable</ClipboardRedirection>
  <vGPU>Disable</vGPU>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>{inbox}</HostFolder>
      <SandboxFolder>{sandbox_inbox}</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>{outbox}</HostFolder>
      <SandboxFolder>{sandbox_outbox}</SandboxFolder>
      <ReadOnly>false</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>{python} {sandbox_inbox}\\sandbox_agent.py --inbox {sandbox_inbox} --outbox {sandbox_outbox}</Command>
  </LogonCommand>
</Configuration>
"""


def sandbox_config_xml(inbox: Path, outbox: Path, *,
                       sandbox_inbox: str = r"C:\h3-in",
                       sandbox_outbox: str = r"C:\h3-out",
                       python_exe: str = r"C:\h3-py\python.exe") -> str:
    """Config for Windows Sandbox.

    The Sandbox base image ships no Python interpreter. ``python_exe`` must be a
    portable interpreter staged into the read-only mapping, or an interpreter
    installed in the image. This is a preflight requirement, not something the
    config can arrange on its own.
    """
    return SANDBOX_CONFIG_TEMPLATE.format(
        inbox=escape(str(inbox)),
        outbox=escape(str(outbox)),
        sandbox_inbox=escape(sandbox_inbox),
        sandbox_outbox=escape(sandbox_outbox),
        python=escape(python_exe),
    )
