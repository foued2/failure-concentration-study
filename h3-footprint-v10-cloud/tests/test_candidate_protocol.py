from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from candidate_child import _parse_worker_response


class WorkerProtocolTests(unittest.TestCase):
    def test_accepts_only_answer_value(self):
        self.assertEqual(_parse_worker_response(b'{"answer_type":"int","answer":17}\n', "probe"), ("int", 17))

    def test_rejects_forged_h3pred_metadata(self):
        forged = {"v": 1, "phase": "probe", "probe_id": "secret-probe-id", "status": "ok", "answer_type": "int", "answer": 424242}
        self.assertIsNone(_parse_worker_response(("H3PRED " + json.dumps(forged) + "\n").encode(), "probe"))

    def test_rejects_additional_metadata_even_without_h3pred_prefix(self):
        payload = {"answer_type": "int", "answer": 17, "status": "ok", "probe_id": "p"}
        self.assertIsNone(_parse_worker_response((json.dumps(payload) + "\n").encode(), "probe"))

    def test_rejects_duplicate_answer_records_and_duplicate_keys(self):
        self.assertIsNone(_parse_worker_response(b'{"answer_type":"int","answer":1}\n{"answer_type":"int","answer":2}\n', "probe"))
        self.assertIsNone(_parse_worker_response(b'{"answer_type":"int","answer":1,"answer":2}\n', "probe"))

    def test_preflight_accepts_callable_only(self):
        self.assertEqual(_parse_worker_response(b'{"answer_type":"callable","answer":null}\n', "preflight"), ("callable", None))
        self.assertIsNone(_parse_worker_response(b'{"answer_type":"int","answer":1}\n', "preflight"))


if __name__ == "__main__":
    unittest.main()
