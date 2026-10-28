from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import container_eval


class MinimalImageBoundaryTests(unittest.TestCase):
    def test_image_context_contains_only_the_worker_and_dockerfile(self):
        files = {path.name for path in container_eval.IMAGE_CONTEXT.iterdir() if path.is_file()}
        self.assertEqual(files, {"Dockerfile", "sandbox_worker.py"})

    def test_dockerfile_does_not_copy_the_repository_tree(self):
        dockerfile = (container_eval.IMAGE_CONTEXT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("COPY sandbox_worker.py /opt/runner/sandbox_worker.py", dockerfile)
        self.assertNotIn("COPY .", dockerfile)
        self.assertNotIn("expected_values.json", dockerfile)
        self.assertNotIn("instrument.py", dockerfile)

    def test_trusted_worker_contains_no_probe_bank_or_answer_key(self):
        worker = (container_eval.IMAGE_CONTEXT / "sandbox_worker.py").read_text(encoding="utf-8")
        self.assertNotIn("expected_values.json", worker)
        self.assertNotIn("instrument.PROBES", worker)
        self.assertNotIn("FAMILY_ORDER", worker)

    def test_effective_limit_check_accepts_only_one_readonly_candidate_bind(self):
        result = {
            "container": {
                "user": "65534:65534",
                "network_mode": "none",
                "readonly_rootfs": True,
                "memory_bytes": container_eval.MEMORY_BYTES,
                "memory_swap_bytes": container_eval.MEMORY_BYTES,
                "nano_cpus": 1_000_000_000,
                "pids_limit": 16,
                "cap_drop": ["ALL"],
                "security_opt": ["no-new-privileges:true"],
                "mounts": [
                    {"type": "bind", "destination": "/candidate/solve.py", "read_only": True,
                     "source": "/tmp/fixture.py"},
                    {"type": "tmpfs", "destination": "/tmp", "read_only": False,
                     "source": None},
                ],
            }
        }
        checks = container_eval.effective_limits(result)
        self.assertTrue(all(checks.values()), checks)

    def test_writable_or_extra_bind_mount_fails_closed(self):
        result = {
            "container": {
                "user": "65534:65534",
                "network_mode": "none",
                "readonly_rootfs": True,
                "memory_bytes": container_eval.MEMORY_BYTES,
                "memory_swap_bytes": container_eval.MEMORY_BYTES,
                "nano_cpus": 1_000_000_000,
                "pids_limit": 16,
                "cap_drop": ["ALL"],
                "security_opt": ["no-new-privileges:true"],
                "mounts": [
                    {"type": "bind", "destination": "/candidate/solve.py", "read_only": False,
                     "source": "/tmp/fixture.py"},
                    {"type": "bind", "destination": "/repo", "read_only": True,
                     "source": "/workspace/repo"},
                ],
            }
        }
        checks = container_eval.effective_limits(result)
        self.assertFalse(checks["exactly_one_readonly_candidate_bind"])


if __name__ == "__main__":
    unittest.main()
