"""Tests for the strict guest adapter's return-type envelope. No provider calls."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline_expression_strict"))

import python_adapter


class StrictAdapterTests(unittest.TestCase):
    def test_exact_integer_is_accepted(self) -> None:
        self.assertEqual(
            python_adapter.encode_result(42),
            {"return_type": "int", "value": "42"},
        )
        self.assertEqual(
            python_adapter.encode_result(-6),
            {"return_type": "int", "value": "-6"},
        )

    def test_numeric_string_is_not_an_integer(self) -> None:
        self.assertEqual(
            python_adapter.encode_result("42"),
            {"return_type": "str", "value": "42"},
        )

    def test_booleans_are_not_integers(self) -> None:
        self.assertEqual(python_adapter.encode_result(True)["return_type"], "bool")
        self.assertEqual(python_adapter.encode_result(False)["return_type"], "bool")

    def test_float_and_none_are_not_integers(self) -> None:
        self.assertEqual(python_adapter.encode_result(42.0)["return_type"], "float")
        self.assertEqual(python_adapter.encode_result(None)["return_type"], "NoneType")

    def test_non_primitive_return_does_not_stringify_the_object(self) -> None:
        result = python_adapter.encode_result(object())
        self.assertEqual(result["return_type"], "object")
        self.assertNotIn("value", result)


if __name__ == "__main__":
    unittest.main()
