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
import time
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
    "stage_runtime",
    "run_rendezvous",
    "main",
]


def stage_runtime(dest: Path | str, *, verify_only: bool = False) -> list[str]:
    """Copy the secret-free runtime into a staging or inbox directory.

    Staging is idempotent. Files that already match are left untouched, because
    a running Sandbox holds its mapped folders open and the host cannot overwrite
    them: attempting the copy produced ``WinError 32`` on a live mapping.
    ``verify_only`` turns a mismatch into a boundary error instead of a write.
    """
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for name in SANDBOX_RUNTIME_FILES:
        source = HERE / name
        target = dest / name
        identical = target.is_file() and target.read_bytes() == source.read_bytes()
        if identical:
            continue
        if verify_only:
            raise backend.FatalBoundaryError(
                f"{target} is missing or differs from {source}; restage the runtime "
                "before launching the Sandbox, because a live mapping cannot be "
                "overwritten from the host"
            )
        try:
            shutil.copy2(source, target)
        except PermissionError as exc:
            raise backend.FatalBoundaryError(
                f"cannot restage {target}: a running Sandbox holds the mapped folder "
                f"open ({exc}); close the Sandbox, restage, then launch it again"
            ) from exc
    return list(SANDBOX_RUNTIME_FILES)


def _case_dirs(ctl: "Controller", name: str) -> tuple[Path, Path, Path]:
    if ctl._case_paths is not None:
        staging, response, scratch = (Path(p) for p in ctl._case_paths)
    else:
        root = ctl.work_root / name
        staging, response, scratch = root / "staging", root / "response", root / "scratch"
    for path in (staging, response, scratch):
        path.mkdir(parents=True, exist_ok=True)
    return staging, response, scratch


