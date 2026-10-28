from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import generate


class FakeResponse:
    status = 200
    headers = {"Content-Type": "application/json"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps({
            "id": "offline-test-response",
            "model": generate.MODEL,
            "choices": [{"message": {"content": "TEST_ONLY"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }).encode("utf-8")


class GeneratorProtocolTests(unittest.TestCase):
    def test_prompt_variants_preserve_v3_three_batch_blocks(self):
        variants = [generate.prompt_variant_for_batch(i) for i in range(12)]
        self.assertEqual(
            variants,
            ["direct"] * 3 + ["menu"] * 3 + ["simple"] * 3 + ["direct"] * 3,
        )

    def test_negative_batch_id_is_rejected(self):
        with self.assertRaises(ValueError):
            generate.prompt_variant_for_batch(-1)

    def test_request_uses_fixed_endpoint_and_needs_no_api_key(self):
        with mock.patch.object(generate, "_wait_for_request_slot"), \
             mock.patch.object(generate.urllib.request, "urlopen", return_value=FakeResponse()) as urlopen:
            status, data, metadata = generate._request_completion("offline-only test prompt")
        self.assertEqual(status, 200)
        self.assertEqual(data["model"], generate.MODEL)
        self.assertEqual(metadata["returned_model"], generate.MODEL)
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, generate.ENDPOINT)
        self.assertIsNone(request.get_header("Authorization"))
        self.assertEqual(json.loads(request.data)["model"], generate.MODEL)
        self.assertEqual(json.loads(request.data)["messages"][0]["content"], "offline-only test prompt")

    def test_only_completed_response_records_count_as_completed_batches(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "attempts.jsonl"
            path.write_text(
                json.dumps({"batch_id": 0, "completed": False}) + "\n"
                + json.dumps({"batch_id": 1, "completed": True}) + "\n"
                + json.dumps({"batch_id": 2, "completed": False, "deferred": True}) + "\n",
                encoding="utf-8",
            )
            with mock.patch.object(generate, "ATTEMPTS", path):
                self.assertEqual(generate.completed_batch_ids(), {1})


if __name__ == "__main__":
    unittest.main()
