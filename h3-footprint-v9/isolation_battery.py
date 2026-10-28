"""Bounded, fixed-fixture Windows Sandbox isolation battery.

This harness is deliberately separate from candidate evaluation:

* it never imports ``controller`` or ``oracle``;
* it never runs a candidate body, calls a model, or creates generated code;
* it publishes only the fixed system fixtures under ``tests/fixtures`` through
  the opt-in immutable request protocol, one at a time, well below the 256-request
  scan limit;
* it stops the guest and validates the complete archived event set before it
  writes a report.

The probes receive the guest's real mapped inbox and outbox paths from the agent,
not paths guessed relative to the child's scratch directory. The battery reads
the same guest paths back from the emitted ``.wsb`` configuration and requires
the probe reports to match them.
"""

from __future__ import annotations

import argparse
import json
import ntpath
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import backend  # noqa: E402
import constants  # noqa: E402
import protocol  # noqa: E402
import runtime_stage  # noqa: E402

FIXTURES = HERE / "tests" / "fixtures"
PROBE_MARKER = "V9PROBE"

# id, fixture file, supervisor timeout in seconds
PROBES = (
    ("host_file_access", "isolation_host_file.py", 15.0),
    ("network", "isolation_network.py", 20.0),
    ("inbox_write", "isolation_inbox_write.py", 15.0),
    ("process_tree", "isolation_tree.py", 20.0),
    ("control_exit", "isolation_control_exit.py", 15.0),
)

GUEST_USER = "wdagutilityaccount"

# Explicit guest-side caps, written into the emitted config. The host waits
# timeout + RESPONSE_SLACK; the guest supervisor must give up first so a hung
# probe returns a recorded timeout instead of the host seeing nothing.
GUEST_TIMEOUT_SECONDS = 30.0
GUEST_MAX_PROCESSES = 8
RESPONSE_SLACK_SECONDS = 45.0


def _norm(path: str) -> str:
    return ntpath.normcase(ntpath.normpath(path or ""))


def _under(path: str, folder: str) -> bool:
    path, folder = _norm(path), _norm(folder)
    return path == folder or path.startswith(folder.rstrip("\\") + "\\")


def parse_probe(raw_stdout: str) -> dict | None:
    """Take the last probe line. Value is untrusted guest data."""
    found = None
    for line in (raw_stdout or "").splitlines():
        if line.startswith(PROBE_MARKER + " "):
            found = line[len(PROBE_MARKER) + 1:]
    if found is None:
        return None
    try:
        value = json.loads(found)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def guest_paths(mappings: list[dict], inbox: Path, outbox: Path) -> dict[str, str]:
    """Read the guest paths the emitted config actually maps, not assumptions."""
    wanted = {_norm(str(inbox)): "inbox", _norm(str(outbox)): "outbox"}
    paths: dict[str, str] = {}
    for mapping in mappings:
        key = wanted.get(_norm(mapping.get("host", "")))
        if key is not None:
            paths[key] = mapping.get("sandbox", "")
    if set(paths) != {"inbox", "outbox"}:
        raise ValueError("config does not map both the inbox and the outbox")
    return paths


def _paths_match(report: dict, guest: dict[str, str]) -> bool:
    got = report.get("paths") or {}
    if _norm(got.get("inbox", "")) != _norm(guest["inbox"]):
        return False
    if _norm(got.get("outbox", "")) != _norm(guest["outbox"]):
        return False
    scratch = got.get("scratch", "")
    if not ntpath.isabs(scratch):
        return False
    if _norm(scratch) in (_norm(guest["inbox"]), _norm(guest["outbox"])):
        return False
    return not (_under(scratch, guest["inbox"]) or _under(scratch, guest["outbox"]))