def run_rendezvous(ctl: "Controller", body_path: Path | str, *,
                   token_a: int = 111, token_b: int = 222) -> dict[str, Any]:
    """Publish token A, confirm its tree is gone, then publish token B.

    The answer the host receives proves which token the candidate saw, so a
    mapping that exposed B early would surface as ``token`` = B in A's response.
    ``Controller._verify`` refuses to continue unless the previous process tree
    is confirmed dead, which is what makes this ordering testable at all.
    """
    body = Path(body_path).read_bytes()
    staging, response_dir, scratch = _case_dirs(ctl, "rendezvous")
    started = time.time()
    events: list[dict[str, Any]] = []

    def stamp(event: str, **fields: Any) -> None:
        events.append({"at": round(time.time() - started, 4), "event": event, **fields})

    def publish(token: int) -> dict[str, Any]:
        job = ctl._publish(staging, body, "system", None,
                           {"n": token, "edges": [], "s": 0, "t": 0})
        return job

    def visible_token() -> str:
        try:
            return (staging / protocol.JOB_FILENAME).read_text(encoding="utf-8")
        except OSError:
            return ""

    job_a = publish(token_a)
    stamp("publish_A", job_id=job_a["job_id"], token=token_a,
          token_b_visible=str(token_b) in visible_token())

    record_a = ctl.transport.execute(
        staging, response_dir, scratch,
        timeout=ctl.preflight_timeout, memory_bytes=ctl.memory_bytes,
        max_processes=ctl.max_processes,
    )
    ctl._verify(job_a, record_a)
    stamp("response_A", job_id=job_a["job_id"], token_seen=record_a.get("answer"),
          status=record_a["status"], tree_empty=record_a["tree_empty"])

    token_b_visible_before_publish = str(token_b) in visible_token()
    stamp("tree_empty_confirmed", job_id=job_a["job_id"],
          token_b_visible=token_b_visible_before_publish)

    job_b = publish(token_b)
    stamp("publish_B", job_id=job_b["job_id"], token=token_b)
    record_b = ctl.transport.execute(
        staging, response_dir, scratch,
        timeout=ctl.preflight_timeout, memory_bytes=ctl.memory_bytes,
        max_processes=ctl.max_processes,
    )
    ctl._verify(job_b, record_b)
    stamp("response_B", job_id=job_b["job_id"], token_seen=record_b.get("answer"),
          status=record_b["status"], tree_empty=record_b["tree_empty"])

    checks = {
        "A_answered_with_A": record_a.get("answer") == token_a,
        "A_tree_empty": record_a.get("tree_empty") is True,
        "B_not_visible_before_A_completed": not token_b_visible_before_publish,
        "B_answered_with_B": record_b.get("answer") == token_b,
        "B_tree_empty": record_b.get("tree_empty") is True,
        "distinct_tokens": token_a != token_b,
        "transport_attested": ctl.transport.isolation_verified,
    }
    return {
        "checks": checks,
        "ordering_ok": all(checks[key] for key in checks
                           if key != "transport_attested"),
        "attested": checks["transport_attested"],
        "transport": ctl.transport.name,
        "tokens": {"A": token_a, "B": token_b},
        "events": events,
    }


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
        stage_runtime(self.runtime)
        if isinstance(self.transport, backend.HostLocalTransport):
            self.transport.runtime = self.runtime
        elif self._case_paths is not None:
            # The agent itself must arrive through the read-only inbox mapping.
            # Once that mapping is live the guest holds the files open, so staging
            # here is a verification step, not a rewrite.
            stage_runtime(self._case_paths[0],
                          verify_only=self.transport.isolation_verified)

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
        protocol.publish_job(
            staging, job, body=body,
            atomic=not getattr(self.transport, "requires_sandbox", False),
        )
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
    parser.add_argument("--preflight", action="store_true",
                        help="handshake only: prove the Sandbox boundary, publish no job, "
                             "evaluate nothing")
    parser.add_argument("--rendezvous", action="store_true",
                        help="publish token A, confirm its tree is gone, then publish token B")
    parser.add_argument("--rendezvous-body", default=None,
                        help="harmless system fixture (default: tests/fixtures/echo_input.py)")
    parser.add_argument("--write-sandbox-config", metavar="PATH",
                        help="write a .wsb config for the one-item broker")
    parser.add_argument("--mode", choices=("preflight", "serve"), default="preflight",
                        help="config mode for --write-sandbox-config (default: preflight)")
    parser.add_argument("--inbox", help="host path mapped read-only into the Sandbox")
    parser.add_argument("--outbox", help="host path mapped writable into the Sandbox")
    parser.add_argument("--python-root",
                        help="host directory holding the portable interpreter to map read-only")
    parser.add_argument("--wsb-out", help="where --preflight writes its .wsb config")
    parser.add_argument("--launch", action="store_true",
                        help="start WindowsSandbox.exe after the session file is written")
    parser.add_argument("--report", help="where --preflight writes its attestation JSON")
    parser.add_argument("--handshake-timeout", type=float, default=300.0)
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
        if not args.python_root:
            parser.error("--write-sandbox-config requires --python-root: an unmapped "
                         "interpreter cannot start inside the Sandbox")
        xml = backend.sandbox_config_xml(
            Path(args.inbox), Path(args.outbox),
            python_root=Path(args.python_root), mode=args.mode,
        )
        config = backend.verify_sandbox_config(xml, mode=args.mode)
        if not config["ok"]:
            print(json.dumps({"ok": False, "config": config}, indent=2, sort_keys=True))
            return 3
        target = Path(args.write_sandbox_config)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(xml, encoding="utf-8")
        print(f"wrote {target}")
        print(json.dumps({"ok": True, "checks": config["checks"]}, indent=2, sort_keys=True))
        return 0

    if args.preflight:
        return _preflight_cli(parser, args)

    if args.rendezvous:
        return _rendezvous_cli(parser, args)

    if not args.bodies:
        parser.error("nothing to do: pass --verify-boundary, --preflight, "
                     "--rendezvous, --write-sandbox-config or --bodies")

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
        transport = backend.WindowsSandboxTransport(
            handshake_timeout=args.handshake_timeout
        )
        stage_runtime(Path(args.inbox))
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


