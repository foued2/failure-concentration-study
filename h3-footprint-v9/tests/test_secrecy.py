from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import backend  # noqa: E402
import controller  # noqa: E402
import protocol  # noqa: E402

V9 = HERE.parent
FORBIDDEN_IN_SANDBOX = {"oracle.py", "constants.py", "controller.py",
                        "expected_values.json", "instrument.py", "job.json"}


class SandboxImageTests(unittest.TestCase):
    def _controller(self, td) -> controller.Controller:
        root = Path(td)
        return controller.Controller(root / "work",
                                     transport=backend.HostLocalTransport(root / "rt"))

    def test_runtime_contains_only_supervisor_and_child(self):
        with tempfile.TemporaryDirectory() as td:
            ctl = self._controller(td)
            present = {p.name for p in ctl.runtime.iterdir()}
            self.assertEqual(present, set(controller.SANDBOX_RUNTIME_FILES))
            self.assertEqual(present & FORBIDDEN_IN_SANDBOX, set())

    def test_no_reference_data_anywhere_in_runtime(self):
        with tempfile.TemporaryDirectory() as td:
            ctl = self._controller(td)
            blob = "\n".join(p.read_text(encoding="utf-8") for p in ctl.runtime.glob("*.py"))
            self.assertNotIn("EXPECTED", blob)
            self.assertNotIn("probe_id", blob)
            self.assertNotIn("family_counts", blob)

    def test_supervisor_does_not_import_oracle(self):
        for name in ("supervisor.py", "child_runner.py", "sandbox_agent.py", "backend.py"):
            source = (V9 / name).read_text(encoding="utf-8")
            self.assertNotIn("import oracle", source, f"{name} must stay secret-free")
            self.assertNotIn("from oracle", source)

    def test_backend_stays_on_the_host(self):
        self.assertNotIn("backend.py", controller.SANDBOX_RUNTIME_FILES)
        self.assertNotIn("oracle.py", controller.SANDBOX_RUNTIME_FILES)
        self.assertNotIn("constants.py", controller.SANDBOX_RUNTIME_FILES)

    def test_controller_never_imports_candidate(self):
        source = (V9 / "controller.py").read_text(encoding="utf-8")
        self.assertNotIn("importlib", source)
        self.assertNotIn("exec_module", source)
        self.assertNotIn("spec_from_file_location", source)

    def test_active_job_is_one_body_and_one_input(self):
        with tempfile.TemporaryDirectory() as td:
            staging = Path(td) / "staging"
            protocol.publish_job(staging, {
                "v9": 1, "job_id": "x", "sequence": 1, "kind": "probe",
                "body_sha256": "0" * 64, "probe_index": 0,
                "input": {"n": 1, "edges": [], "s": 0, "t": 0},
                "limits": {},
            }, body=b"def solve(n, e, s, t):\n    return 0\n")
            self.assertEqual({p.name for p in staging.iterdir()}, {"body.py", "job.json"})
            job = protocol.read_job(staging)
            self.assertNotIn("expected", str(job).lower())
            self.assertNotIn("family", str(job).lower())
            self.assertNotIn("probe_id", str(job).lower())


if __name__ == "__main__":
    unittest.main()