def validate_probe(probe_id: str, record: dict, report: dict | None,
                   guest: dict[str, str]) -> dict:
    """Return the probe's checks and every reason it cannot support a claim."""
    errors: list[str] = []
    checks: dict[str, bool] = {}

    def want(name: str, value: bool) -> None:
        checks[name] = bool(value)
        if not value:
            errors.append(name)

    if not isinstance(report, dict):
        errors.append("probe report is missing or not an object")
        report = {}

    want("status_ok", record.get("status") == "ok")
    want("tree_empty", record.get("tree_empty") is True)
    want("inside_sandbox", record.get("inside_sandbox") is True)
    want("sandbox_account",
         str(record.get("identity_user", "")).split("\\")[-1].lower() == GUEST_USER)
    want("not_timed_out", record.get("timed_out") is False)
    want("stdout_not_overflowed", record.get("stdout_overflow") is False)
    want("probe_matches_request", report.get("probe") == probe_id)
    want("mapped_paths", _paths_match(report, guest))

    if probe_id == "host_file_access":
        want("host_oracle_denied", report.get("oracle_allowed") is False)
        want("host_oracle_error_recorded",
             isinstance(report.get("oracle_error"), str) and bool(report.get("oracle_error")))
        want("host_repo_absent", report.get("host_repo_present") is False)
        want("mapped_body_readable", report.get("positive_allowed") is True)
    elif probe_id == "network":
        want("loopback_connected", report.get("loopback_connected") is True)
        want("external_connect_denied", report.get("external_connected") is False)
        want("external_error_recorded",
             isinstance(report.get("external_error"), str) and bool(report.get("external_error")))
        want("external_target_recorded", report.get("external_target") == "1.1.1.1:443")
    elif probe_id == "inbox_write":
        want("inbox_write_denied", report.get("inbox_write_allowed") is False)
        want("outbox_write_denied", report.get("outbox_write_allowed") is False)
        want("scratch_write_allowed", report.get("scratch_write_allowed") is True)
        want("inbox_error_recorded",
             isinstance(report.get("inbox_write_error"), str)
             and bool(report.get("inbox_write_error")))
        want("outbox_error_recorded",
             isinstance(report.get("outbox_write_error"), str)
             and bool(report.get("outbox_write_error")))
    elif probe_id == "process_tree":
        want("child_spawned", report.get("child_spawned") is True)
        want("child_alive_at_return", report.get("child_alive_at_return") is True)
    elif probe_id == "control_exit":
        want("exited_normally", report.get("exited_normally") is True)

    return {"checks": checks, "errors": errors}


def positive_controls(results: list[dict]) -> dict[str, bool]:
    by_id = {item["id"]: item for item in results}
    report = {item["id"]: (item.get("probe") or {}) for item in results}

    def get(probe_id: str, key: str) -> bool:
        return bool((report.get(probe_id) or {}).get(key))

    return {
        "host_file_mapped_body_readable": get("host_file_access", "positive_allowed"),
        "network_loopback_connected": get("network", "loopback_connected"),
        "scratch_write_allowed": get("inbox_write", "scratch_write_allowed"),
        "control_exit_tree_empty": (
            by_id.get("control_exit", {}).get("accepted") is True
            and by_id.get("control_exit", {}).get("checks", {}).get("tree_empty") is True
        ),
    }


def check_response_channel(outbox: Path, tmp_root: Path) -> dict:
    """Host-side integrity check over disposable copies, never the live guest path."""
    root = Path(tempfile.mkdtemp(prefix="v9-response-channel-", dir=str(tmp_root)))
    job_id = uuid.uuid4().hex
    normal = root / f"response-{job_id}.json"
    record = {
        "v9": protocol.JOB_SCHEMA,
        "job_id": job_id,
        "sequence": 1,
        "kind": "system",
        "body_sha256": "0" * 64,
        "status": "ok",
        "tree_empty": True,
        "answer": 1,
    }
    normal.write_text(json.dumps(record, sort_keys=True), encoding="utf-8")
    normal_accepted = backend.read_trusted_response(normal, job_id)["job_id"] == job_id

    link_id = uuid.uuid4().hex
    target = root / "target"
    target.mkdir()
    link = root / f"response-{link_id}.json"
    made = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace",
    )
    reparse_created = bool(link.exists()) and backend._is_reparse_point(link)
    reparse_rejected = False
    reparse_error = None
    if reparse_created:
        try:
            backend.read_trusted_response(link, link_id)
        except backend.FatalBoundaryError as exc:
            reparse_rejected = True
            reparse_error = str(exc)[:200]
    try:
        if link.exists():
            os.rmdir(link)
    except OSError:
        pass

    foreign = [
        path.name for path in Path(outbox).iterdir()
        if backend._is_reparse_point(path)
    ]
    shutil.rmtree(root, ignore_errors=True)
    return {
        "normal_accepted": normal_accepted,
        "reparse_created": reparse_created,
        "reparse_rejected": reparse_rejected,
        "reparse_error": reparse_error,
        "junction_tool_rc": made.returncode,
        "outbox_reparse_points": foreign,
        "ok": normal_accepted and reparse_created and reparse_rejected and not foreign,
    }


