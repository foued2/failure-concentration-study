"""Host controller: the only component that owns reference data.

It never imports, compiles or executes candidate code, and it never assumes an
isolation boundary it has not been given. For each probe it:

  1. publishes exactly one active job (one body, one probe input),
  2. hands the job to an explicit transport (host-local, or the Windows Sandbox
     broker),
  3. requires the response record to match the job it published,
  4. requires the candidate process tree to be gone,
  5. only then compares the raw answer against the private oracle and advances.

``evaluate`` produces scoring logic on whatever transport it is given and marks
the result with that transport's isolation status. ``evaluate_authorized`` is the
only entry point that may produce study evidence, and it refuses every transport
that cannot attest Windows Sandbox execution.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import uuid
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import backend  # noqa: E402
import constants  # noqa: E402
import oracle  # noqa: E402
import protocol  # noqa: E402
from backend import BoundaryNotEstablished, FatalBoundaryError  # noqa: E402

HERE = Path(__file__).resolve().parent
SANDBOX_RUNTIME_FILES = (
    "supervisor.py",
    "child_runner.py",
    "protocol.py",
    "winjob.py",
    "sandbox_agent.py",
)

# Infrastructure failures abort the run; candidate misbehaviour does not.
FATAL_STATUSES = {
    "boundary_error",
    "staging_mismatch",
}

__all__ = [
    "Controller",
    "FatalBoundaryError",
    "BoundaryNotEstablished",
    "SANDBOX_RUNTIME_FILES",
    "main",
]


def _invalid(reason: str, body_hash: str, group_id: str | None,
             **boundary: Any) -> dict[str, Any]:
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
        **boundary,
    }


class Controller:
    def __init__(self, work_root: Path | str, *, transport: Any,
                 python: str | None = None,
                 timeout: float = constants.PROBE_TIMEOUT_SECONDS,
                 preflight_timeout: float = constants.PREFLIGHT_TIMEOUT_SECONDS,
                 memory_bytes: int = constants.MEMORY_LIMIT_BYTES,
                 max_processes: int = constants.MAX_PROCESSES_PER_CANDIDATE,
                 case_paths: tuple[Path, Path, Path] | None = None) -> None:
        if transport is None:
            raise TypeError("Controller requires an explicit transport")
        self.work_root = Path(work_root)
        self.work_root.mkdir(parents=True, exist_ok=True)
        self.runtime = self.work_root / "sandbox-runtime"
        self.transport = transport
        self.timeout = timeout
        self.preflight_timeout = preflight_timeout
        self.memory_bytes = memory_bytes
        self.max_processes = max_processes
        self._case_paths = case_paths
        self._sequence = 0
        self._last_tree_empty = True
        self._install_runtime()

    def _install_runtime(self) -> None:
        """Build the Sandbox image: supervisor, child and agent only."""
        self.runtime.mkdir(parents=True, exist_ok=True)
        for name in SANDBOX_RUNTIME_FILES:
            shutil.copy2(HERE / name, self.runtime / name)
        if isinstance(self.transport, backend.HostLocalTransport):
            self.transport.runtime = self.runtime

    # -- boundary helpers ----------------------------------------------------

    def _require_previous_tree_dead(self) -> None:
        if not self._last_tree_empty:
            raise FatalBoundaryError(
                "refusing to publish a new job: previous candidate process tree is not confirmed dead"
            )

    def boundary_status(self) -> dict[str, Any]:
        return {
            "transport": self.transport.name,
            "isolation_verified": self.transport.isolation_verified,
            "attestation": self.transport.attestation(),
            "identity": backend.current_identity(),
        }

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
        if getattr(self.transport, "requires_sandbox", False) and record.get("inside_sandbox") is not True:
            raise FatalBoundaryError(
                "transport claims Sandbox execution but the supervisor did not attest it"
            )
        if record.get("tree_empty") is not True:
            self._last_tree_empty = False
            raise FatalBoundaryError("candidate process tree survived the probe")
        self._last_tree_empty = True
        if record["status"] in FATAL_STATUSES or record["status"].startswith("supervisor_error"):
            raise FatalBoundaryError(f"supervisor reported {record['status']}")

    # -- evaluation ----------------------------------------------------------

    def evaluate(self, body_path: Path | str, group_id: str | None = None) -> dict[str, Any]:
        """Score a body. The row records which boundary produced it."""
        return self._evaluate(body_path, group_id, authorized=False)

    def evaluate_authorized(self, body_path: Path | str,
                            group_id: str | None = None) -> dict[str, Any]:
        """Score a body for study evidence. Requires an attested Sandbox."""
        if not self.transport.isolation_verified:
            raise BoundaryNotEstablished(
                f"transport {self.transport.name!r} cannot attest Windows Sandbox isolation; "
                "refusing authorized evaluation"
            )
        return self._evaluate(body_path, group_id, authorized=True)

    def _evaluate(self, body_path: Path | str, group_id: str | None,
                  *, authorized: bool) -> dict[str, Any]:
        body = Path(body_path).read_bytes()
        body_hash = protocol.sha256_bytes(body)

        if self._case_paths is None:
            case = self.work_root / "case"
            shutil.rmtree(case, ignore_errors=True)
            staging, response_dir, scratch = case / "staging", case / "response", case / "scratch"
        else:
            staging, response_dir, scratch = self._case_paths
        for path in (staging, response_dir, scratch):
            Path(path).mkdir(parents=True, exist_ok=True)

        boundary = {
            "authorized": authorized,
            "transport": self.transport.name,
            "isolation_verified": self.transport.isolation_verified,
        }

        job = self._publish(staging, body, "preflight", None, None)
        record = self.transport.execute(
            staging, response_dir, scratch,
            timeout=self.preflight_timeout, memory_bytes=self.memory_bytes,
            max_processes=self.max_processes,
        )
        self._verify(job, record)
        boundary["execution_inside_sandbox"] = record.get("inside_sandbox") is True
        if record["status"] != "ok":
            return _invalid("load_error:" + str(record.get("error") or record["status"]),
                            body_hash, group_id, **boundary)

        fails: list[bool] = []
        for index, probe in enumerate(oracle.PROBES):
            job = self._publish(staging, body, "probe", index, oracle.probe_input(probe))
            record = self.transport.execute(
                staging, response_dir, scratch,
                timeout=self.timeout, memory_bytes=self.memory_bytes,
                max_processes=self.max_processes,
            )
            self._verify(job, record)

            if record["status"] in ("timeout", "error"):
                fails.append(True)
                continue
            if record["status"] != "ok":
                return _invalid(record["status"], body_hash, group_id, **boundary)

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
            **boundary,
        }


# -- command line -------------------------------------------------------------


def _cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="H3 V9 controller. Candidate evaluation requires Windows Sandbox."
    )
    parser.add_argument("--verify-boundary", action="store_true",
                        help="report whether this process is inside Windows Sandbox")
    parser.add_argument("--write-sandbox-config", metavar="PATH",
                        help="write a .wsb config for the one-item broker")
    parser.add_argument("--inbox", help="host path mapped read-only into the Sandbox")
    parser.add_argument("--outbox", help="host path mapped writable into the Sandbox")
    parser.add_argument("--bodies", help="directory of candidate .py files to evaluate")
    parser.add_argument("--work-root", default=str(Path("runs") / "current"))
    parser.add_argument("--group-id", default=None)
    parser.add_argument("--transport", choices=("sandbox", "host-local"), default="host-local")
    parser.add_argument("--allow-host-local", action="store_true",
                        help="score bodies on the host for unit testing; rows are not study evidence")
    args = parser.parse_args(argv)

    if args.verify_boundary:
        ident = backend.current_identity()
        payload = {
            "identity": ident,
            "inside_sandbox": ident["inside_sandbox"],
            "evaluation_authorized": ident["inside_sandbox"],
            "note": "authorized evaluation additionally needs a completed nonce handshake",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if ident["inside_sandbox"] else 2

    if args.write_sandbox_config:
        if not (args.inbox and args.outbox):
            parser.error("--write-sandbox-config requires --inbox and --outbox")
        xml = backend.sandbox_config_xml(Path(args.inbox), Path(args.outbox))
        target = Path(args.write_sandbox_config)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(xml, encoding="utf-8")
        print(f"wrote {target}")
        print("note: the Sandbox image ships no Python; stage a portable interpreter "
              "or edit python_exe in the config before launching")
        return 0

    if not args.bodies:
        parser.error("nothing to do: pass --verify-boundary, --write-sandbox-config or --bodies")

    if args.transport == "host-local" and not args.allow_host_local:
        print("refusing to evaluate on the host: host-local execution is not an isolation "
              "boundary and the candidate can read oracle.py. Use --transport sandbox, or "
              "pass --allow-host-local for scoring-logic tests only.", file=sys.stderr)
        return 2

    bodies = sorted(Path(args.bodies).glob("*.py"))
    if not bodies:
        parser.error(f"no .py files in {args.bodies}")

    work_root = Path(args.work_root)
    if args.transport == "sandbox":
        if not (args.inbox and args.outbox):
            parser.error("--transport sandbox requires --inbox and --outbox")
        transport = backend.WindowsSandboxTransport()
        transport.start(Path(args.inbox), Path(args.outbox))
        ctl = Controller(work_root, transport=transport,
                         case_paths=(Path(args.inbox), Path(args.outbox),
                                     work_root / "sandbox-scratch"))
    else:
        transport = backend.HostLocalTransport(work_root / "sandbox-runtime")
        ctl = Controller(work_root, transport=transport)

    print(json.dumps(ctl.boundary_status(), sort_keys=True))
    status = 0
    for body in bodies:
        row = (ctl.evaluate_authorized(body, group_id=args.group_id)
               if ctl.transport.isolation_verified
               else ctl.evaluate(body, group_id=args.group_id))
        print(json.dumps(row, sort_keys=True))
        if row["excluded"]:
            status = 2
    return status


def main() -> None:
    raise SystemExit(_cli())


if __name__ == "__main__":
    main()
