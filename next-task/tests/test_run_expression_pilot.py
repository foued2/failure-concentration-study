"""Offline tests for the expression pilot runner. No provider request is made."""
from __future__ import annotations

import base64
import copy
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline_expression_strict"))

import python_adapter
import run_expression_pilot as runner
from expression_mutants import VARIANTS


def raw_row(probe_id: str, value: str = "0", *, status: str = "complete",
            exit_code: int | None = 0, timed_out: bool = False) -> dict:
    return {
        "probe_id": probe_id,
        "status": status,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "tree_terminated": True,
        "stdout_b64": base64.b64encode(value.encode("utf-8")).decode("ascii"),
        "stderr_b64": base64.b64encode(b"").decode("ascii"),
        "elapsed_ms": 1,
    }


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class ExpressionPilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="expression-pilot-test-")
        self.temp_path = Path(self.temp.name)
        self.diagnostic, self.evaluation, _ = runner.load_frozen_banks()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def execute_with_source(self, source: str, mode: str = "normal"):
        namespace: dict = {}
        exec(compile(source, "<test-solver>", "exec"), namespace)
        solve = namespace["solve"]
        calls: list[str] = []

        def execute(temp, suite_name, case_id, entries, received_source, runtime):
            calls.append(suite_name)
            self.assertEqual(received_source, source)
            for entry in entries:
                self.assertEqual(set(entry), {"probe_id", "input"})
                self.assertEqual(set(entry["input"]), {"expr"})
            rows = []
            for entry in entries:
                expr = entry["input"]["expr"]
                if mode == "timeout":
                    rows.append(raw_row(entry["probe_id"], "", status="timeout",
                                        exit_code=None, timed_out=True))
                elif mode == "crash":
                    rows.append(raw_row(entry["probe_id"], "", status="crash", exit_code=1))
                elif mode == "malformed":
                    rows.append(raw_row(entry["probe_id"], "not-an-integer\n"))
                else:
                    try:
                        value = solve(expr)
                    except Exception:
                        rows.append(raw_row(entry["probe_id"], "", status="crash", exit_code=1))
                    else:
                        envelope = json.dumps(python_adapter.encode_result(value)) + "\n"
                        rows.append(raw_row(entry["probe_id"], envelope))
            return {"probe_rows": rows}, 0.001

        return execute, calls

    def generator(self, source: str):
        screen = runner.screen_source(source)
        bid = runner.body_id(source)

        def generate(attempt_dir: Path, number: int) -> dict:
            (attempt_dir / "generated-response.txt").write_text(source, encoding="utf-8")
            (attempt_dir / "generated-solver.py").write_text(source, encoding="utf-8")
            runner.save_json(attempt_dir / "source-screen.json", {
                "accepted": screen.accepted,
                "reasons": list(screen.reasons),
                "body_id": bid,
                "source_bytes": len(source.encode("utf-8")),
            })
            return {
                "status": "generated",
                "source": source,
                "screen": {
                    "accepted": screen.accepted,
                    "reasons": list(screen.reasons),
                    "body_id": bid,
                    "source_bytes": len(source.encode("utf-8")),
                },
                "elapsed_seconds": 0.0,
                "http_status": 200,
                "finish_reason": "STOP",
            }

        return generate

    def run_one(self, name: str, source: str, mode: str = "normal", cap: int = 1):
        run_dir = self.temp_path / name
        execute, calls = self.execute_with_source(source, mode)
        result = runner.run_pilot(
            run_dir,
            generate_fn=self.generator(source),
            execute_fn=execute,
            attempt_cap=cap,
            runtime=run_dir / "runtime",
        )
        return result, calls

    def assert_target(self, result: dict, target: str | None, correct: int) -> None:
        attempt = result["attempts"][0]
        diag = attempt["diagnostic"]
        ev = attempt["evaluation"]
        if target is None:
            self.assertEqual(diag["k"], 0)
            self.assertEqual(diag["C"], 0.0)
            self.assertEqual(diag["family_counts"], {family: 0 for family in runner.FAMILY_ORDER})
        else:
            self.assertEqual(diag["k"], 5)
            self.assertEqual(diag["C"], 1.0)
            self.assertEqual(diag["family_counts"][target], 5)
            self.assertEqual(
                sum(count for family, count in diag["family_counts"].items() if family != target), 0)
            self.assertEqual(ev["status_counts"].get("pass", 0), correct)
        self.assertEqual(ev["correct_count"], correct)
        self.assertTrue(attempt["eligible"])

    def test_prompt_matches_preregistration(self) -> None:
        self.assertEqual(runner.load_preregistered_prompt(), runner.PROMPT)

    def test_strict_adapter_matches_calibration_and_old_path_is_rejected(self) -> None:
        self.assertEqual(runner.validate_strict_adapter(), runner.STRICT_ADAPTER_SHA256)
        with mock.patch.object(runner, "EXPRESSION_PIPELINE", runner.ROOT / "pipeline_expression"):
            with self.assertRaises(RuntimeError):
                runner.validate_strict_adapter()

    def test_protocol_records_launch_identity(self) -> None:
        source = VARIANTS["reference_parser"]["source"]
        self.run_one("protocol", source)
        protocol = json.loads(
            (self.temp_path / "protocol" / "PROTOCOL.json").read_text(encoding="utf-8"))
        self.assertEqual(protocol["strict_adapter_sha256"], runner.STRICT_ADAPTER_SHA256)
        self.assertEqual(protocol["runner_sha256"], runner.sha256_file(Path(runner.__file__)))
        self.assertIsNone(protocol["repository_commit"])
        self.assertTrue(protocol["source_hashes"]["03C_PILOT_LAUNCH_PRECONDITIONS_2026-10-22.md"])

    def test_guest_payload_contains_no_oracles(self) -> None:
        for records, id_key in ((self.diagnostic, "probe_id"), (self.evaluation, "hid")):
            entries = runner.guest_entries(records, id_key)
            serialized = json.dumps(entries)
            self.assertEqual(len(entries), 30)
            self.assertNotIn("expected", serialized)
            self.assertNotIn("family", serialized)
            for entry in entries:
                self.assertEqual(set(entry), {"probe_id", "input"})
                self.assertEqual(set(entry["input"]), {"expr"})

    def test_source_screen_closes_obvious_dynamic_execution(self) -> None:
        probes = {
            "eval": "def solve(expr):\n    return eval(expr)\n",
            "exec": "def solve(expr):\n    exec('x = 1')\n    return 1\n",
            "compile": "def solve(expr):\n    return compile(expr, '<x>', 'eval')\n",
            "open": "def solve(expr):\n    return open('x').read()\n",
            "os": "import os\ndef solve(expr):\n    return 1\n",
        }
        for name, source in probes.items():
            result = runner.screen_source(source)
            self.assertFalse(result.accepted, name)
            self.assertTrue(result.reasons, name)
        literal = "import ast\ndef solve(expr):\n    return ast.literal_eval(expr)\n"
        self.assertTrue(runner.screen_source(literal).accepted)
        namespace: dict = {}
        exec(compile(literal, "<literal>", "exec"), namespace)
        with self.assertRaises(Exception):
            namespace["solve"]("2+3*4")

    def test_correct_and_six_mutants_reconstruct_host_results(self) -> None:
        expectations = {
            "reference_parser": (None, 30),
            "precedence_flat": ("F1", 25),
            "minus_right_assoc": ("F2", 25),
            "parens_dropped": ("F3", 25),
            "unary_rejected": ("F4", 25),
            "single_digit_tokenizer": ("F5", 25),
            "whitespace_rejected": ("F6", 25),
        }
        for name, (target, correct) in expectations.items():
            with self.subTest(variant=name):
                source = VARIANTS[name]["source"]
                result, _ = self.run_one(f"variant-{name}", source)
                self.assert_target(result, target, correct)
                if name == "reference_parser":
                    self.assertEqual(result["state"], "CEILING_NO_FAILURE_VARIATION")
                else:
                    self.assertEqual(result["state"], "INCORRECT_BODIES_BUT_NO_REPEATED_K")

    def test_malformed_output_is_invalid_and_not_passed(self) -> None:
        source = "def solve(expr):\n    return 42\n"
        result, _ = self.run_one("malformed", source, mode="malformed")
        attempt = result["attempts"][0]
        self.assertEqual(attempt["diagnostic"]["status_counts"], {"invalid": 30})
        self.assertEqual(attempt["evaluation"]["status_counts"], {"invalid": 30})
        self.assertEqual(attempt["diagnostic"]["k"], 30)
        self.assertEqual(attempt["evaluation"]["correct_count"], 0)
        self.assertTrue(attempt["eligible"])

    def test_strict_envelope_accepts_only_exact_int(self) -> None:
        accepted = '{"return_type":"int","value":"42"}\n'
        self.assertEqual(
            runner.parse_expression_return(raw_row("valid", accepted)),
            {"return_type": "int", "value": 42},
        )
        for kind, payload in (
            ("str", '{"return_type":"str","value":"42"}\n'),
            ("bool", '{"return_type":"bool","value":"true"}\n'),
            ("float", '{"return_type":"float","value":"42.0"}\n'),
            ("NoneType", '{"return_type":"NoneType","value":null}\n'),
        ):
            with self.subTest(kind=kind):
                with self.assertRaises(runner.WrongReturnType):
                    runner.parse_expression_return(raw_row(kind, payload))
        for payload in (
            "not-json\n",
            '{"return_type":"int","value":"4.2"}\n',
            '{"return_type":"int","value":"42","extra":1}\n',
            '{"return_type":"int","value":"42"}\nextra\n',
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(runner.CaptureRejected):
                    runner.parse_expression_return(raw_row("malformed", payload))

    def test_numeric_string_return_is_a_family_failure(self) -> None:
        source = 'def solve(expr):\n    return "42"\n'
        result, _ = self.run_one("numeric-string", source)
        attempt = result["attempts"][0]
        self.assertEqual(attempt["diagnostic"]["status_counts"], {"wrong_type": 30})
        self.assertEqual(attempt["evaluation"]["status_counts"], {"wrong_type": 30})
        self.assertEqual(attempt["diagnostic"]["k"], 30)
        self.assertEqual(attempt["evaluation"]["correct_count"], 0)
        self.assertTrue(attempt["eligible"])
        self.assertEqual(
            {row["return_type"] for row in attempt["diagnostic"]["probe_rows"]}, {"str"})

    def test_wrong_type_raises_its_family_count_by_one(self) -> None:
        entry = {"probe_id": "F1_single", "input": {"expr": "1+2"}}
        meta = {"probe_id": "F1_single", "family": "F1", "expr": "1+2", "expected": 3}
        row = runner.expression_outcome(
            raw_row("F1_single", '{"return_type":"str","value":"3"}\n'),
            entry, meta, "diagnostic")
        self.assertEqual(row["status"], "wrong_type")
        summary = runner.diagnostic_summary([row])
        self.assertEqual(summary["family_counts"]["F1"], 1)
        self.assertEqual(sum(summary["family_counts"].values()), 1)
        self.assertEqual(summary["k"], 1)
        self.assertEqual(summary["C"], 1.0)

    def test_boolean_float_and_none_returns_are_wrong_type(self) -> None:
        cases = {
            "true": ("def solve(expr):\n    return True\n", "bool"),
            "false": ("def solve(expr):\n    return False\n", "bool"),
            "float": ("def solve(expr):\n    return 42.0\n", "float"),
            "none": ("def solve(expr):\n    return None\n", "NoneType"),
        }
        for name, (source, expected_type) in cases.items():
            with self.subTest(kind=name):
                result, _ = self.run_one(f"wrong-type-{name}", source)
                attempt = result["attempts"][0]
                self.assertEqual(attempt["diagnostic"]["status_counts"], {"wrong_type": 30})
                self.assertEqual(attempt["evaluation"]["correct_count"], 0)
                self.assertTrue(attempt["eligible"])
                self.assertEqual(
                    {row["return_type"] for row in attempt["diagnostic"]["probe_rows"]},
                    {expected_type},
                )

    def test_timeout_body_is_ineligible(self) -> None:
        source = VARIANTS["reference_parser"]["source"]
        result, _ = self.run_one("timeout", source, mode="timeout")
        attempt = result["attempts"][0]
        self.assertEqual(attempt["execution_status"], "complete")
        self.assertFalse(attempt["eligible"])
        self.assertTrue(attempt["diagnostic"]["timed_out"])
        self.assertEqual(attempt["diagnostic"]["status_counts"], {"timeout": 30})
        self.assertEqual(result["state"], "NO_ELIGIBLE_BODIES")

    def test_crash_is_recorded_as_failure(self) -> None:
        source = VARIANTS["reference_parser"]["source"]
        result, _ = self.run_one("crash", source, mode="crash")
        attempt = result["attempts"][0]
        self.assertTrue(attempt["eligible"])
        self.assertEqual(attempt["diagnostic"]["status_counts"], {"crash": 30})
        self.assertEqual(attempt["diagnostic"]["k"], 30)
        self.assertEqual(attempt["evaluation"]["correct_count"], 0)
        self.assertEqual(result["state"], "INCORRECT_BODIES_BUT_NO_REPEATED_K")

    def test_auth_failure_halts_without_retry_or_replacement(self) -> None:
        run_dir = self.temp_path / "auth-halt"

        def generate(attempt_dir: Path, number: int) -> dict:
            return {"status": "generation_failed", "failure_kind": "auth",
                    "elapsed_seconds": 0.0, "http_status": None, "response_present": False}

        result = runner.run_pilot(
            run_dir, generate_fn=generate, execute_fn=lambda *args: ({}, 0.0),
            attempt_cap=3, runtime=run_dir / "runtime")
        self.assertEqual(result["attempt_count"], 1)
        self.assertEqual(result["generation_failures"], 1)
        self.assertEqual(result["state"], "HALTED_GENERATION_AUTH")
        self.assertEqual(runner.validate_attempts(result["attempts"]), [])

    def test_duplicate_is_retained_without_reexecution(self) -> None:
        source = VARIANTS["reference_parser"]["source"]
        result, calls = self.run_one("duplicate", source, cap=2)
        self.assertEqual(len(result["attempts"]), 2)
        self.assertEqual(result["attempts"][1]["execution_status"], "duplicate_skipped")
        self.assertEqual(result["attempts"][1]["duplicate_of"], result["attempts"][0]["attempt_id"])
        self.assertEqual(result["duplicates"], 1)
        self.assertEqual(len([name for name in calls if name.startswith("diagnostic_")]), 1)
        self.assertEqual(runner.validate_attempts(result["attempts"]), [])

    def test_attempt_record_validation_rejects_corruption(self) -> None:
        source = VARIANTS["reference_parser"]["source"]
        result, _ = self.run_one("validation", source)
        self.assertEqual(runner.validate_attempts(result["attempts"]), [])
        missing_eval = copy.deepcopy(result["attempts"])
        missing_eval[0]["evaluation"] = None
        self.assertTrue(runner.validate_attempts(missing_eval))
        bad_timeout = copy.deepcopy(result["attempts"])
        bad_timeout[0]["eligible"] = True
        bad_timeout[0]["diagnostic"]["timed_out"] = True
        self.assertTrue(runner.validate_attempts(bad_timeout))
        duplicate_execution = copy.deepcopy(result["attempts"])
        clone = copy.deepcopy(duplicate_execution[0])
        clone["attempt_id"] = "attempt-0002"
        clone["generation_order"] = 2
        duplicate_execution.append(clone)
        self.assertTrue(runner.validate_attempts(duplicate_execution))

    def test_fixed_k_decision_requires_cross_c_evaluation_separation(self) -> None:
        def body(suffix: str, k: int, c: float, correct: int) -> dict:
            return {
                "body_id": suffix * 64,
                "execution_status": "complete",
                "eligible": True,
                "diagnostic": {"k": k, "C": c},
                "evaluation": {"correct_count": correct},
            }

        qualifying = [
            body("a", 4, 1.0, 30), body("b", 4, 1.0, 30),
            body("c", 4, 0.5, 25), body("d", 4, 0.5, 25),
        ]
        summary = runner.summarize(qualifying)
        self.assertTrue(summary["feasibility_demonstrated"])
        self.assertEqual(summary["missing_conditions"], [])
        nonqualifying = copy.deepcopy(qualifying)
        for row in nonqualifying:
            row["evaluation"]["correct_count"] = 30
        self.assertFalse(runner.summarize(nonqualifying)["feasibility_demonstrated"])

    def test_request_one_retains_source_without_logging_secret(self) -> None:
        attempt = self.temp_path / "request"
        attempt.mkdir()
        source = VARIANTS["reference_parser"]["source"]
        payload = {
            "candidates": [{"content": {"parts": [{"text": source}]}, "finishReason": "STOP"}],
            "usageMetadata": {"promptTokenCount": 1, "candidatesTokenCount": 2},
        }
        with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "test-secret-key"}):
            with mock.patch("run_expression_pilot.urllib.request.urlopen",
                            return_value=FakeResponse(payload)):
                result = runner.request_one(attempt, 1)
        self.assertEqual(result["status"], "generated")
        self.assertTrue(result["screen"]["accepted"])
        self.assertEqual((attempt / "generated-response.txt").read_text(encoding="utf-8"), source)
        self.assertTrue((attempt / "generated-solver.py").is_file())
        for path in attempt.iterdir():
            if path.is_file():
                self.assertNotIn("test-secret-key", path.read_text(encoding="utf-8", errors="replace"))

    def test_request_one_classifies_usage_limit_and_missing_key(self) -> None:
        attempt = self.temp_path / "request-errors"
        attempt.mkdir()
        with mock.patch.dict(os.environ, {}, clear=True):
            missing = runner.request_one(attempt, 1)
        self.assertEqual(missing["failure_kind"], "auth")
        error = urllib.error.HTTPError(
            "https://example.invalid", 429, "Too Many Requests", None, io.BytesIO(b"quota"))
        with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "test-secret-key"}):
            with mock.patch("run_expression_pilot.urllib.request.urlopen", side_effect=error):
                limited = runner.request_one(attempt, 2)
        error.close()
        self.assertEqual(limited["failure_kind"], "usage_limit")


if __name__ == "__main__":
    unittest.main()
