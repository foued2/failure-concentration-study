from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import backend  # noqa: E402
import controller  # noqa: E402
from _support import fixture  # noqa: E402

V9 = HERE.parent
ON_HOST = not backend.current_identity()["inside_sandbox"]


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
            (root / "out" / "hello.json").write_text(json.dumps({
                "nonce": "stale", "inside_sandbox": True, "user": "WDAGUtilityAccount",
            }), encoding="utf-8")
            with self.assertRaises(backend.BoundaryNotEstablished) as ctx:
                transport.await_handshake()
            self.assertIn("nonce=False", str(ctx.exception))

    def test_handshake_rejects_an_agent_running_on_the_host(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox, outbox = root / "in", root / "out"
            transport = backend.WindowsSandboxTransport(handshake_timeout=10.0)
            transport.prepare(inbox, outbox)
            proc = subprocess.Popen(
                [sys.executable, "-I", str(V9 / "sandbox_agent.py"),
                 "--inbox", str(inbox), "--outbox", str(outbox), "--allow-host"],
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
        good = {"nonce": "n", "inside_sandbox": True, "user": "desktop-abc\\WDAGUtilityAccount"}
        self.assertTrue(all(backend.validate_handshake(good, "n").values()))

    def test_rejects_each_failure_independently(self):
        base = {"nonce": "n", "inside_sandbox": True, "user": "desktop-abc\\WDAGUtilityAccount"}
        for key, value, flag in (
            ("nonce", "other", "nonce"),
            ("inside_sandbox", False, "inside_sandbox"),
            ("user", "desktop-abc\\Foued", "account"),
        ):
            checks = backend.validate_handshake({**base, key: value}, "n")
            self.assertFalse(checks[flag], f"{key} was not rejected")
            self.assertEqual(sum(1 for v in checks.values() if not v), 1)


class SandboxConfigTests(unittest.TestCase):
    def test_config_is_offline_and_maps_one_read_only_inbox(self):
        xml = backend.sandbox_config_xml(Path(r"C:\stage"), Path(r"C:\out"))
        root = ET.fromstring(xml)
        self.assertEqual(root.findtext("Networking"), "Disable")
        self.assertEqual(root.findtext("ClipboardRedirection"), "Disable")
        folders = root.findall("MappedFolders/MappedFolder")
        self.assertEqual(len(folders), 2)
        self.assertEqual(folders[0].findtext("ReadOnly"), "true")
        self.assertEqual(folders[1].findtext("ReadOnly"), "false")
        self.assertIn("sandbox_agent.py", root.findtext("LogonCommand/Command") or "")


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

    def test_write_sandbox_config_produces_a_usable_file(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "v9.wsb"
            proc = subprocess.run(
                [sys.executable, "-I", str(V9 / "controller.py"),
                 "--write-sandbox-config", str(target),
                 "--inbox", str(Path(td) / "in"), "--outbox", str(Path(td) / "out")],
                capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(target.exists())
            ET.fromstring(target.read_text(encoding="utf-8"))

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


if __name__ == "__main__":
    unittest.main()
