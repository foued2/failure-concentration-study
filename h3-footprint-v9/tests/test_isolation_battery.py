"""Tests for the fixed-fixture isolation battery.

The battery is a system-boundary harness, not an evaluation entry point. These
tests prove that:

* probe paths are read from the emitted ``.wsb`` configuration, and a report
  that targets look-alike siblings of the guest scratch directory is rejected;
* every required probe and positive control must be present and unambiguous;
* the host-file probe reports only permitted/denied and never returns the bytes
  of the file it tried to open;
* the battery stops immediately if host-file access is unexpectedly permitted;
* the guest is stopped before the event set is collected;
* the harness and its fixtures do not import the evaluation controller or the
  reference oracle.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
V9 = HERE.parent
sys.path.insert(0, str(V9))
sys.path.insert(0, str(HERE))

import backend  # noqa: E402
import isolation_battery  # noqa: E402
import protocol  # noqa: E402
import supervisor  # noqa: E402
import winjob  # noqa: E402

PROBE_IDS = [probe_id for probe_id, _, _ in isolation_battery.PROBES]
PROBE_BY_FIXTURE = {name: probe_id for probe_id, name, _ in isolation_battery.PROBES}
EXPECTED_GUEST = {
    "inbox": backend.SANDBOX_DESKTOP + "\\h3-in",
    "outbox": backend.SANDBOX_DESKTOP + "\\h3-out",
    "scratch": r"C:\Users\WDAGUtilityAccount\AppData\Local\Temp\h3-scratch",
}


def record(**overrides):
    value = {
        "v9": protocol.JOB_SCHEMA,
        "job_id": "a" * 32,
        "sequence": 1,
        "kind": "system",
        "body_sha256": "b" * 64,
        "status": "ok",
        "tree_empty": True,
        "inside_sandbox": True,
        "identity_user": "WDAGUtilityAccount",
        "timed_out": False,
        "stdout_overflow": False,
        "answer": 1,
        "raw_stdout": "",
    }
    value.update(overrides)
    return value


def report_for(probe_id: str, **overrides):
    value = {"probe": probe_id, "paths": dict(EXPECTED_GUEST)}
    if probe_id == "host_file_access":
        value.update(
            oracle_allowed=False,
            oracle_error="PermissionError",
            host_repo_present=False,
            positive_path=EXPECTED_GUEST["inbox"] + "\\isolation_host_file.py",
            positive_allowed=True,
            positive_error=None,
        )
    elif probe_id == "network":
        value.update(
            loopback_port=50000,
            loopback_connected=True,
            loopback_error=None,
            loopback_detail="",
            external_target="1.1.1.1:443",
            external_connected=False,
            external_error="OSError",
            external_detail="blocked",
        )
    elif probe_id == "inbox_write":
        value.update(
            inbox_write_allowed=False,
            inbox_write_error="PermissionError",
            outbox_write_allowed=False,
            outbox_write_error="PermissionError",
            scratch_write_allowed=True,
            scratch_write_error=None,
        )
    elif probe_id == "process_tree":
        value.update(
            parent_pid=100, child_pid=101, child_spawned=True,
            child_alive_at_return=True,
        )
    elif probe_id == "control_exit":
        value.update(exited_normally=True)
    else:  # pragma: no cover - a new probe id needs an explicit report shape
        raise AssertionError(f"no report shape for {probe_id}")
    value.update(overrides)
    return value


def accepted(probe_id: str, probe_report, **record_overrides):
    verdict = isolation_battery.validate_probe(
        probe_id, record(**record_overrides), probe_report, EXPECTED_GUEST
    )
    return verdict["errors"]


def load_fixture(name: str):
    path = isolation_battery.FIXTURES / name
    spec = importlib.util.spec_from_file_location("fixture_" + path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def marker_report(text: str) -> dict:
    line = next(line for line in text.splitlines()
                if line.startswith(isolation_battery.PROBE_MARKER + " "))
    return json.loads(line.split(" ", 1)[1])


class GuestPathTests(unittest.TestCase):
    """The probe must target the mapped folders, not siblings of scratch."""

    def _guest(self, root: Path) -> dict:
        xml = backend.sandbox_config_xml(
            root / "host-in", root / "host-out", python_root=root / "py-embed",
            mode="serve", job_protocol="immutable",
        )
        verified = backend.verify_sandbox_config(
            xml, mode="serve", job_protocol="immutable"
        )
        self.assertTrue(verified["ok"], verified["violations"])
        return isolation_battery.guest_paths(
            verified["mappings"], root / "host-in", root / "host-out"
        )

    def test_guest_paths_come_from_the_emitted_config(self):
        with tempfile.TemporaryDirectory() as td:
            guest = self._guest(Path(td))
        self.assertEqual(guest["inbox"], EXPECTED_GUEST["inbox"])
        self.assertEqual(guest["outbox"], EXPECTED_GUEST["outbox"])
        self.assertTrue(guest["inbox"].endswith("h3-in"))
        self.assertTrue(guest["outbox"].endswith("h3-out"))

    def test_inbox_mapping_is_read_only_and_outbox_is_the_writable_one(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            xml = backend.sandbox_config_xml(
                root / "host-in", root / "host-out", python_root=root / "py",
                mode="serve", job_protocol="immutable",
            )
            folders = backend.verify_sandbox_config(xml)["mappings"]
        by_guest = {folder["sandbox"]: folder["readonly"] for folder in folders}
        self.assertTrue(by_guest[EXPECTED_GUEST["inbox"]])
        self.assertFalse(by_guest[EXPECTED_GUEST["outbox"]])

    def test_a_config_missing_one_mapping_is_refused(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mappings = [{
                "host": str(root / "host-in"),
                "sandbox": EXPECTED_GUEST["inbox"],
                "readonly": True,
            }]
            with self.assertRaises(ValueError):
                isolation_battery.guest_paths(
                    mappings, root / "host-in", root / "host-out"
                )

    def test_a_mapping_of_unrelated_host_folders_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mappings = [
                {"host": str(root / "other-in"),
                 "sandbox": EXPECTED_GUEST["inbox"], "readonly": True},
                {"host": str(root / "other-out"),
                 "sandbox": EXPECTED_GUEST["outbox"], "readonly": False},
            ]
            with self.assertRaises(ValueError):
                isolation_battery.guest_paths(
                    mappings, root / "host-in", root / "host-out"
                )

    def test_paths_beside_scratch_are_not_the_mapped_folders(self):
        # This is exactly the previous defect: ../staging and ../response resolve
        # beside the guest-local scratch directory, not to the Desktop mappings.
        lookalike = {
            "inbox": r"C:\Users\WDAGUtilityAccount\AppData\Local\Temp\staging",
            "outbox": r"C:\Users\WDAGUtilityAccount\AppData\Local\Temp\response",
            "scratch": r"C:\Users\WDAGUtilityAccount\AppData\Local\Temp\h3-scratch",
        }
        errors = accepted("inbox_write", report_for("inbox_write", paths=lookalike))
        self.assertIn("mapped_paths", errors)

    def test_scratch_inside_a_mapped_folder_is_rejected(self):
        paths = dict(EXPECTED_GUEST)
        paths["scratch"] = EXPECTED_GUEST["inbox"] + "\\scratch"
        self.assertIn("mapped_paths", accepted(
            "control_exit", report_for("control_exit", paths=paths)
        ))

    def test_relative_scratch_is_rejected(self):
        paths = dict(EXPECTED_GUEST)
        paths["scratch"] = "h3-scratch"
        self.assertIn("mapped_paths", accepted(
            "control_exit", report_for("control_exit", paths=paths)
        ))

    def test_missing_paths_are_rejected(self):
        errors = accepted("control_exit", report_for("control_exit", paths={}))
        self.assertIn("mapped_paths", errors)


class ProbeValidationTests(unittest.TestCase):
    """Every probe needs its expected observation *and* a safe control."""

    def test_each_probe_accepts_its_expected_report(self):
        for probe_id in PROBE_IDS:
            with self.subTest(probe=probe_id):
                self.assertEqual(accepted(probe_id, report_for(probe_id)), [])

    def test_a_missing_probe_report_fails(self):
        errors = accepted("network", None)
        self.assertTrue(errors)
        self.assertTrue(any("missing or not an object" in error for error in errors))

    def test_a_probe_naming_the_wrong_request_fails(self):
        self.assertIn("probe_matches_request", accepted(
            "network", report_for("inbox_write")
        ))

    def test_record_level_failures_are_not_ignored(self):
        cases = {
            "status_ok": {"status": "error"},
            "tree_empty": {"tree_empty": False},
            "inside_sandbox": {"inside_sandbox": False},
            "sandbox_account": {"identity_user": "Foued\\Foued"},
            "not_timed_out": {"timed_out": True},
            "stdout_not_overflowed": {"stdout_overflow": True},
        }
        for check, override in cases.items():
            with self.subTest(check=check):
                errors = accepted(
                    "control_exit", report_for("control_exit"), **override
                )
                self.assertIn(check, errors)

    def test_host_file_access_must_be_denied(self):
        errors = accepted(
            "host_file_access", report_for("host_file_access", oracle_allowed=True)
        )
        self.assertIn("host_oracle_denied", errors)

    def test_host_file_probe_needs_its_safe_positive_control(self):
        errors = accepted(
            "host_file_access", report_for("host_file_access", positive_allowed=False)
        )
        self.assertIn("mapped_body_readable", errors)

    def test_host_file_probe_needs_a_recorded_error_class(self):
        errors = accepted(
            "host_file_access", report_for("host_file_access", oracle_error=None)
        )
        self.assertIn("host_oracle_error_recorded", errors)

    def test_host_repo_must_be_absent_from_the_guest(self):
        errors = accepted(
            "host_file_access", report_for("host_file_access", host_repo_present=True)
        )
        self.assertIn("host_repo_absent", errors)

    def test_network_needs_loopback_as_a_positive_control(self):
        errors = accepted(
            "network", report_for("network", loopback_connected=False)
        )
        self.assertIn("loopback_connected", errors)

    def test_external_connection_must_be_denied_and_explained(self):
        errors = accepted(
            "network", report_for("network", external_connected=True)
        )
        self.assertIn("external_connect_denied", errors)
        errors = accepted(
            "network", report_for("network", external_error=None)
        )
        self.assertIn("external_error_recorded", errors)

    def test_external_target_is_recorded_exactly(self):
        errors = accepted(
            "network", report_for("network", external_target="example.com:80")
        )
        self.assertIn("external_target_recorded", errors)

    def test_inbox_and_outbox_writes_must_be_denied(self):
        self.assertIn("inbox_write_denied", accepted(
            "inbox_write", report_for("inbox_write", inbox_write_allowed=True)
        ))
        self.assertIn("outbox_write_denied", accepted(
            "inbox_write", report_for("inbox_write", outbox_write_allowed=True)
        ))

    def test_inbox_write_probe_needs_a_scratch_positive_control(self):
        errors = accepted(
            "inbox_write", report_for("inbox_write", scratch_write_allowed=False)
        )
        self.assertIn("scratch_write_allowed", errors)

    def test_inbox_write_errors_must_be_recorded(self):
        errors = accepted(
            "inbox_write", report_for("inbox_write", inbox_write_error=None)
        )
        self.assertIn("inbox_error_recorded", errors)

    def test_process_tree_probe_requires_a_live_child_at_return(self):
        errors = accepted(
            "process_tree", report_for("process_tree", child_alive_at_return=False)
        )
        self.assertIn("child_alive_at_return", errors)

    def test_normal_exit_control_is_required(self):
        errors = accepted(
            "control_exit", report_for("control_exit", exited_normally=False)
        )
        self.assertIn("exited_normally", errors)


class PositiveControlTests(unittest.TestCase):
    def _results(self, **overrides) -> list[dict]:
        results = []
        for probe_id in PROBE_IDS:
            report = report_for(probe_id)
            if probe_id in overrides:
                report.update(overrides[probe_id])
            results.append({
                "id": probe_id,
                "accepted": True,
                "checks": {"tree_empty": True},
                "probe": report,
            })
        return results

    def test_all_controls_pass_together(self):
        controls = isolation_battery.positive_controls(self._results())
        self.assertTrue(all(controls.values()), controls)

    def test_a_missing_control_makes_the_report_fail(self):
        results = [item for item in self._results()
                   if item["id"] != "control_exit"]
        self.assertFalse(isolation_battery.positive_controls(results)[
            "control_exit_tree_empty"
        ])

    def test_a_control_exit_without_an_empty_tree_fails(self):
        results = self._results()
        for item in results:
            if item["id"] == "control_exit":
                item["checks"]["tree_empty"] = False
        self.assertFalse(isolation_battery.positive_controls(results)[
            "control_exit_tree_empty"
        ])

    def test_a_denied_host_positive_control_fails(self):
        controls = isolation_battery.positive_controls(
            self._results(host_file_access={"positive_allowed": False})
        )
        self.assertFalse(controls["host_file_mapped_body_readable"])


@unittest.skipUnless(winjob.IS_WINDOWS, "response-channel integrity uses Windows junctions")
class ResponseChannelTests(unittest.TestCase):
    def test_a_normal_response_is_accepted_and_a_junction_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            outbox = root / "out"
            outbox.mkdir()
            result = isolation_battery.check_response_channel(outbox, root)
            self.assertTrue(result["normal_accepted"], result)
            self.assertTrue(result["reparse_created"], result)
            self.assertTrue(result["reparse_rejected"], result)
            self.assertTrue(result["ok"], result)
            self.assertEqual(result["outbox_reparse_points"], [])
            self.assertEqual(list(root.glob("v9-response-channel-*")), [])

    def test_a_reparse_point_in_the_outbox_fails_the_channel(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            outbox = root / "out"
            target = outbox / "target"
            target.mkdir(parents=True)
            link = outbox / ("response-" + "d" * 32 + ".json")
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(target)],
                capture_output=True, text=True, timeout=30,
                encoding="utf-8", errors="replace",
            )
            if not backend._is_reparse_point(link):
                self.skipTest("this host cannot create an unprivileged junction")
            self.addCleanup(_remove_junction, link)
            result = isolation_battery.check_response_channel(outbox, root)
            self.assertFalse(result["ok"], result)
            self.assertIn(link.name, result["outbox_reparse_points"])


def _remove_junction(path: Path) -> None:
    import os
    try:
        os.rmdir(path)
    except OSError:
        pass


class FakeSandboxTransport:
    """A scripted guest that still speaks the immutable request protocol."""

    name = "fake-sandbox"
    requires_sandbox = True
    instances: list["FakeSandboxTransport"] = []
    reports: dict = {}
    raise_on: set[str] = set()
    fixture_hashes: dict[str, str] = {}

    def __init__(self, *, handshake_timeout: float = 180.0,
                 response_slack: float = 120.0, job_protocol: str = "legacy") -> None:
        self.handshake_timeout = handshake_timeout
        self.response_slack = response_slack
        self.job_protocol = job_protocol
        self._attestation = None
        self._nonce = None
        self.executed: list[str] = []
        FakeSandboxTransport.instances.append(self)

    @property
    def isolation_verified(self) -> bool:
        return bool(self._attestation and self._attestation.get("verified"))

    @property
    def nonce(self) -> str | None:
        return self._nonce

    def prepare(self, inbox: Path, outbox: Path) -> None:
        self._nonce = "e" * 32
        protocol._atomic_write(
            Path(inbox) / backend.HANDLE_SESSION,
            json.dumps({"v9": protocol.JOB_SCHEMA, "nonce": self._nonce},
                       sort_keys=True).encode("utf-8"),
        )
        hello = Path(outbox) / backend.HANDLE_HELLO
        if hello.exists():
            hello.unlink()

    def await_handshake(self) -> dict:
        self._attestation = {
            "verified": True,
            "transport": self.name,
            "checks": {"nonce": True, "inside_sandbox": True, "account": True},
            "agent": {"pid": 4242, "user": "WDAGUtilityAccount"},
        }
        return self._attestation

    def execute(self, staging: Path, response_dir: Path, scratch: Path, *,
                timeout: float, memory_bytes: int, max_processes: int) -> dict:
        scan = protocol.scan_immutable_jobs(staging)
        self.assertCleanScan(scan)
        job = scan["requests"][-1]
        fixture = next(
            name for name, digest in self.fixture_hashes.items()
            if digest == job["body_sha256"]
        )
        probe_id = PROBE_BY_FIXTURE[fixture]
        self.executed.append(probe_id)
        if probe_id in self.raise_on:
            raise backend.FatalBoundaryError(f"scripted failure for {probe_id}")
        report = self.reports.get(probe_id)
        raw = "" if report is None else (
            isolation_battery.PROBE_MARKER + " " + json.dumps(report, sort_keys=True)
        )
        response = {
            "v9": protocol.JOB_SCHEMA,
            "job_id": job["job_id"],
            "sequence": job["sequence"],
            "kind": job["kind"],
            "body_sha256": job["body_sha256"],
            "probe_index": job.get("probe_index"),
            "status": "ok",
            "tree_empty": True,
            "answer": 1,
            "raw_stdout": raw,
            "inside_sandbox": True,
            "identity_user": "WDAGUtilityAccount",
            "timed_out": False,
            "stdout_overflow": False,
        }
        path = protocol.write_response_exclusive(Path(response_dir), response)
        return backend.read_trusted_response(path, job["job_id"])

    @staticmethod
    def assertCleanScan(scan: dict) -> None:
        if not scan["scanned"] or scan["errors"] or scan["truncated"]:
            raise AssertionError(f"unexpected scan state: {scan}")


class BatteryRunTests(unittest.TestCase):
    """End-to-end over a scripted guest, with the real staging/config path."""

    def setUp(self) -> None:
        FakeSandboxTransport.instances = []
        FakeSandboxTransport.reports = {
            probe_id: report_for(probe_id) for probe_id in PROBE_IDS
        }
        FakeSandboxTransport.raise_on = set()
        FakeSandboxTransport.fixture_hashes = {
            name: protocol.sha256_bytes(
                (isolation_battery.FIXTURES / name).read_bytes()
            )
            for _, name, _ in isolation_battery.PROBES
        }

    def _run(self, *, reports=None, raise_on=None, collected=None, channel=None,
             populated_inbox=False, order=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        inbox, outbox, work = root / "in", root / "out", root / "work"
        python_root = root / "py-embed"
        python_root.mkdir()
        config, report_path = root / "battery.wsb", root / "battery.json"
        if populated_inbox:
            inbox.mkdir(parents=True)
            (inbox / "stale.txt").write_text("stale\n", encoding="utf-8")

        if reports is not None:
            FakeSandboxTransport.reports = reports
        if raise_on:
            FakeSandboxTransport.raise_on = set(raise_on)
        if collected is None:
            collected = {
                "events": [{"seq": index} for index in range(1, 6)],
                "anomalies": [],
                "foreign_events": 0,
                "max_seq": 5,
                "started_at": 1.0,
                "agent_pids": [4242],
            }
        if channel is None:
            channel = {
                "normal_accepted": True, "reparse_created": True,
                "reparse_rejected": True, "reparse_error": "reparse point",
                "junction_tool_rc": 0, "outbox_reparse_points": [], "ok": True,
            }

        events: list[str] = order if order is not None else []
        launched: list[Path] = []

        def fake_launch(path) -> int:
            events.append("launch")
            self.assertTrue(Path(path).is_file())
            launched.append(Path(path))
            return 777

        def fake_stop() -> dict:
            events.append("stop")
            return {"stopped": True, "WindowsSandbox.exe": 0}

        def fake_collect(*args, **kwargs) -> dict:
            events.append("collect")
            return collected

        with mock.patch.object(
            isolation_battery.backend, "WindowsSandboxTransport", FakeSandboxTransport
        ), mock.patch.object(
            isolation_battery, "launch_sandbox", side_effect=fake_launch
        ), mock.patch.object(
            isolation_battery, "stop_guest", side_effect=fake_stop
        ), mock.patch.object(
            isolation_battery, "check_response_channel", return_value=channel
        ), mock.patch.object(
            isolation_battery, "collect_until_stable", side_effect=fake_collect
        ):
            payload = isolation_battery.run_battery(
                inbox=inbox, outbox=outbox, work_root=work,
                python_root=python_root, config=config, report=report_path,
                launch=True, settle_seconds=0.0,
            )
        return payload, FakeSandboxTransport.instances[-1], report_path, config

    def test_a_complete_battery_passes_only_with_every_probe_and_control(self):
        order: list[str] = []
        payload, fake, report_path, config = self._run(order=order)

        self.assertTrue(payload["isolation_ok"], json.dumps(payload, indent=2)[:4000])
        self.assertEqual(payload["protocol"], "immutable-v1")
        self.assertEqual(fake.job_protocol, "immutable")
        self.assertEqual(fake.response_slack, isolation_battery.RESPONSE_SLACK_SECONDS)
        self.assertEqual(fake.executed, PROBE_IDS)
        self.assertEqual([item["id"] for item in payload["probes"]], PROBE_IDS)
        self.assertTrue(all(item["accepted"] for item in payload["probes"]))
        self.assertTrue(all(payload["positive_controls"].values()))
        self.assertIsNone(payload["stopped_after"])
        self.assertEqual(
            {key: payload["config"]["guest"][key] for key in ("inbox", "outbox")},
            {key: EXPECTED_GUEST[key] for key in ("inbox", "outbox")},
        )
        self.assertEqual(payload["event_count"], 5)
        self.assertEqual(payload["agent_pids"], [4242])
        self.assertEqual(payload["telemetry_anomalies"], [])
        self.assertTrue(report_path.is_file())
        saved = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertTrue(saved["isolation_ok"])

        # The guest is stopped before its event set is read.
        self.assertLess(order.index("stop"), order.index("collect"))
        self.assertLess(order.index("launch"), order.index("stop"))

        # Explicit caps are written into the config the guest is launched with.
        xml = config.read_text(encoding="utf-8")
        self.assertIn("--job-protocol immutable", xml)
        self.assertIn(f"--timeout {isolation_battery.GUEST_TIMEOUT_SECONDS:g}", xml)
        self.assertIn("--max-processes 8", xml)
        self.assertIn("--memory-bytes 536870912", xml)

    def test_the_run_publishes_only_immutable_requests_and_stays_bounded(self):
        payload, fake, _, _ = self._run()
        inbox = Path(payload["config"]["path"]).parent / "in"
        jobs = sorted(inbox.glob("job-*.json"))
        bodies = sorted((inbox / "bodies").glob("*.py"))
        self.assertEqual(len(jobs), len(PROBE_IDS))
        self.assertEqual(len(bodies), len(PROBE_IDS))
        self.assertFalse((inbox / "job.json").exists())
        self.assertLess(len(PROBE_IDS), protocol.IMMUTABLE_SCAN_LIMIT)

    def test_a_permitted_host_file_stops_the_battery_immediately(self):
        reports = dict(FakeSandboxTransport.reports)
        reports["host_file_access"] = report_for(
            "host_file_access", oracle_allowed=True
        )
        payload, fake, _, _ = self._run(reports=reports)

        self.assertFalse(payload["isolation_ok"])
        self.assertEqual(fake.executed, ["host_file_access"])
        self.assertEqual(payload["stopped_after"], "host_file_access_permitted")
        self.assertEqual(len(payload["probes"]), 1)
        self.assertIn("host_oracle_denied", payload["probes"][0]["errors"])

    def test_a_failed_probe_stops_before_the_remaining_probes(self):
        reports = dict(FakeSandboxTransport.reports)
        reports["network"] = report_for("network", external_connected=True)
        payload, fake, _, _ = self._run(reports=reports)

        self.assertFalse(payload["isolation_ok"])
        self.assertEqual(fake.executed, ["host_file_access", "network"])
        self.assertEqual(payload["stopped_after"], "network")
        self.assertEqual(len(payload["probes"]), 2)

    def test_a_missing_probe_report_is_a_failure_not_a_pass(self):
        reports = dict(FakeSandboxTransport.reports)
        reports["inbox_write"] = None
        payload, fake, _, _ = self._run(reports=reports)

        self.assertFalse(payload["isolation_ok"])
        self.assertEqual(payload["stopped_after"], "inbox_write")
        item = payload["probes"][-1]
        self.assertFalse(item["accepted"])
        self.assertTrue(any("missing or not an object" in error
                            for error in item["errors"]))

    def test_path_lookalikes_fail_the_first_probe(self):
        reports = dict(FakeSandboxTransport.reports)
        reports["host_file_access"] = report_for(
            "host_file_access",
            paths={
                "inbox": EXPECTED_GUEST["scratch"] + r"\..\staging",
                "outbox": EXPECTED_GUEST["scratch"] + r"\..\response",
                "scratch": EXPECTED_GUEST["scratch"],
            },
        )
        payload, fake, _, _ = self._run(reports=reports)

        self.assertFalse(payload["isolation_ok"])
        self.assertEqual(fake.executed, ["host_file_access"])
        self.assertIn("mapped_paths", payload["probes"][0]["errors"])

    def test_a_reparse_point_in_the_response_channel_fails_the_report(self):
        reports = dict(FakeSandboxTransport.reports)
        channel = {
            "normal_accepted": True, "reparse_created": True,
            "reparse_rejected": False, "reparse_error": None,
            "junction_tool_rc": 0, "outbox_reparse_points": [], "ok": False,
        }
        payload, _, _, _ = self._run(reports=reports, channel=channel)
        self.assertFalse(payload["isolation_ok"])
        self.assertFalse(payload["response_channel"]["reparse_rejected"])

    def test_telemetry_anomalies_fail_an_otherwise_passing_run(self):
        payload, _, _, _ = self._run(collected={
            "events": [{"seq": 1}], "anomalies": [{"file": "", "error": "bad"}],
            "foreign_events": 0, "max_seq": 1, "started_at": 1.0,
            "agent_pids": [4242],
        })
        self.assertFalse(payload["isolation_ok"])
        self.assertEqual(payload["telemetry_anomalies"], [{"file": "", "error": "bad"}])

    def test_more_than_one_agent_pid_fails_the_run(self):
        payload, _, _, _ = self._run(collected={
            "events": [{"seq": 1}], "anomalies": [], "foreign_events": 0,
            "max_seq": 1, "started_at": 1.0, "agent_pids": [4242, 4343],
        })
        self.assertFalse(payload["isolation_ok"])

    def test_a_nonempty_inbox_is_refused_before_anything_runs(self):
        with self.assertRaises(ValueError):
            self._run(populated_inbox=True)
        self.assertEqual(FakeSandboxTransport.instances, [])

    def test_a_scripted_boundary_error_is_recorded_and_stops_the_battery(self):
        payload, fake, _, _ = self._run(raise_on={"process_tree"})
        self.assertFalse(payload["isolation_ok"])
        self.assertEqual(fake.executed[-1], "process_tree")
        self.assertEqual(payload["stopped_after"], "process_tree")
        self.assertTrue(any("scripted failure" in error
                            for error in payload["probes"][-1]["errors"]))


class HarnessSeparationTests(unittest.TestCase):
    """The diagnostic harness must stay outside candidate evaluation."""

    def test_probe_ids_cover_every_required_boundary(self):
        self.assertEqual(set(PROBE_IDS), {
            "host_file_access", "network", "inbox_write",
            "process_tree", "control_exit",
        })
        self.assertNotIn("boundary_probe.py",
                         {name for _, name, _ in isolation_battery.PROBES})

    def test_harness_does_not_import_evaluation_or_reference_modules(self):
        source = (V9 / "isolation_battery.py").read_text(encoding="utf-8")
        for forbidden in ("controller", "oracle", "gates"):
            self.assertIsNone(
                re.search(rf"(?m)^\s*(import|from)\s+{forbidden}\b", source),
                f"isolation_battery.py imports {forbidden}",
            )

    def test_fixtures_do_not_import_reference_modules(self):
        for _, name, _ in isolation_battery.PROBES:
            source = (isolation_battery.FIXTURES / name).read_text(encoding="utf-8")
            for forbidden in ("controller", "oracle"):
                self.assertIsNone(
                    re.search(rf"(?m)^\s*(import|from)\s+{forbidden}\b", source),
                    f"{name} imports {forbidden}",
                )
            self.assertIn("solve_job", source, name)

    def test_battery_jobs_carry_no_expectation_and_use_bounded_caps(self):
        job, body = isolation_battery.build_job(1, "isolation_control_exit.py")
        self.assertEqual(job["body_sha256"], protocol.sha256_bytes(body))
        self.assertEqual(job["kind"], "system")
        serialized = json.dumps(job).lower()
        for forbidden in ("expected", "answer", "family", "oracle"):
            self.assertNotIn(forbidden, serialized)
        self.assertEqual(job["limits"]["max_processes"],
                         isolation_battery.GUEST_MAX_PROCESSES)

    def test_the_bounded_battery_is_far_below_the_request_scan_limit(self):
        self.assertLess(len(isolation_battery.PROBES), 256)
        self.assertLessEqual(len(isolation_battery.PROBES), 8)


class FixtureBehaviourTests(unittest.TestCase):
    def test_host_file_probe_never_returns_the_file_contents(self):
        fixture = load_fixture("isolation_host_file.py")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sentinel = "SECRET-ANSWER-MUST-NOT-CROSS"
            oracle = root / "oracle.py"
            oracle.write_text(f"EXPECTED = {sentinel!r}\n", encoding="utf-8")
            out = io.StringIO()
            with mock.patch.object(fixture, "HOST_ORACLE", str(oracle)), \
                    mock.patch.object(fixture, "HOST_REPO", str(root)), \
                    contextlib.redirect_stdout(out):
                self.assertEqual(fixture.solve_job({"paths": EXPECTED_GUEST}), 1)
        text = out.getvalue()
        self.assertNotIn(sentinel, text)
        report = marker_report(text)
        self.assertTrue(report["oracle_allowed"])
        self.assertTrue(report["host_repo_present"])
        self.assertIsNone(report["oracle_error"])

    def test_host_file_probe_reports_a_denial_without_reading(self):
        fixture = load_fixture("isolation_host_file.py")
        with tempfile.TemporaryDirectory() as td:
            missing = str(Path(td) / "absent-oracle.py")
            out = io.StringIO()
            with mock.patch.object(fixture, "HOST_ORACLE", missing), \
                    contextlib.redirect_stdout(out):
                fixture.solve_job({"paths": EXPECTED_GUEST})
        report = marker_report(out.getvalue())
        self.assertFalse(report["oracle_allowed"])
        self.assertEqual(report["oracle_error"], "FileNotFoundError")

    def test_inbox_probe_targets_only_the_paths_it_is_given(self):
        fixture = load_fixture("isolation_inbox_write.py")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox, outbox = root / "in", root / "out"
            scratch = root / "scratch"
            decoy_in, decoy_out = root / "staging", root / "response"
            for path in (inbox, outbox, scratch, decoy_in, decoy_out):
                path.mkdir()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                fixture.solve_job({"paths": {
                    "inbox": str(inbox), "outbox": str(outbox),
                    "scratch": str(scratch),
                }})
            self.assertTrue((inbox / "probe-write.txt").is_file())
            self.assertTrue((outbox / "probe-write.txt").is_file())
            self.assertTrue((scratch / "probe-write.txt").is_file())
            self.assertEqual(list(decoy_in.iterdir()), [])
            self.assertEqual(list(decoy_out.iterdir()), [])
        report = marker_report(out.getvalue())
        self.assertTrue(report["scratch_write_allowed"])
        self.assertEqual(report["paths"]["inbox"], str(inbox))

    def test_inbox_probe_refuses_to_write_without_absolute_paths(self):
        fixture = load_fixture("isolation_inbox_write.py")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(fixture.solve_job({}), 1)
        report = marker_report(out.getvalue())
        self.assertEqual(report["paths_error"], "missing_or_relative_paths")
        self.assertNotIn("scratch_write_allowed", report)


class RuntimePathTests(unittest.TestCase):
    """The agent passes the directories it was launched with, not a guess."""

    def test_runtime_paths_are_absolute_and_distinct(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = supervisor.runtime_paths(root / "in", root / "out", root / "scratch")
        self.assertEqual(set(paths), {"inbox", "outbox", "scratch"})
        for value in paths.values():
            self.assertTrue(Path(value).is_absolute())
        self.assertEqual(len(set(paths.values())), 3)

    def test_runtime_paths_reject_duplicate_directories(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaises(ValueError):
                supervisor.runtime_paths(root / "in", root / "in", root / "scratch")

    def test_child_payload_preserves_the_job_input_and_adds_paths(self):
        job = {"input": {"n": 3, "edges": [[0, 1]], "s": 0, "t": 1}}
        payload = json.loads(supervisor._child_payload(job, EXPECTED_GUEST))
        self.assertEqual(payload["n"], 3)
        self.assertEqual(payload["edges"], [[0, 1]])
        self.assertEqual(payload["paths"], EXPECTED_GUEST)

    def test_child_payload_without_paths_is_unchanged(self):
        job = {"input": {"n": 3, "edges": [], "s": 0, "t": 1}}
        self.assertEqual(
            supervisor._child_payload(job, None),
            json.dumps(job["input"], sort_keys=True),
        )

    def test_child_payload_wraps_a_non_object_input(self):
        payload = json.loads(supervisor._child_payload({"input": 7}, EXPECTED_GUEST))
        self.assertEqual(payload, {"input": 7, "paths": EXPECTED_GUEST})


if __name__ == "__main__":
    unittest.main()