def stop_guest(timeout: float = 20.0) -> dict[str, int | bool]:
    """Stop the dedicated Sandbox session so the event set is final."""
    codes: dict[str, int | bool] = {}
    for name in ("WindowsSandboxClient.exe", "WindowsSandbox.exe"):
        proc = subprocess.run(
            ["taskkill", "/IM", name, "/F"], capture_output=True, text=True,
            timeout=30, encoding="utf-8", errors="replace",
        )
        codes[name] = proc.returncode
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        running = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq WindowsSandbox.exe", "/NH"],
            capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace",
        ).stdout.lower()
        if "windowsandbox.exe" not in running:
            break
        time.sleep(0.5)
    codes["stopped"] = "windowsandbox.exe" not in subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq WindowsSandbox.exe", "/NH"],
        capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace",
    ).stdout.lower()
    return codes


def collect_until_stable(outbox: Path, nonce: str, expected_pid: int,
                         attempts: int = 20) -> dict:
    """Collect the archived events until two reads agree."""
    previous = None
    collected = backend.collect_events(outbox, nonce, expected_pid=expected_pid)
    for _ in range(attempts):
        state = (len(collected["events"]), len(collected["anomalies"]),
                 collected.get("max_seq"))
        if state == previous:
            break
        previous = state
        time.sleep(0.5)
        collected = backend.collect_events(outbox, nonce, expected_pid=expected_pid)
    return collected


def build_job(sequence: int, fixture_name: str) -> tuple[dict, bytes]:
    body = (FIXTURES / fixture_name).read_bytes()
    job = {
        "v9": protocol.JOB_SCHEMA,
        "job_id": uuid.uuid4().hex,
        "sequence": sequence,
        "kind": "system",
        "body_sha256": protocol.sha256_bytes(body),
        "probe_index": sequence,
        "input": {"n": 0, "edges": [], "s": 0, "t": 0},
        "limits": {
            "max_stdout_bytes": constants.MAX_CHILD_STDOUT_BYTES,
            "memory_bytes": constants.MEMORY_LIMIT_BYTES,
            "max_processes": 8,
        },
    }
    return job, body


def _require_empty(path: Path, label: str) -> None:
    path = Path(path)
    if path.exists() and any(path.iterdir()):
        raise ValueError(f"{label} must be empty for a fresh battery: {path}")


def launch_sandbox(config: Path) -> int:
    if sys.platform != "win32":
        raise ValueError("Windows Sandbox can only be launched on Windows")
    # Reuse the detached launcher the preflight already uses: the GUI process
    # must outlive this host-side battery, which keeps running the probes.
    return int(backend.launch_sandbox(Path(config))["pid"])


