from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import backend  # noqa: E402
import controller  # noqa: E402
import protocol  # noqa: E402
from _support import fixture  # noqa: E402

V9 = HERE.parent
ON_HOST = not backend.current_identity()["inside_sandbox"]
WDAG = "DESKTOP-ABC\\WDAGUtilityAccount"


def write_hello(outbox: Path, nonce: str, *, user: str = WDAG,
                inside: bool = True, mode: str = "preflight") -> Path:
    outbox.mkdir(parents=True, exist_ok=True)
    path = outbox / "hello.json"
    path.write_text(json.dumps({
        "v9": protocol.JOB_SCHEMA, "nonce": nonce, "mode": mode,
        "user": user, "inside_sandbox": inside, "computer": "DESKTOP-ABC",
        "pid": 4242, "source": "GetUserNameW",
    }), encoding="utf-8")
    return path


def fake_python_root(root: Path) -> Path:
    """A stand-in for an embeddable distribution staged for the mapping."""
    directory = root / "py-embed"
    directory.mkdir(parents=True, exist_ok=True)
    for name in ("python.exe", "python313.zip", "python313.dll"):
        (directory / name).write_bytes(b"MZ")
    return directory


def valid_response(**overrides) -> dict:
    record = {
        "v9": protocol.JOB_SCHEMA,
        "job_id": "a" * 32,
        "sequence": 1,
        "kind": "probe",
        "body_sha256": "b" * 64,
        "status": "ok",
        "tree_empty": True,
        "answer": 0,
        "raw_stdout": "",
    }
    record.update(overrides)
    return record


class IdentityTests(unittest.TestCase):
    def test_identity_comes_from_the_token_not_the_environment(self):
        ident = backend.current_identity()
        self.assertEqual(ident["source"], "GetUserNameW")
        self.assertIn("inside_sandbox", ident)

    @unittest.skipUnless(ON_HOST, "only meaningful outside Windows Sandbox")
    def test_setting_username_cannot_masquerade_as_sandbox(self):
        saved = os.environ.get("USERNAME")
        os.environ["USERNAME"] = "WDAGUtilityAccount"
        try:
            self.assertFalse(backend.current_identity()["inside_sandbox"])
        finally:
            if saved is None:
                os.environ.pop("USERNAME", None)
            else:
                os.environ["USERNAME"] = saved


