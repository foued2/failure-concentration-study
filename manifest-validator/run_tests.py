#!/usr/bin/env python3
"""Run the validator against the synthetic fixture corpus.

Checks, in order:
 1. every fixture produces exactly the declared distinct error codes and the
    declared validity / M1-si status;
 2. declared warnings, alias reasons, exclusion reasons and counts are present;
 3. two independent CLI runs produce byte-identical reports (determinism);
 4. the JSON Schema agrees with an independent draft 2020-12 implementation
    (skipped, and reported as SKIP, only if ``jsonschema`` is not installed).

The expectations in ``fixtures/expected_results.json`` were written by hand and
are not derived from validator output.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
sys.path.insert(0, str(HERE))

import validate_manifest as vm  # noqa: E402

FAILURES = []


def check(condition, label, detail=""):
    if condition:
        print(f"  PASS  {label}")
    else:
        FAILURES.append(f"{label}: {detail}")
        print(f"  FAIL  {label}  {detail}")


def documented_codes(items):
    return sorted({item["code"] for item in items})


def main():
    spec = importlib.util.spec_from_file_location("validate_manifest_cli", HERE / "validate_manifest.py")
    assert spec and spec.loader
    fixture_expectations = json.loads((FIXTURES / "expected_results.json").read_text("utf-8"))
    schema_path = HERE / "manifest_schema.json"

    print("== expectations ==")
    for expected in fixture_expectations["expectations"]:
        name = expected["fixture"]
        manifest_path = FIXTURES / name
        limits_path = FIXTURES / expected["limits"]
        report = vm.run(manifest_path, limits_path, schema_path)
        label = name

        check(
            report["decision"]["valid"] == expected["valid"],
            f"{label} valid",
            f"expected {expected['valid']}, got {report['decision']['valid']}",
        )
        check(
            report["decision"]["m1_si"] == expected["m1_si"],
            f"{label} m1_si",
            f"expected {expected['m1_si']}, got {report['decision']['m1_si']}",
        )
        check(
            documented_codes(report["errors"]) == expected["error_codes"],
            f"{label} error codes",
            f"expected {expected['error_codes']}, got {documented_codes(report['errors'])}",
        )
        check(
            set(expected.get("warning_codes", [])) <= set(documented_codes(report["warnings"])),
            f"{label} warning codes",
            f"expected {expected.get('warning_codes', [])}, got {documented_codes(report['warnings'])}",
        )
        alias_reasons = sorted({a["reason"] for a in report["aliases"]})
        check(
            set(expected.get("alias_reasons", [])) <= set(alias_reasons),
            f"{label} alias reasons",
            f"expected {expected.get('alias_reasons', [])}, got {alias_reasons}",
        )
        excluded_reasons = sorted({e["reason"] for e in report["excluded"]})
        check(
            set(expected.get("excluded_reasons", [])) <= set(excluded_reasons),
            f"{label} exclusion reasons",
            f"expected {expected.get('excluded_reasons', [])}, got {excluded_reasons}",
        )
        if "variants_realized" in expected:
            check(
                report["counts"].get("variants_realized") == expected["variants_realized"],
                f"{label} variants_realized",
                f"expected {expected['variants_realized']}, got {report['counts'].get('variants_realized')}",
            )
        if "max_qualifying_parents" in expected:
            check(
                report["counts"].get("max_qualifying_parents_in_one_cell")
                == expected["max_qualifying_parents"],
                f"{label} max qualifying parents",
                f"expected {expected['max_qualifying_parents']}, "
                f"got {report['counts'].get('max_qualifying_parents_in_one_cell')}",
            )

    print("== determinism ==")
    outputs = []
    for _ in range(2):
        result = subprocess.run(
            [
                sys.executable,
                str(HERE / "validate_manifest.py"),
                "--manifest",
                str(FIXTURES / "valid_realized.json"),
                "--limits",
                str(FIXTURES / "limits_standard.json"),
                "--schema",
                str(schema_path),
            ],
            capture_output=True,
            check=False,
        )
        outputs.append(result.stdout)
        check(result.returncode == 0, "cli exit code 0 on valid manifest", f"got {result.returncode}")
    check(outputs[0] == outputs[1], "byte-identical repeated reports")
    check(len(outputs[0]) > 0, "non-empty report")

    print("== schema cross-check ==")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        print("  SKIP  jsonschema not installed; independent draft 2020-12 agreement not checked")
    else:
        schema = json.loads(schema_path.read_text("utf-8"))
        validator_class = jsonschema.Draft202012Validator
        for expected in fixture_expectations["expectations"]:
            if expected["valid"] is not True:
                continue
            instance = json.loads((FIXTURES / expected["fixture"]).read_text("utf-8"))
            errors = sorted(validator_class(schema).iter_errors(instance), key=lambda e: list(e.path))
            check(
                not errors,
                f"schema accepts {expected['fixture']}",
                "; ".join(e.message for e in errors[:3]),
            )

    print()
    if FAILURES:
        print(f"FAILED {len(FAILURES)} check(s)")
        for failure in FAILURES:
            print(f"  - {failure}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
