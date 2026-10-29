from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import generation_plan_draft as draft


def fenced(body: str) -> str:
    return "```python\n" + body.strip() + "\n```\n"


class GenerationPlanDraftTests(unittest.TestCase):
    def test_plan_preserves_frozen_v3_round_robin_and_prompt_variants(self):
        cases = {
            0: ("deepseek", "direct", "opencode/deepseek-v4.1-flash-free"),
            1: ("glm", "direct", "opencode/glm-5.3-flash-free"),
            2: ("mimo", "direct", "opencode/mimo-v2.6-flash-free"),
            3: ("deepseek", "menu", "opencode/deepseek-v4.1-flash-free"),
            6: ("deepseek", "simple", "opencode/deepseek-v4.1-flash-free"),
            399: ("deepseek", "menu", "opencode/deepseek-v4.1-flash-free"),
        }
        for batch_id, (route_id, variant, alias) in cases.items():
            with self.subTest(batch_id=batch_id):
                plan = draft.plan_batch(batch_id)
                self.assertEqual(plan["route_id"], route_id)
                self.assertEqual(plan["prompt_variant"], variant)
                self.assertEqual(plan["original_route_alias"], alias)
                self.assertEqual(plan["requested_bodies"], 8)
                self.assertEqual(plan["provenance_group"], f"batch-{batch_id:03d}")
                self.assertFalse(plan["network_request_performed"])
                self.assertFalse(plan["generation_permitted"])
                self.assertIsNone(plan["temperature"])
                self.assertIsNone(plan["max_output_tokens"])

    def test_invalid_batch_ids_are_rejected(self):
        for value in (-1, 400, True, 1.0, "1"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    draft.plan_batch(value)

    def test_generator_source_hash_matches_pinned_frozen_manifest(self):
        import json
        freeze = json.loads(draft.V3_FREEZE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(freeze["tag"], draft.V3_FROZEN_TAG)
        self.assertEqual(draft._git_blob_sha1(draft.V3_FREEZE_PATH), draft.V3_FROZEN_MANIFEST_GIT_BLOB_SHA1)
        self.assertEqual(draft.V3_GENERATOR_SOURCE_SHA256, draft.V3_FROZEN_GENERATOR_SHA256)
        self.assertEqual(freeze["artifact_hashes_sha256"]["generate.py"], draft.V3_GENERATOR_SOURCE_SHA256)
        self.assertEqual(draft.plan_batch(0)["v3_generator_source_sha256"], draft.V3_FROZEN_GENERATOR_SHA256)

    def test_generator_hash_normalizes_windows_crlf(self):
        import hashlib
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "generate.py"
            lf_bytes = b"def solve(): return 0\\n"
            source.write_bytes(b"def solve(): return 0\\r\\n")
            expected = hashlib.sha256(lf_bytes).hexdigest()
            self.assertEqual(draft._verify_v3_generator_source(source, expected), expected)

    def test_modified_generator_source_is_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "generate.py"
            source.write_bytes(b"def solve(): return 1\\n")
            with self.assertRaisesRegex(ValueError, "pinned frozen SHA-256"):
                draft._verify_v3_generator_source(source)

    def test_modified_freeze_manifest_is_rejected(self):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            freeze = Path(td) / "FREEZE.json"
            freeze.write_text(json.dumps({
                "tag": draft.V3_FROZEN_TAG,
                "status": draft.V3_FROZEN_STATUS,
                "artifact_hashes_sha256": {"generate.py": draft.V3_FROZEN_GENERATOR_SHA256},
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "pinned frozen manifest blob"):
                draft._verify_v3_freeze_manifest(freeze)

    def test_prompt_bytes_match_frozen_v3_prompt_construction(self):
        v3 = draft._V3
        for batch_id in (0, 1, 2, 3, 17, 399):
            plan = draft.plan_batch(batch_id)
            self.assertEqual(plan["prompt"], v3.PROMPTS[plan["prompt_variant"]].format(n=8))
            self.assertEqual(plan["prompt_sha256"], draft._sha256_text(plan["prompt"]))

    def test_extraction_preserves_leading_imports_and_rejects_non_code(self):
        source = "import heapq\n\ndef solve(n, edges, s, t):\n    return -1\n"
        response = fenced(source) + "\n```python\nprint('not a solver')\n```\n"
        bodies = draft.extract_candidates(response)
        self.assertEqual(len(bodies), 1)
        self.assertTrue(bodies[0].startswith("import heapq\n"))
        self.assertIn("def solve", bodies[0])

    def test_underproduction_is_recorded_without_retries_or_best_of(self):
        body1 = "def solve(n, edges, s, t):\n    return -1\n"
        body2 = "def solve(n, edges, s, t):\n    return 0\n"
        record = draft.record_response_metadata(0, fenced(body1) + fenced(body2))
        self.assertEqual(record["extracted_bodies"], 2)
        self.assertEqual(record["batch_outcome"], "UNDERPRODUCED")
        self.assertEqual(record["provenance_group"], "batch-000")
        self.assertEqual(len(record["body_hashes_in_response_order"]), 2)
        self.assertNotEqual(record["body_hashes_in_response_order"][0], record["body_hashes_in_response_order"][1])
        self.assertFalse(record["provider_call_performed_by_helper"])
        self.assertIsNone(record["retries_observed_by_helper"])
        self.assertFalse(record["best_of_selection_performed_by_helper"])
        self.assertFalse(record["generation_permitted"])

    def test_complete_and_overproduced_responses_are_not_truncated(self):
        body = "def solve(n, edges, s, t):\n    return 0\n"
        complete = draft.record_response_metadata(1, "\n".join(fenced(body.replace("return 0", f"return {i}")) for i in range(8)))
        over = draft.record_response_metadata(1, "\n".join(fenced(body.replace("return 0", f"return {i}")) for i in range(9)))
        self.assertEqual(complete["batch_outcome"], "COMPLETE")
        self.assertEqual(complete["extracted_bodies"], 8)
        self.assertEqual(over["batch_outcome"], "OVERPRODUCED")
        self.assertEqual(over["extracted_bodies"], 9)
        self.assertEqual(len(over["candidate_records"]), 9)

    def test_generation_gate_is_closed_even_if_plan_helper_is_used(self):
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            draft.assert_generation_disabled()


if __name__ == "__main__":
    unittest.main()
