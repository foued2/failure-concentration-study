from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import run_container_candidate as executor
import isolated_supervisor
from candidate_child import BoundedTextIO, _validate_input


class ContainerExecutorUnitTests(unittest.TestCase):
    def test_pinned_image_is_content_addressed(self):
        self.assertIn("@sha256:", executor.PYTHON_IMAGE)
        self.assertEqual(len(executor.PYTHON_IMAGE.rsplit("@sha256:", 1)[1]), 64)

    def test_regular_file_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            real = root / "real.py"
            real.write_text("x=1\n")
            link = root / "link.py"
            try:
                link.symlink_to(real)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation unavailable on this runner")
            with self.assertRaises(executor.ContainerExecutionError):
                executor._regular_file(link, "test file")

    def test_inspect_config_accepts_expected_container_constraints(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = root / "body.py"
            supervisor = root / "isolated_supervisor.py"
            child = root / "candidate_child.py"
            for p in (body, supervisor, child):
                p.write_text("# fixture\n")
            host = {
                "NetworkMode": "none", "ReadonlyRootfs": True, "PidsLimit": 8,
                "Memory": 536870912, "MemorySwap": 536870912,
                "NanoCpus": 1000000000, "CapDrop": ["ALL"],
                "CapAdd": ["CHOWN", "SETUID", "SETGID", "KILL"],
                "SecurityOpt": ["no-new-privileges"],
                "Tmpfs": {
                    "/tmp": "rw,noexec,nosuid,size=64m,mode=0711",
                    "/dev/shm": "ro,noexec,nosuid,size=16m",
                },
            }
            mount_list = [
                {"Destination": "/candidate/body.py", "Source": str(body), "RW": False},
                {"Destination": "/trusted/isolated_supervisor.py", "Source": str(supervisor), "RW": False},
                {"Destination": "/trusted/candidate_child.py", "Source": str(child), "RW": False},
            ]
            fake = {"HostConfig": host, "Config": {"User": "0:0", "Image": executor.PYTHON_IMAGE}, "Mounts": mount_list}
            original = executor._docker
            executor._docker = lambda args, timeout=30: type("CP", (), {
                "returncode": 0, "stdout": json.dumps([fake]), "stderr": ""
            })()
            try:
                result = executor._inspect_container("id", body, supervisor, child)
            finally:
                executor._docker = original
            self.assertTrue(result["verified"])
            self.assertTrue(all(result["checks"].values()))

    def test_inspect_config_rejects_network_or_writable_root(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = root / "body.py"
            supervisor = root / "isolated_supervisor.py"
            child = root / "candidate_child.py"
            for p in (body, supervisor, child):
                p.write_text("# fixture\n")
            host = {
                "NetworkMode": "bridge", "ReadonlyRootfs": False, "PidsLimit": 8,
                "Memory": 536870912, "MemorySwap": 536870912,
                "NanoCpus": 1000000000, "CapDrop": ["ALL"],
                "CapAdd": ["CHOWN", "SETUID", "SETGID", "KILL"], "SecurityOpt": ["no-new-privileges"],
                "Tmpfs": {
                    "/tmp": "rw,noexec,nosuid,size=64m,mode=0711",
                    "/dev/shm": "ro,noexec,nosuid,size=16m",
                },
            }
            mounts = [
                {"Destination": "/candidate/body.py", "Source": str(body), "RW": False},
                {"Destination": "/trusted/isolated_supervisor.py", "Source": str(supervisor), "RW": False},
                {"Destination": "/trusted/candidate_child.py", "Source": str(child), "RW": False},
            ]
            fake = {"HostConfig": host, "Config": {"User": "0:0", "Image": executor.PYTHON_IMAGE}, "Mounts": mounts}
            original = executor._docker
            executor._docker = lambda args, timeout=30: type("CP", (), {
                "returncode": 0, "stdout": json.dumps([fake]), "stderr": ""
            })()
            try:
                with self.assertRaises(executor.ContainerExecutionError):
                    executor._inspect_container("id", body, supervisor, child)
            finally:
                executor._docker = original

    def test_prefixed_capability_names_normalize_and_missing_caps_fail(self):
        # Runtime APIs may represent the same Linux capability with an optional CAP_ prefix.
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = root / "body.py"
            supervisor = root / "isolated_supervisor.py"
            child = root / "candidate_child.py"
            for p in (body, supervisor, child):
                p.write_text("# fixture\\n")
            host = {
                "NetworkMode": "none", "ReadonlyRootfs": True, "PidsLimit": 8,
                "Memory": 536870912, "MemorySwap": 536870912,
                "NanoCpus": 1000000000, "CapDrop": ["ALL"],
                "CapAdd": ["CAP_CHOWN", "CAP_SETUID", "CAP_SETGID", "CAP_KILL"],
                "SecurityOpt": ["no-new-privileges"],
                "Tmpfs": {
                    "/tmp": "rw,noexec,nosuid,size=64m,mode=0711",
                    "/dev/shm": "ro,noexec,nosuid,size=16m",
                },
            }
            mounts = [
                {"Destination": "/candidate/body.py", "Source": str(body), "RW": False},
                {"Destination": "/trusted/isolated_supervisor.py", "Source": str(supervisor), "RW": False},
                {"Destination": "/trusted/candidate_child.py", "Source": str(child), "RW": False},
            ]
            fake = {"HostConfig": host, "Config": {"User": "0:0", "Image": executor.PYTHON_IMAGE}, "Mounts": mounts}
            original = executor._docker
            executor._docker = lambda args, timeout=30: type("CP", (), {
                "returncode": 0, "stdout": json.dumps([fake]), "stderr": ""
            })()
            try:
                result = executor._inspect_container("id", body, supervisor, child)
                self.assertTrue(result["verified"])
                host["CapAdd"] = ["CAP_CHOWN", "CAP_SETUID", "CAP_SETGID"]
                with self.assertRaises(executor.ContainerExecutionError):
                    executor._inspect_container("id", body, supervisor, child)
            finally:
                executor._docker = original

    def test_static_policy_matches_v3_for_forbidden_imports(self):
        source = """import os
def solve(n, edges, s, t):
    return 0
"""
        self.assertEqual(executor.unsafe_reason(source), "import:os")

    def test_static_policy_rejects_undefined_global(self):
        source = """def solve(n, edges, s, t):
    return missing_distance
"""
        self.assertEqual(executor.undefined_global_names(source), ["missing_distance"])

    def test_static_policy_allows_simple_self_contained_solver(self):
        source = """def solve(n, edges, s, t):
    return 0
"""
        self.assertIsNone(executor.unsafe_reason(source))
        self.assertEqual(executor.undefined_global_names(source), [])

    def test_static_rejection_report_does_not_launch_execution(self):
        with tempfile.TemporaryDirectory() as td:
            body = Path(td) / "body.py"
            body.write_text("""import socket
def solve(n, edges, s, t):
    return 0
""")
            report = executor._static_exclusion_report(body, [{"probe_id": str(i)} for i in range(30)], 5.0, "import:socket")
            self.assertFalse(report["candidate_valid"])
            self.assertEqual(report["candidate_status"], "static_rejection")
            self.assertEqual(report["probe_count"], 0)
            self.assertEqual(report["expected_probe_count"], 30)
            self.assertIsNone(report["container_config"])
            self.assertFalse(report["execution_performed"])
            self.assertIsNone(report["isolation_harness_ok"])

    def test_preflight_payload_is_answer_free(self):
        probe = {"probe_id": "real-probe", "n": 3, "edges": [[0, 1, 2]], "s": 0, "t": 1}
        payload = executor._preflight_payload(probe)
        self.assertEqual(payload["probe_id"], "__h3_preflight__")
        self.assertEqual(payload["phase"], "preflight")
        self.assertEqual(payload["n"], 3)
        self.assertEqual(payload["edges"], [[0, 1, 2]])
        self.assertEqual(set(payload), {"probe_id", "phase", "n", "edges", "s", "t"})
        self.assertFalse(any("answer" in key.lower() or "expected" in key.lower() for key in payload))

    def test_preflight_classifies_load_error_as_invalid_candidate_not_k(self):
        valid, status, error = executor._preflight_state({
            "phase": "preflight", "status": "load_error", "error_type": "ImportError"
        })
        self.assertFalse(valid)
        self.assertEqual(status, "load_error")
        self.assertEqual(error, "ImportError")

    def test_preflight_accepts_only_callable_without_output_overflow(self):
        record = {"phase": "preflight", "status": "ok", "answer_type": "callable",
                  "answer": None, "solver_output_overflow": False}
        self.assertEqual(executor._preflight_state(record), (True, "valid", None))
        record["solver_output_overflow"] = True
        self.assertEqual(executor._preflight_state(record), (False, "preflight_output_overflow", None))

    def test_preflight_timeout_is_not_a_probe_failure(self):
        valid, status, error = executor._preflight_state({"phase": "preflight", "status": "timeout"})
        self.assertFalse(valid)
        self.assertEqual(status, "preflight_timeout")
        self.assertIsNone(error)

    def test_overflow_status_is_preserved_by_supervisor_parser(self):
        record = {
            "v": 1, "phase": "probe", "probe_id": "p", "status": "output_overflow",
            "answer_type": "none", "answer": None, "solver_output_overflow": True,
        }
        parsed = isolated_supervisor._parse_prediction("H3PRED " + json.dumps(record), "p")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["status"], "output_overflow")

    def test_preflight_payload_has_an_explicit_phase(self):
        payload = {"probe_id": "__preflight__", "phase": "preflight",
                   "n": 1, "edges": [], "s": 0, "t": 0}
        parsed = _validate_input(payload)
        self.assertEqual(parsed[-1], "preflight")
        self.assertEqual(parsed[-2], "__preflight__")

    def test_invalid_phase_is_rejected(self):
        payload = {"probe_id": "p", "phase": "score",
                   "n": 1, "edges": [], "s": 0, "t": 0}
        with self.assertRaises(ValueError):
            _validate_input(payload)

    def test_supervisor_accepts_load_error_as_distinct_from_probe_exception(self):
        record = {
            "v": 1, "phase": "probe", "probe_id": "p", "status": "load_error",
            "error_type": "ImportError", "answer_type": "none", "answer": None,
            "solver_output_overflow": False,
        }
        parsed = isolated_supervisor._parse_prediction("H3PRED " + json.dumps(record), "p")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["status"], "load_error")

    def test_supervisor_rejects_a_phase_mismatch(self):
        record = {
            "v": 1, "phase": "preflight", "probe_id": "p", "status": "ok",
            "answer_type": "callable", "answer": None, "solver_output_overflow": False,
        }
        self.assertIsNone(isolated_supervisor._parse_prediction(
            "H3PRED " + json.dumps(record), "p", "probe"
        ))
        self.assertIsNotNone(isolated_supervisor._parse_prediction(
            "H3PRED " + json.dumps(record), "p", "preflight"
        ))

    def test_supervisor_rejects_overflowed_solver_output(self):
        record = {
            "v": 1, "phase": "probe", "probe_id": "p", "status": "ok",
            "answer_type": "int", "answer": 4, "solver_output_overflow": True,
        }
        self.assertIsNone(isolated_supervisor._parse_prediction(
            "H3PRED " + json.dumps(record), "p"
        ))

    def test_bounded_text_io_marks_overflow_without_retaining_it(self):
        stream = BoundedTextIO(limit=5)
        self.assertEqual(stream.write("abcd"), 4)
        self.assertEqual(stream.write("xyz"), 3)
        self.assertEqual(stream.characters, 5)
        self.assertTrue(stream.overflow)
        self.assertEqual("".join(stream.parts), "abcdx")

    def test_bad_probe_shapes_fail_before_docker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = root / "body.py"
            trusted = root / "trusted"
            trusted.mkdir()
            (trusted / "isolated_supervisor.py").write_text("# supervisor\n")
            (trusted / "candidate_child.py").write_text("# child\n")
            body.write_text("def solve(n,edges,s,t): return 0\n")
            with self.assertRaises(ValueError):
                executor.run_candidate(body, trusted, [])
            with self.assertRaises(ValueError):
                executor.run_candidate(body, trusted, [{"probe_id": "x"}, {"probe_id": "x"}])


if __name__ == "__main__":
    unittest.main()
