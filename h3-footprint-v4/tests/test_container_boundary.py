from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import container_eval
import run_gate


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


class EvaluationCacheTests(unittest.TestCase):
    def test_matching_fingerprint_reuses_a_source_bound_row(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / ("a" * 64 + ".py")
            source.write_text("def solve(n, edges, s, t):\n    return 0\n", encoding="utf-8")
            cache_path = root / "results" / "evaluated_rows.jsonl"
            row = {
                "body_hash": source.stem,
                "excluded": None,
                "k": 0,
                "C": 0.0,
                "group_id": "batch-000",
                "generator": "fixture",
            }
            run_gate.append_evaluation_cache(cache_path, "fingerprint-a", source, row)
            loaded = run_gate.load_evaluation_cache(cache_path, "fingerprint-a")
            self.assertIn(source.stem, loaded)
            self.assertEqual(loaded[source.stem]["row"], row)
            self.assertEqual(
                loaded[source.stem]["source_sha256"],
                hashlib.sha256(source.read_bytes()).hexdigest(),
            )

    def test_stale_fingerprint_and_torn_lines_are_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / ("b" * 64 + ".py")
            source.write_text("def solve(n, edges, s, t):\n    return 0\n", encoding="utf-8")
            cache_path = root / "evaluated_rows.jsonl"
            row = {"body_hash": source.stem, "excluded": "fixture", "k": None}
            run_gate.append_evaluation_cache(cache_path, "old-fingerprint", source, row)
            with cache_path.open("a", encoding="utf-8") as handle:
                handle.write('{"truncated":')
            self.assertEqual(run_gate.load_evaluation_cache(cache_path, "new-fingerprint"), {})

    def test_source_change_is_detectable_even_when_body_filename_is_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / ("c" * 64 + ".py")
            source.write_text("def solve(n, edges, s, t):\n    return 0\n", encoding="utf-8")
            cache_path = root / "evaluated_rows.jsonl"
            run_gate.append_evaluation_cache(
                cache_path, "same-fingerprint", source,
                {"body_hash": source.stem, "excluded": None, "k": 0},
            )
            first = run_gate.load_evaluation_cache(cache_path, "same-fingerprint")[source.stem]
            source.write_text("def solve(n, edges, s, t):\n    return -1\n", encoding="utf-8")
            actual = hashlib.sha256(source.read_bytes()).hexdigest()
            self.assertNotEqual(first["source_sha256"], actual)


if __name__ == "__main__":
    unittest.main()
