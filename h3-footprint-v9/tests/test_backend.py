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
import sandbox_agent  # noqa: E402
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


class StagingTests(unittest.TestCase):
    """Staging must not rewrite files a live Sandbox mapping holds open."""

    def test_staging_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            names = controller.stage_runtime(dest)
            before = {n: (dest / n).stat().st_mtime_ns for n in names}
            self.assertEqual(controller.stage_runtime(dest), names)
            after = {n: (dest / n).stat().st_mtime_ns for n in names}
            self.assertEqual(before, after, "identical files must not be rewritten")

    def test_verify_only_rejects_a_differing_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            controller.stage_runtime(dest)
            (dest / "protocol.py").write_text("# tampered\n", encoding="utf-8")
            with self.assertRaises(backend.FatalBoundaryError):
                controller.stage_runtime(dest, verify_only=True)
            self.assertEqual((dest / "protocol.py").read_text(encoding="utf-8"),
                             "# tampered\n", "verify_only must not write")

    def test_staging_repairs_a_differing_runtime_when_writing_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            controller.stage_runtime(dest)
            (dest / "protocol.py").write_text("# tampered\n", encoding="utf-8")
            controller.stage_runtime(dest)
            self.assertEqual((dest / "protocol.py").read_bytes(),
                             (V9 / "protocol.py").read_bytes())


class PublishTests(unittest.TestCase):
    """The mapped-folder path cannot rename, so publishing must be able to skip it."""

    def test_direct_publish_is_readable_and_leaves_no_temp_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            staging = Path(tmp)
            job = {
                "v9": protocol.JOB_SCHEMA, "job_id": "a" * 32, "sequence": 1,
                "kind": "system", "body_sha256": protocol.sha256_bytes(b"print(1)\n"),
                "probe_index": None, "input": None, "limits": {},
            }
            protocol.publish_job(staging, job, body=b"print(1)\n", atomic=False)
            self.assertEqual(protocol.read_job(staging)["job_id"], "a" * 32)
            self.assertEqual(sorted(p.name for p in staging.iterdir()),
                             ["body.py", "job.json"])

    def test_direct_publish_overwrites_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            staging = Path(tmp)
            for index, body in ((1, b"print(1)\n"), (2, b"print(2)\n")):
                job = {
                    "v9": protocol.JOB_SCHEMA, "job_id": str(index) * 32,
                    "sequence": index, "kind": "system",
                    "body_sha256": protocol.sha256_bytes(body),
                    "probe_index": None, "input": None, "limits": {},
                }
                protocol.publish_job(staging, job, body=body, atomic=False)
            self.assertEqual(protocol.read_job(staging)["job_id"], "2" * 32)
            self.assertEqual((staging / "body.py").read_bytes(), b"print(2)\n")


NONCE = "c" * 32


class _AttestedStub:
    """A transport that claims a verified Sandbox attestation but must never run."""

    name = "attested-stub"
    requires_sandbox = True
    isolation_verified = True

    def __init__(self) -> None:
        self.calls = 0

    def attestation(self) -> dict:
        return {"verified": True, "transport": self.name}

    def execute(self, *args, **kwargs):
        self.calls += 1
        raise AssertionError("the execution gate must refuse before any call to execute()")