class TransportTests(unittest.TestCase):
    def test_controller_requires_an_explicit_transport(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(TypeError):
                controller.Controller(Path(td) / "work")  # type: ignore[call-arg]

    def test_authorized_evaluation_refuses_host_transport(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = controller.Controller(
                root / "work", transport=backend.HostLocalTransport(root / "rt")
            )
            with self.assertRaises(backend.BoundaryNotEstablished):
                ctl.evaluate_authorized(fixture("correct.py"))

    def test_sandbox_transport_refuses_to_execute_without_attestation(self):
        transport = backend.WindowsSandboxTransport()
        self.assertFalse(transport.isolation_verified)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaises(backend.BoundaryNotEstablished):
                transport.execute(root, root, root, timeout=0.1,
                                  memory_bytes=1, max_processes=1)

    def test_handshake_times_out_without_an_agent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            transport = backend.WindowsSandboxTransport(handshake_timeout=0.3)
            transport.prepare(root / "in", root / "out")
            with self.assertRaises(backend.BoundaryNotEstablished):
                transport.await_handshake()

    def test_handshake_rejects_a_stale_nonce(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            transport = backend.WindowsSandboxTransport(handshake_timeout=1.0)
            transport.prepare(root / "in", root / "out")
            write_hello(root / "out", "stale")
            with self.assertRaises(backend.BoundaryNotEstablished) as ctx:
                transport.await_handshake()
            self.assertIn("nonce=False", str(ctx.exception))

    def test_handshake_rejects_an_agent_running_on_the_host(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox, outbox = root / "in", root / "out"
            transport = backend.WindowsSandboxTransport(handshake_timeout=20.0)
            transport.prepare(inbox, outbox)
            proc = subprocess.Popen(
                [sys.executable, "-I", str(V9 / "sandbox_agent.py"),
                 "--inbox", str(inbox), "--outbox", str(outbox),
                 "--handshake-only", "--allow-host"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            try:
                with self.assertRaises(backend.BoundaryNotEstablished) as ctx:
                    transport.await_handshake()
                self.assertIn("inside_sandbox=False", str(ctx.exception))
                self.assertFalse(transport.isolation_verified)
            finally:
                proc.kill()
                proc.wait(timeout=10)


class HandshakePredicateTests(unittest.TestCase):
    """Test the predicate, not a fabricated attestation."""

    def test_accepts_only_a_matching_sandbox_account(self):
        good = {"nonce": "n", "inside_sandbox": True, "user": WDAG}
        self.assertTrue(all(backend.validate_handshake(good, "n").values()))

    def test_rejects_each_failure_independently(self):
        base = {"nonce": "n", "inside_sandbox": True, "user": WDAG}
        for key, value, flag in (
            ("nonce", "other", "nonce"),
            ("inside_sandbox", False, "inside_sandbox"),
            ("user", "desktop-abc\\Foued", "account"),
        ):
            checks = backend.validate_handshake({**base, key: value}, "n")
            self.assertFalse(checks[flag], f"{key} was not rejected")
            self.assertEqual(sum(1 for v in checks.values() if not v), 1)


class SandboxConfigMappingTests(unittest.TestCase):
    """The emitted config must be launchable *and* bounded.

    The previous revision pointed the LogonCommand at C:\\h3-py\\python.exe while
    mapping only the inbox and outbox, so the agent could never start.
    """

    def _xml(self, root: Path, **kwargs) -> str:
        return backend.sandbox_config_xml(
            root / "in", root / "out", python_root=kwargs.pop("python_root",
                                                             root / "py-embed"),
            **kwargs,
        )

    def test_interpreter_is_covered_by_a_read_only_mapping(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            xml = self._xml(root)
            config = backend.verify_sandbox_config(xml, mode="preflight")
            self.assertTrue(config["ok"], config["violations"])

            parsed = ET.fromstring(xml)
            folders = {f.findtext("SandboxFolder"): f.findtext("ReadOnly")
                       for f in parsed.findall("MappedFolders/MappedFolder")}
            command = parsed.findtext("LogonCommand/Command") or ""
            exe = command.split('"')[1]
            folder = str(Path(exe).parent).replace("/", "\\")
            self.assertIn(folder, folders, f"interpreter {exe} is not inside a mapped folder")
            self.assertEqual(folders[folder], "true")

    def test_exactly_one_mapping_is_writable_and_it_is_the_outbox(self):
        with tempfile.TemporaryDirectory() as td:
            xml = self._xml(Path(td))
            parsed = ET.fromstring(xml)
            writable = [f.findtext("SandboxFolder")
                        for f in parsed.findall("MappedFolders/MappedFolder")
                        if (f.findtext("ReadOnly") or "").lower() == "false"]
            self.assertEqual(len(writable), 1)
            self.assertTrue(writable[0].endswith("h3-out"), writable)

    def test_hardening_switches_are_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            parsed = ET.fromstring(self._xml(Path(td)))
            self.assertEqual(parsed.findtext("Networking"), "Disable")
            self.assertEqual(parsed.findtext("ClipboardRedirection"), "Disable")
            self.assertEqual(parsed.findtext("vGPU"), "Disable")
            self.assertEqual(parsed.findtext("AudioInput"), "Disable")
            self.assertEqual(parsed.findtext("VideoInput"), "Disable")
            self.assertEqual(parsed.findtext("PrinterRedirection"), "Disable")
            self.assertGreater(int(parsed.findtext("MemoryInMB")), 0)

    def test_interpreter_argument_is_mandatory(self):
        with self.assertRaises(TypeError):
            backend.sandbox_config_xml(Path("in"), Path("out"))  # type: ignore[call-arg]

    def test_unmapped_interpreter_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            xml = self._xml(root)
            # Move the Python mapping away while the command still points at it.
            broken = xml.replace(
                '<SandboxFolder>' + backend.SANDBOX_DESKTOP + '\\h3-py</SandboxFolder>',
                '<SandboxFolder>' + backend.SANDBOX_DESKTOP + '\\h3-elsewhere</SandboxFolder>',
            )
            config = backend.verify_sandbox_config(broken)
            self.assertFalse(config["ok"])
            self.assertIn("interpreter_mapped_read_only", config["violations"])

    def test_guest_paths_must_be_absolute_and_unique(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            xml = backend.sandbox_config_xml(root / "in", root / "out",
                                             python_root=root / "py-embed")
            duplicated = xml.replace(
                '<SandboxFolder>' + backend.SANDBOX_DESKTOP + '\\h3-out</SandboxFolder>',
                '<SandboxFolder>' + backend.SANDBOX_DESKTOP + '\\h3-in</SandboxFolder>',
            )
            config = backend.verify_sandbox_config(duplicated)
            self.assertIn("guest_paths_unique", config["violations"])

    def test_agent_script_is_mapped_read_only(self):
        with tempfile.TemporaryDirectory() as td:
            config = backend.verify_sandbox_config(self._xml(Path(td)))
            self.assertTrue(config["checks"]["agent_mapped_read_only"])

    def test_preflight_mode_differs_from_serve_mode(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pre = backend.sandbox_config_xml(root / "in", root / "out",
                                             python_root=root / "py",
                                             mode="preflight")
            serve = backend.sandbox_config_xml(root / "in", root / "out",
                                               python_root=root / "py",
                                               mode="serve")
            self.assertIn("--handshake-only", pre)
            self.assertNotIn("--handshake-only", serve)
            self.assertFalse(backend.verify_sandbox_config(pre, mode="serve")["checks"]
                             ["handshake_only_matches_mode"])


class InterpreterPreflightTests(unittest.TestCase):
    def test_embeddable_layout_passes(self):
        with tempfile.TemporaryDirectory() as td:
            result = backend.interpreter_preflight(fake_python_root(Path(td)))
            self.assertTrue(result["ok"], result["violations"])

    def test_missing_interpreter_is_reported(self):
        with tempfile.TemporaryDirectory() as td:
            result = backend.interpreter_preflight(Path(td) / "nowhere")
            self.assertFalse(result["ok"])
            self.assertIn("directory_exists", result["violations"])

    def test_venv_is_rejected_as_non_portable(self):
        with tempfile.TemporaryDirectory() as td:
            root = fake_python_root(Path(td))
            (root / "pyvenv.cfg").write_text("home = C:\\host\\python", encoding="utf-8")
            result = backend.interpreter_preflight(root)
            self.assertIn("no_venv_marker", result["violations"])


class PreflightTests(unittest.TestCase):
    """Handshake-only workflow: record the attestation, publish nothing."""

    def _report(self, transport, inbox, outbox, hello):
        def launch():
            self.assertTrue((inbox / "session.json").exists(),
                            "session.json must exist before the Sandbox starts")
            write_hello(outbox, transport._nonce, **hello)
            return {"launched": "fake"}
        return transport.preflight(inbox, outbox, launch=launch)

    def test_valid_handshake_records_attestation_and_publishes_no_job(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox, outbox = root / "in", root / "out"
            transport = backend.WindowsSandboxTransport(handshake_timeout=5)
            report = self._report(transport, inbox, outbox, {})
            self.assertTrue(report["attestation"]["verified"])
            self.assertEqual(report["attestation"]["agent"]["user"], WDAG)
            self.assertEqual(report["jobs_published"], 0)
            self.assertEqual(report["response_files"], [])
            self.assertFalse(report["evaluation_attempted"])
            self.assertFalse((inbox / "job.json").exists())
            self.assertEqual(sorted(p.name for p in outbox.glob("response-*.json")), [])

    def test_preflight_rejects_a_wrong_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            transport = backend.WindowsSandboxTransport(handshake_timeout=5)
            with self.assertRaises(backend.BoundaryNotEstablished) as ctx:
                self._report(transport, root / "in", root / "out",
                             {"user": "DESKTOP-ABC\\Foued"})
            self.assertIn("account=False", str(ctx.exception))
            self.assertFalse(transport.isolation_verified)

    def test_preflight_rejects_an_untrusted_inside_sandbox_flag(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            transport = backend.WindowsSandboxTransport(handshake_timeout=5)
            with self.assertRaises(backend.BoundaryNotEstablished) as ctx:
                self._report(transport, root / "in", root / "out", {"inside": False})
            self.assertIn("inside_sandbox=False", str(ctx.exception))

    def test_preflight_rejects_a_stale_nonce(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox, outbox = root / "in", root / "out"
            transport = backend.WindowsSandboxTransport(handshake_timeout=5)

            def launch():
                write_hello(outbox, "stale-nonce")
                return None

            with self.assertRaises(backend.BoundaryNotEstablished) as ctx:
                transport.preflight(inbox, outbox, launch=launch)
            self.assertIn("nonce=False", str(ctx.exception))

    def test_preflight_times_out_without_an_agent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            transport = backend.WindowsSandboxTransport(handshake_timeout=0.4)
            started = time.monotonic()
            with self.assertRaises(backend.BoundaryNotEstablished):
                transport.preflight(root / "in", root / "out")
            self.assertLess(time.monotonic() - started, 10)

    def test_agent_started_before_the_session_polls_then_handshakes(self):
        """Either launch order must work; the agent may not exit on a missing session."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox, outbox = root / "in", root / "out"
            inbox.mkdir(parents=True, exist_ok=True)
            outbox.mkdir(parents=True, exist_ok=True)
            proc = subprocess.Popen(
                [sys.executable, "-I", str(V9 / "sandbox_agent.py"),
                 "--inbox", str(inbox), "--outbox", str(outbox),
                 "--handshake-only", "--allow-host", "--session-timeout", "30"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            try:
                time.sleep(1.0)
                self.assertIsNone(proc.poll(), "agent exited because session.json was absent")

                transport = backend.WindowsSandboxTransport(handshake_timeout=30)
                transport.prepare(inbox, outbox)
                with self.assertRaises(backend.BoundaryNotEstablished):
                    transport.await_handshake()
                hello = json.loads((outbox / "hello.json").read_text(encoding="utf-8"))
                self.assertEqual(hello["nonce"], transport._nonce)
                self.assertFalse(hello["inside_sandbox"])
                self.assertEqual(hello["mode"], "preflight")
            finally:
                proc.kill()
                proc.wait(timeout=10)

    def test_agent_reports_missing_session_and_exits_3(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            proc = subprocess.run(
                [sys.executable, "-I", str(V9 / "sandbox_agent.py"),
                 "--inbox", str(root / "in"), "--outbox", str(root / "out"),
                 "--handshake-only", "--allow-host", "--session-timeout", "0.5"],
                capture_output=True, text=True, timeout=120,
                encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 3)
            self.assertIn("no_session", proc.stderr)


class ResponseTrustTests(unittest.TestCase):
    """The outbox is candidate-writable, so the host validates it strictly."""

    def test_accepts_a_well_formed_response(self):
        record = backend.validate_response(valid_response(), "a" * 32)
        self.assertEqual(record["status"], "ok")

    def test_rejects_missing_fields(self):
        broken = valid_response()
        del broken["tree_empty"]
        with self.assertRaises(backend.FatalBoundaryError):
            backend.validate_response(broken)

    def test_rejects_an_unknown_status(self):
        with self.assertRaises(backend.FatalBoundaryError):
            backend.validate_response(valid_response(status="definitely_fine"))

    def test_rejects_a_job_id_mismatch(self):
        with self.assertRaises(backend.FatalBoundaryError):
            backend.validate_response(valid_response(), "c" * 32)

    def test_rejects_a_boolean_where_an_answer_is_expected(self):
        with self.assertRaises(backend.FatalBoundaryError):
            backend.validate_response(valid_response(answer=True))

    def test_rejects_an_oversized_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "response.json"
            path.write_text("x" * (backend.RESPONSE_LIMIT_BYTES + 1), encoding="utf-8")
            with self.assertRaises(backend.FatalBoundaryError) as ctx:
                backend.read_trusted_response(path)
            self.assertIn("over the", str(ctx.exception))

    def test_rejects_invalid_json(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "response.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(backend.FatalBoundaryError):
                backend.read_trusted_response(path)

    def test_reads_a_valid_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "response.json"
            path.write_text(json.dumps(valid_response()), encoding="utf-8")
            self.assertEqual(backend.read_trusted_response(path)["job_id"], "a" * 32)


class CommandLineTests(unittest.TestCase):
    def test_verify_boundary_reports_the_current_identity(self):
        proc = subprocess.run([sys.executable, "-I", str(V9 / "controller.py"), "--verify-boundary"],
                              capture_output=True, text=True, timeout=120,
                              encoding="utf-8", errors="replace")
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["inside_sandbox"], backend.current_identity()["inside_sandbox"])
        self.assertEqual(proc.returncode, 0 if payload["inside_sandbox"] else 2)

    def test_cli_refuses_host_evaluation_without_explicit_consent(self):
        proc = subprocess.run(
            [sys.executable, "-I", str(V9 / "controller.py"),
             "--bodies", str(HERE / "fixtures"), "--transport", "host-local"],
            capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace",
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("not an isolation boundary", proc.stderr)

    def test_write_sandbox_config_requires_a_mapped_interpreter(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "v9.wsb"
            proc = subprocess.run(
                [sys.executable, "-I", str(V9 / "controller.py"),
                 "--write-sandbox-config", str(target),
                 "--inbox", str(Path(td) / "in"), "--outbox", str(Path(td) / "out")],
                capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 2)
            self.assertIn("--python-root", proc.stderr)
            self.assertFalse(target.exists())

    def test_write_sandbox_config_produces_a_verified_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "v9.wsb"
            proc = subprocess.run(
                [sys.executable, "-I", str(V9 / "controller.py"),
                 "--write-sandbox-config", str(target),
                 "--inbox", str(root / "in"), "--outbox", str(root / "out"),
                 "--python-root", str(fake_python_root(root))],
                capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(target.exists())
            config = backend.verify_sandbox_config(target.read_text(encoding="utf-8"),
                                                   mode="preflight")
            self.assertTrue(config["ok"], config["violations"])

    def test_preflight_refuses_to_be_combined_with_bodies(self):
        proc = subprocess.run(
            [sys.executable, "-I", str(V9 / "controller.py"),
             "--preflight", "--bodies", str(HERE / "fixtures"),
             "--inbox", "in", "--outbox", "out", "--python-root", "py"],
            capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace",
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("handshake-only", proc.stderr)

    def test_preflight_failure_is_recorded_and_publishes_nothing(self):
        """End-to-end CLI: interpreter + config pass, no agent, so the gate stays open."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            report = root / "reports" / "preflight.json"
            inbox, outbox = root / "in", root / "out"
            proc = subprocess.run(
                [sys.executable, "-I", str(V9 / "controller.py"),
                 "--preflight", "--inbox", str(inbox), "--outbox", str(outbox),
                 "--python-root", str(fake_python_root(root)),
                 "--wsb-out", str(root / "v9.wsb"),
                 "--report", str(report),
                 "--handshake-timeout", "0.5"],
                capture_output=True, text=True, timeout=180, encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error"], "BoundaryNotEstablished")
            self.assertFalse(payload["evaluation_attempted"])
            self.assertEqual(payload["candidate_files"], [])
            self.assertTrue(payload["config"]["ok"], payload["config"]["violations"])
            self.assertFalse((inbox / "job.json").exists())
            self.assertFalse((root / "v9.wsb").read_text(encoding="utf-8").count("--bodies"))

    @unittest.skipUnless(ON_HOST, "only meaningful outside Windows Sandbox")
    def test_supervisor_refuses_host_execution_when_sandbox_is_required(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            proc = subprocess.run(
                [sys.executable, "-I", str(V9 / "supervisor.py"),
                 "--staging", str(root / "s"), "--response-dir", str(root / "r"),
                 "--scratch", str(root / "c"), "--timeout", "1",
                 "--memory-bytes", str(1024 * 1024), "--max-processes", "2",
                 "--require-sandbox"],
                capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 2)
            self.assertIn("not_inside_windows_sandbox", proc.stdout)


class RendezvousTests(unittest.TestCase):
    """Two-token ordering, exercised through the real transport interface."""

    def test_tokens_are_ordered_and_distinct(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = controller.Controller(
                root / "work", transport=backend.HostLocalTransport(root / "rt")
            )
            result = controller.run_rendezvous(ctl, HERE / "fixtures" / "echo_input.py")
            self.assertTrue(result["ordering_ok"], result["checks"])
            self.assertFalse(result["attested"], "host-local must never claim attestation")
            self.assertEqual(result["tokens"], {"A": 111, "B": 222})
            seen = {event["event"]: event.get("token_seen") for event in result["events"]}
            self.assertEqual(seen["response_A"], 111)
            self.assertEqual(seen["response_B"], 222)
            self.assertTrue(result["checks"]["B_not_visible_before_A_completed"])
            names = [event["event"] for event in result["events"]]
            self.assertLess(names.index("publish_A"), names.index("response_A"))
            self.assertLess(names.index("response_A"), names.index("publish_B"))
            self.assertLess(names.index("publish_B"), names.index("response_B"))

    def test_cli_refuses_rendezvous_on_the_host_without_consent(self):
        proc = subprocess.run(
            [sys.executable, "-I", str(V9 / "controller.py"),
             "--rendezvous", "--inbox", "in", "--outbox", "out"],
            capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace",
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("not an isolation boundary", proc.stderr)

    def test_cli_runs_the_harness_with_explicit_host_consent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            report = root / "rendezvous.json"
            proc = subprocess.run(
                [sys.executable, "-I", str(V9 / "controller.py"),
                 "--rendezvous", "--transport", "host-local", "--allow-host-local",
                 "--inbox", str(root / "in"), "--outbox", str(root / "out"),
                 "--work-root", str(root / "work"), "--report", str(report),
                 "--rendezvous-body", str(HERE / "fixtures" / "echo_input.py")],
                capture_output=True, text=True, timeout=180,
                encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertTrue(payload["ordering_ok"], payload["checks"])
            self.assertFalse(payload["attested"])


if __name__ == "__main__":
    unittest.main()