def _rendezvous_cli(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    """Two-token ordering test. No candidate, no scoring, no oracle."""
    if args.bodies:
        parser.error("--rendezvous runs a system fixture and cannot be combined with --bodies")
    if not (args.inbox and args.outbox):
        parser.error("--rendezvous requires --inbox and --outbox")
    if args.transport == "host-local" and not args.allow_host_local:
        print("refusing to run on the host: host-local execution is not an isolation "
              "boundary. Use --transport sandbox, or pass --allow-host-local for a "
              "harness check only.", file=sys.stderr)
        return 2

    body = Path(args.rendezvous_body) if args.rendezvous_body else (
        HERE / "tests" / "fixtures" / "echo_input.py"
    )
    if not body.is_file():
        parser.error(f"rendezvous fixture not found: {body}")

    work_root = Path(args.work_root)
    report_path = Path(args.report) if args.report else work_root / "rendezvous-log.json"
    inbox, outbox = Path(args.inbox), Path(args.outbox)

    if args.transport == "sandbox":
        stage_runtime(inbox)
        transport = backend.WindowsSandboxTransport(handshake_timeout=args.handshake_timeout)
        try:
            transport.start(inbox, outbox)
        except backend.FatalBoundaryError as exc:
            result = {"ordering_ok": False, "error": type(exc).__name__,
                      "detail": str(exc), "transport": transport.name, "attested": False}
            return _write_report(report_path, result)
        ctl = Controller(work_root, transport=transport,
                         case_paths=(inbox, outbox, work_root / "sandbox-scratch"))
    else:
        transport = backend.HostLocalTransport(work_root / "sandbox-runtime")
        ctl = Controller(work_root, transport=transport)

    try:
        result = run_rendezvous(ctl, body)
    except backend.FatalBoundaryError as exc:
        result = {"ordering_ok": False, "error": type(exc).__name__,
                  "detail": str(exc), "transport": transport.name,
                  "attested": transport.isolation_verified}
        return _write_report(report_path, result)

    result["preflight_attestation"] = transport.attestation()
    return _write_report(report_path, result)


def _write_report(path: Path, payload: dict[str, Any]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"report: {path}", file=sys.stderr)
    return 0 if payload.get("ordering_ok") else 2


def _preflight_cli(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    """Prove the boundary, record it, exit. No job, no candidate, no scoring."""
    if args.bodies:
        parser.error("--preflight is handshake-only and cannot be combined with --bodies")
    if not (args.inbox and args.outbox):
        parser.error("--preflight requires --inbox and --outbox")
    if not args.python_root:
        parser.error("--preflight requires --python-root: an unmapped interpreter "
                     "cannot start inside the Sandbox")

    work_root = Path(args.work_root)
    report_path = Path(args.report) if args.report else work_root / "preflight-attestation.json"
    report: dict[str, Any] = {
        "stage": "sandbox-preflight",
        "host_identity": backend.current_identity(),
        "evaluation_attempted": False,
        "candidate_files": [],
    }

    def finish(status: int) -> int:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return status

    python_root = Path(args.python_root)
    interpreter = backend.interpreter_preflight(python_root)
    report["interpreter"] = interpreter
    if not interpreter["ok"]:
        report.update(ok=False, error="interpreter_preflight_failed")
        return finish(3)

    inbox, outbox = Path(args.inbox), Path(args.outbox)
    inbox.mkdir(parents=True, exist_ok=True)
    outbox.mkdir(parents=True, exist_ok=True)
    report["staged_runtime"] = stage_runtime(inbox)

    xml = backend.sandbox_config_xml(inbox, outbox, python_root=python_root, mode="preflight")
    config = backend.verify_sandbox_config(xml, mode="preflight")
    report["config"] = config
    if not config["ok"]:
        report.update(ok=False, error="sandbox_config_invalid")
        return finish(3)

    wsb = Path(args.wsb_out) if args.wsb_out else work_root / "v9-preflight.wsb"
    wsb.parent.mkdir(parents=True, exist_ok=True)
    wsb.write_text(xml, encoding="utf-8")
    report["wsb"] = str(wsb)

    transport = backend.WindowsSandboxTransport(handshake_timeout=args.handshake_timeout)
    launcher = (lambda: backend.launch_sandbox(wsb)) if args.launch else None
    try:
        report["preflight"] = transport.preflight(inbox, outbox, launch=launcher)
    except backend.FatalBoundaryError as exc:
        report.update(ok=False, error=type(exc).__name__, detail=str(exc))
        return finish(2)

    report["ok"] = bool(report["preflight"]["attestation"]["verified"])
    return finish(0 if report["ok"] else 2)


def main() -> None:
    raise SystemExit(_cli())


if __name__ == "__main__":
    main()