class ExecutionGateTests(unittest.TestCase):
    """A verified handshake is necessary, never sufficient."""

    def test_verified_handshake_cannot_bypass_the_prerequisite_gate(self):
        with tempfile.TemporaryDirectory() as td:
            stub = _AttestedStub()
            ctl = controller.Controller(Path(td) / "work", transport=stub)
            with self.assertRaises(controller.ExecutionNotAuthorized) as ctx:
                ctl.evaluate_authorized(fixture("correct.py"))
            message = str(ctx.exception)
            self.assertIn("prerequisite blocker", message)
            self.assertIn("sandbox_rendezvous_ordering", message)
            self.assertEqual(stub.calls, 0, "no job may be published before the gate passes")

    def test_attested_sandbox_cannot_use_the_unauthorized_path(self):
        with tempfile.TemporaryDirectory() as td:
            stub = _AttestedStub()
            ctl = controller.Controller(Path(td) / "work", transport=stub)
            with self.assertRaises(backend.BoundaryNotEstablished):
                ctl.evaluate(fixture("correct.py"))
            self.assertEqual(stub.calls, 0)

    def test_host_local_scoring_path_still_works(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = controller.Controller(
                root / "work", transport=backend.HostLocalTransport(root / "rt")
            )
            row = ctl.evaluate(fixture("correct.py"))
            self.assertFalse(row["authorized"])
            self.assertEqual(row["fails"], [False] * 30)

    def test_cli_refuses_sandbox_evaluation_before_staging_anything(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox, outbox = root / "in", root / "out"
            proc = subprocess.run(
                [sys.executable, "-I", str(V9 / "controller.py"),
                 "--bodies", str(HERE / "fixtures"), "--transport", "sandbox",
                 "--inbox", str(inbox), "--outbox", str(outbox)],
                capture_output=True, text=True, timeout=120,
                encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertIn("refusing authorized evaluation", proc.stderr)
            self.assertIn("sandbox_rendezvous_ordering", proc.stderr)
            self.assertFalse(inbox.exists(), "nothing may be staged before the gate passes")
            self.assertFalse(outbox.exists())
            self.assertFalse((root / "runs").exists())

    def test_cli_check_execution_gate_reports_the_blockers(self):
        proc = subprocess.run(
            [sys.executable, "-I", str(V9 / "controller.py"), "--check-execution-gate"],
            capture_output=True, text=True, timeout=120,
            encoding="utf-8", errors="replace",
        )
        self.assertEqual(proc.returncode, 2)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["ok"])
        ids = {item["id"] for item in payload["blockers"]}
        self.assertIn("authorization_missing", ids)
        self.assertIn("gate_not_passing:sandbox_isolation_report", ids)


class TelemetryValidationTests(unittest.TestCase):
    """Guest events arrive through the writable mapping, so the host distrusts them."""

    def _outbox(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        outbox = Path(tmp.name) / "out"
        outbox.mkdir(parents=True)
        return outbox

    def _record(self, seq: int, event: str = "heartbeat", **overrides) -> dict:
        record = {
            "v9": protocol.JOB_SCHEMA,
            "nonce": NONCE,
            "pid": 4242,
            "seq": seq,
            "event": event,
            "phase": "serve",
            "timestamp": time.time(),
            "job_id": None,
            "job_sequence": None,
            "detail": None,
        }
        record.update(overrides)
        return record

    def _write(self, outbox: Path, record: dict) -> Path:
        path = outbox / protocol.event_filename(
            record["nonce"], record["pid"], record["seq"], record["event"])
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def test_valid_events_are_ordered_by_sequence(self):
        outbox = self._outbox()
        self._write(outbox, self._record(2, "heartbeat"))
        self._write(outbox, self._record(1, "agent_start", phase="startup"))
        collected = backend.collect_events(outbox, NONCE, expected_pid=4242)
        self.assertEqual([event["seq"] for event in collected["events"]], [1, 2])
        self.assertEqual(collected["anomalies"], [])
        self.assertEqual(collected["max_seq"], 2)

    def test_events_from_another_session_are_ignored(self):
        outbox = self._outbox()
        self._write(outbox, self._record(1, nonce="d" * 32))
        collected = backend.collect_events(outbox, NONCE)
        self.assertEqual(collected["events"], [])
        self.assertEqual(collected["foreign_events"], 1)

    def test_a_malformed_filename_is_an_anomaly(self):
        outbox = self._outbox()
        (outbox / "event-not-a-name.json").write_text("{}", encoding="utf-8")
        collected = backend.collect_events(outbox, NONCE)
        self.assertEqual(collected["anomalies"][0]["error"], "malformed_event_name")

    def test_a_schema_violation_is_an_anomaly(self):
        outbox = self._outbox()
        record = self._record(1)
        record["extra"] = "field"
        self._write(outbox, record)
        collected = backend.collect_events(outbox, NONCE)
        self.assertIn("keys differ", collected["anomalies"][0]["error"])

    def test_an_oversized_event_is_an_anomaly(self):
        outbox = self._outbox()
        path = self._write(outbox, self._record(1))
        path.write_text(path.read_text(encoding="utf-8") + " " * 5000, encoding="utf-8")
        collected = backend.collect_events(outbox, NONCE)
        self.assertIn("over the", collected["anomalies"][0]["error"])

    def test_a_pid_that_differs_from_the_handshake_is_an_anomaly(self):
        outbox = self._outbox()
        self._write(outbox, self._record(1))
        collected = backend.collect_events(outbox, NONCE, expected_pid=9999)
        self.assertIn("does not match the attested agent", collected["anomalies"][0]["error"])

    def test_filename_must_agree_with_its_content(self):
        outbox = self._outbox()
        record = self._record(1)
        path = outbox / protocol.event_filename(NONCE, 4242, 7, "heartbeat")
        path.write_text(json.dumps(record), encoding="utf-8")
        collected = backend.collect_events(outbox, NONCE)
        self.assertIn("filename disagrees", collected["anomalies"][0]["error"])

    def test_agent_event_log_writes_unique_direct_files(self):
        outbox = self._outbox()
        log = sandbox_agent.EventLog(outbox, NONCE)
        log.emit("agent_start", phase="startup")
        log.emit("heartbeat", phase="serve")
        names = sorted(path.name for path in outbox.iterdir())
        self.assertEqual(len(names), 2)
        self.assertTrue(all(name.endswith(".json") and not name.endswith(".tmp")
                            for name in names))
        collected = backend.collect_events(outbox, NONCE)
        self.assertEqual([event["seq"] for event in collected["events"]], [1, 2])
        self.assertEqual(collected["anomalies"], [])

    @staticmethod
    def _state(**overrides) -> dict:
        state = {
            "poll_count": 3,
            "last_poll_at": time.time(),
            "scanned": True,
            "visible": ["job-000001-" + "a" * 32 + ".json"],
            "visible_count": 1,
            "outcome": "only_handled",
            "last_job_id": "a" * 32,
            "last_job_sequence": 1,
            "error": None,
            "error_file": None,
        }
        state.update(overrides)
        return state

    def test_poll_state_and_snapshotted_heartbeat_are_valid(self):
        outbox = self._outbox()
        self._write(outbox, self._record(1, "poll_state", state=self._state()))
        self._write(outbox, self._record(2, "heartbeat", state=self._state()))
        collected = backend.collect_events(outbox, NONCE, expected_pid=4242)
        self.assertEqual(collected["anomalies"], [])
        self.assertEqual(collected["events"][0]["state"]["outcome"], "only_handled")

    def test_poll_state_without_a_state_is_an_anomaly(self):
        outbox = self._outbox()
        self._write(outbox, self._record(1, "poll_state"))
        collected = backend.collect_events(outbox, NONCE)
        self.assertIn("has no state", collected["anomalies"][0]["error"])

    def test_state_is_refused_on_other_events(self):
        outbox = self._outbox()
        self._write(outbox, self._record(1, "job_discovered", state=self._state()))
        collected = backend.collect_events(outbox, NONCE)
        self.assertIn("only allowed on heartbeat or poll_state",
                      collected["anomalies"][0]["error"])

    def test_an_invented_scan_outcome_is_an_anomaly(self):
        outbox = self._outbox()
        self._write(outbox, self._record(
            1, "poll_state", state=self._state(outcome="definitely_fresh")))
        collected = backend.collect_events(outbox, NONCE)
        self.assertIn("is not allowed", collected["anomalies"][0]["error"])

    def test_an_unbounded_visible_list_is_an_anomaly(self):
        outbox = self._outbox()
        visible = [f"job-{index:06d}-{'a' * 32}.json"
                   for index in range(protocol.EVENT_VISIBLE_LIMIT + 1)]
        self._write(outbox, self._record(
            1, "poll_state", state=self._state(visible=visible, visible_count=len(visible))))
        collected = backend.collect_events(outbox, NONCE)
        self.assertIn("bounded list", collected["anomalies"][0]["error"])

    def test_state_keys_must_match_exactly(self):
        outbox = self._outbox()
        state = self._state()
        state["extra"] = "field"
        self._write(outbox, self._record(1, "poll_state", state=state))
        collected = backend.collect_events(outbox, NONCE)
        self.assertIn("event state keys differ", collected["anomalies"][0]["error"])


class ScriptedGuestTransport:
    """A Sandbox-shaped transport that emits guest telemetry from a script."""

    name = "scripted-guest"

    def __init__(self, outbox: Path, *, alive_after_b: bool = True,
                 discover_b: bool = True, start_b: bool = True,
                 respond_b: bool = True, poll_after_b: bool = True,
                 polls: int = 2, b_in_scan: bool = False,
                 b_out_of_order: bool = False, scanned: bool = True) -> None:
        self.outbox = Path(outbox)
        self.nonce = NONCE
        self.requires_sandbox = True
        self.isolation_verified = True
        self.alive_after_b = alive_after_b
        self.discover_b = discover_b
        self.start_b = start_b
        self.respond_b = respond_b
        self.poll_after_b = poll_after_b
        self.polls = polls
        self.b_in_scan = b_in_scan
        self.b_out_of_order = b_out_of_order
        self.scanned = scanned
        self._pid = 5150
        self._seq = 0

    def attestation(self) -> dict:
        return {"verified": True, "transport": self.name, "agent": {"pid": self._pid}}

    def emit(self, name: str, job: dict | None = None, detail: str | None = None,
             state: dict | None = None) -> None:
        self._seq += 1
        record = {
            "v9": protocol.JOB_SCHEMA,
            "nonce": self.nonce,
            "pid": self._pid,
            "seq": self._seq,
            "event": name,
            "phase": "serve",
            "timestamp": time.time(),
            "job_id": job.get("job_id") if job else None,
            "job_sequence": job.get("sequence") if job else None,
            "detail": detail,
        }
        if state is not None:
            record["state"] = state
        protocol.write_event(self.outbox, record)

    def _poll_state(self, job: dict, poll_count: int) -> dict:
        if self.b_out_of_order:
            outcome, error, error_file = "out_of_order", None, None
        elif self.b_in_scan:
            outcome, error, error_file = (
                "error", "filename_payload_mismatch",
                f"job-000002-{job['job_id']}.json",
            )
        else:
            outcome, error, error_file = "no_jobs", None, None
        visible = ([f"job-000002-{job['job_id']}.json"]
                   if (self.b_in_scan or self.b_out_of_order) else [])
        return {
            "poll_count": poll_count,
            "last_poll_at": time.time(),
            "scanned": self.scanned,
            "visible": visible,
            "visible_count": len(visible),
            "outcome": outcome,
            "last_job_id": None,
            "last_job_sequence": None,
            "error": error,
            "error_file": error_file,
        }

    def _emit_polls(self, job: dict) -> None:
        for offset in range(self.polls):
            self.emit("poll_state", state=self._poll_state(job, 10 + offset))

    def _respond(self, job: dict, answer: int) -> dict:
        record = {
            "v9": protocol.JOB_SCHEMA,
            "job_id": job["job_id"],
            "sequence": job["sequence"],
            "kind": job["kind"],
            "body_sha256": job["body_sha256"],
            "probe_index": job.get("probe_index"),
            "status": "ok",
            "tree_empty": True,
            "answer": answer,
            "inside_sandbox": True,
            "raw_stdout": "",
        }
        protocol.write_response_exclusive(self.outbox, record)
        return record

    def execute(self, staging: Path, response_dir: Path, scratch: Path, *,
                timeout: float, memory_bytes: int, max_processes: int) -> dict:
        job = protocol.read_job(staging)
        if job["input"]["n"] == 111:
            self.emit("job_discovered", job)
            self.emit("job_started", job)
            self.emit("response_written", job)
            return self._respond(job, 111)

        if self.alive_after_b:
            self.emit("heartbeat")
        if not self.discover_b:
            if self.poll_after_b:
                self._emit_polls(job)
            raise backend.FatalBoundaryError("no Sandbox response for job B within 125s")
        self.emit("job_discovered", job)
        if not self.start_b:
            raise backend.FatalBoundaryError("no Sandbox response for job B within 125s")
        self.emit("job_started", job)
        if not self.respond_b:
            raise backend.FatalBoundaryError("no Sandbox response for job B within 125s")
        self.emit("response_written", job)
        return self._respond(job, 222)


class RendezvousDiagnosticTests(unittest.TestCase):
    """The four cases the work order names, driven through run_rendezvous."""

    def _controller(self, **behaviour) -> controller.Controller:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        inbox, outbox, scratch = root / "in", root / "out", root / "scratch"
        for path in (inbox, outbox, scratch):
            path.mkdir(parents=True, exist_ok=True)
        controller.stage_runtime(inbox)
        transport = ScriptedGuestTransport(outbox, **behaviour)
        return controller.Controller(root / "work", transport=transport,
                                     case_paths=(inbox, outbox, scratch))

    def _run(self, **behaviour) -> dict:
        return controller.run_rendezvous(
            self._controller(**behaviour), HERE / "fixtures" / "echo_input.py"
        )

    def test_normal_completion_of_a_and_b(self):
        result = self._run()
        self.assertTrue(result["ordering_ok"], result["checks"])
        self.assertIsNone(result["diagnostic"])
        self.assertEqual(
            [event["event"] for event in result["guest_events"]
             if event["event"] != "poll_state"],
            ["job_discovered", "job_started", "response_written",
             "heartbeat", "job_discovered", "job_started", "response_written"],
        )
        self.assertEqual(result["telemetry_anomalies"], [])

    def test_agent_that_stops_after_a(self):
        result = self._run(alive_after_b=False, discover_b=False)
        self.assertFalse(result["ordering_ok"])
        self.assertEqual(result["diagnostic"]["classification"], "agent_stopped")
        self.assertFalse(result["diagnostic"]["agent_alive_after_b"])
        self.assertTrue(result["checks"]["A_answered_with_A"])

    def test_heartbeat_alone_does_not_prove_loop_progress(self):
        result = self._run(discover_b=False, poll_after_b=False)
        self.assertFalse(result["ordering_ok"])
        diagnostic = result["diagnostic"]
        self.assertEqual(diagnostic["classification"], "job_loop_progress_unknown")
        self.assertTrue(diagnostic["agent_alive_after_b"])
        self.assertFalse(diagnostic["job_loop_progressing"])
        self.assertFalse(diagnostic["job_b_discovered"])

    def test_agent_polls_but_never_lists_b(self):
        result = self._run(discover_b=False)
        self.assertFalse(result["ordering_ok"])
        diagnostic = result["diagnostic"]
        self.assertEqual(diagnostic["classification"], "inbox_not_refreshed")
        self.assertTrue(diagnostic["agent_alive_after_b"])
        self.assertTrue(diagnostic["job_loop_progressing"])
        self.assertFalse(diagnostic["job_b_seen_in_scan"])
        self.assertFalse(diagnostic["job_b_discovered"])

    def test_b_visible_but_not_usable(self):
        result = self._run(discover_b=False, b_in_scan=True)
        self.assertFalse(result["ordering_ok"])
        diagnostic = result["diagnostic"]
        self.assertEqual(diagnostic["classification"], "job_request_unusable")
        self.assertTrue(diagnostic["job_b_seen_in_scan"])
        self.assertFalse(diagnostic["job_b_discovered"])

    def test_b_visible_out_of_order(self):
        result = self._run(discover_b=False, b_out_of_order=True)
        self.assertFalse(result["ordering_ok"])
        diagnostic = result["diagnostic"]
        self.assertEqual(diagnostic["classification"], "job_request_out_of_order")
        self.assertEqual(diagnostic["last_scan_outcome"], "out_of_order")
        self.assertFalse(diagnostic["job_b_discovered"])

    def test_b_observed_but_no_response_published(self):
        result = self._run(respond_b=False)
        self.assertFalse(result["ordering_ok"])
        self.assertEqual(result["diagnostic"]["classification"],
                         "supervisor_or_response_path")
        self.assertTrue(result["diagnostic"]["job_b_discovered"])
        self.assertTrue(result["diagnostic"]["job_b_started"])
        self.assertFalse(result["diagnostic"]["job_b_response_written"])

    def test_host_local_transport_has_no_guest_telemetry(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = controller.Controller(
                root / "work", transport=backend.HostLocalTransport(root / "rt")
            )
            snapshot = controller._snapshot(ctl)
            self.assertEqual(snapshot["events"], [])
            self.assertIsNone(controller._telemetry_source(ctl))


if __name__ == "__main__":
    unittest.main()