def run_battery(*, inbox: Path, outbox: Path, work_root: Path, python_root: Path,
                config: Path, report: Path, launch: bool = False,
                keep_guest: bool = False,
                handshake_timeout: float = 300.0,
                settle_seconds: float = 2.0) -> dict:
    inbox, outbox, work_root = Path(inbox), Path(outbox), Path(work_root)
    config, report = Path(config), Path(report)

    _require_empty(inbox, "inbox")
    _require_empty(outbox, "outbox")
    _require_empty(work_root, "work root")
    work_root.mkdir(parents=True, exist_ok=True)
    (work_root / "host-scratch").mkdir(parents=True, exist_ok=True)

    runtime_stage.stage_runtime(inbox)
    xml = backend.sandbox_config_xml(
        inbox, outbox, python_root=python_root, mode="serve", job_protocol="immutable",
        agent_timeout=GUEST_TIMEOUT_SECONDS,
        agent_memory_bytes=constants.MEMORY_LIMIT_BYTES,
        agent_max_processes=GUEST_MAX_PROCESSES,
    )
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(xml, encoding="utf-8")
    verified = backend.verify_sandbox_config(xml, mode="serve", job_protocol="immutable")
    if not verified["ok"]:
        raise ValueError(f"refusing an invalid .wsb config: {verified['violations']}")
    guest = guest_paths(verified["mappings"], inbox, outbox)

    transport = backend.WindowsSandboxTransport(
        handshake_timeout=handshake_timeout,
        response_slack=RESPONSE_SLACK_SECONDS,
        job_protocol="immutable",
    )
    transport.prepare(inbox, outbox)
    started = time.time()
    launcher_pid = launch_sandbox(config) if launch else None
    attestation = transport.await_handshake()
    if not transport.isolation_verified:
        raise ValueError("Sandbox handshake did not verify")

    results: list[dict] = []
    stopped_after = None
    for sequence, (probe_id, fixture_name, timeout) in enumerate(PROBES, start=1):
        job, body = build_job(sequence, fixture_name)
        protocol.publish_immutable_job(inbox, job, body)
        try:
            record = transport.execute(
                inbox, outbox, work_root / "host-scratch",
                timeout=timeout, memory_bytes=constants.MEMORY_LIMIT_BYTES,
                max_processes=8,
            )
        except backend.FatalBoundaryError as exc:
            results.append({
                "id": probe_id, "sequence": sequence, "job_id": job["job_id"],
                "accepted": False, "checks": {}, "errors": [f"{type(exc).__name__}: {exc}"],
                "probe": None, "record": None,
            })
            stopped_after = probe_id
            break

        probe_report = parse_probe(record.get("raw_stdout", ""))
        verdict = validate_probe(probe_id, record, probe_report, guest)
        item = {
            "id": probe_id, "sequence": sequence, "job_id": job["job_id"],
            "accepted": not verdict["errors"],
            "checks": verdict["checks"], "errors": verdict["errors"],
            "probe": probe_report, "record": record,
        }
        results.append(item)

        # A permitted host-file read is a boundary failure: stop before touching
        # any further fixture.
        if probe_id == "host_file_access" and (probe_report or {}).get("oracle_allowed"):
            stopped_after = "host_file_access_permitted"
            break
        if not item["accepted"]:
            stopped_after = probe_id
            break

    channel = check_response_channel(outbox, work_root)
    stop = {"stopped": True, "skipped": True}
    if not keep_guest:
        stop = stop_guest()
        time.sleep(settle_seconds)

    nonce = transport.nonce
    agent_pid = int(attestation["agent"]["pid"])
    collected = collect_until_stable(outbox, nonce, agent_pid)

    controls = positive_controls(results)
    all_probes = len(results) == len(PROBES)
    isolation_ok = (
        all_probes
        and all(item["accepted"] for item in results)
        and all(controls.values())
        and channel["ok"]
        and not collected["anomalies"]
        and len(collected.get("agent_pids", [])) == 1
        and transport.isolation_verified
        and stopped_after is None
    )

    payload = {
        "v9": 1,
        "suite": "isolation-battery-v1",
        "transport": transport.name,
        "protocol": "immutable-v1",
        "started": started,
        "finished": time.time(),
        "attestation": attestation,
        "config": {
            "path": str(config),
            "sha256": protocol.sha256_file(config),
            "guest": guest,
            "verified": verified,
        },
        "launcher_pid": launcher_pid,
        "probes": results,
        "positive_controls": controls,
        "response_channel": channel,
        "stopped_after": stopped_after,
        "guest_stopped": stop,
        "event_count": len(collected["events"]),
        "agent_pids": collected.get("agent_pids", []),
        "max_seq": collected.get("max_seq"),
        "guest_events": collected["events"],
        "telemetry_anomalies": collected["anomalies"],
        "isolation_ok": bool(isolation_ok),
        "note": (
            "fixed fixtures only; no candidate, no model call, no scoring. A pass "
            "covers this host, this Sandbox configuration and these probes only."
        ),
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inbox", required=True)
    parser.add_argument("--outbox", required=True)
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--python-root", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--launch", action="store_true",
                        help="start WindowsSandbox.exe with the generated config")
    parser.add_argument("--keep-guest", action="store_true",
                        help="debug only: leave the guest running and skip the final stop")
    parser.add_argument("--handshake-timeout", type=float, default=300.0)
    args = parser.parse_args(argv)

    try:
        payload = run_battery(
            inbox=Path(args.inbox), outbox=Path(args.outbox),
            work_root=Path(args.work_root), python_root=Path(args.python_root),
            config=Path(args.config), report=Path(args.report),
            launch=args.launch, keep_guest=args.keep_guest,
            handshake_timeout=args.handshake_timeout,
        )
    except (ValueError, backend.FatalBoundaryError) as exc:
        print(json.dumps({"isolation_ok": False, "error": type(exc).__name__,
                          "detail": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps({key: payload[key] for key in
                      ("isolation_ok", "stopped_after", "event_count",
                       "telemetry_anomalies")}, sort_keys=True))
    return 0 if payload["isolation_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
