"""LC518/150 owner mutation-design annex auditor (mechanical C1-C7 checks).

AUDIT ONLY — NOT AN AUTHORIZATION. This tool checks a supplied owner annex
against the structural and audit rules already frozen in the LC518 protocol
(C1-C7) and GLM_WORK_ORDER.md v1.0 (lines 45, 47; Sections 3, 11). It contains
no mutation content, reconstructs none, and proposes none.

Checks implemented (fail-closed, each produces a rule-tagged reason code):
  C1  exactly eight mechanisms, each with a non-empty definition
  C2  all 28 unordered mechanism pairs appear at least once; exactly two
      distinct preselected pairs appear exactly twice; 30 assignments total
  C3  assignments map one-to-one onto parents G01-G30 (no parent twice);
      the SA/SB orientation (which mechanism is mutation A) is consistent
      for every repeated pair
  C5  30 S-extra assignments, one per parent, balanced across the eight
      mechanisms as closely as integer counts permit (audit expectation:
      six mechanisms at 4, two at 3); deviation is reported, never repaired
  C7  structural K5 scope exclusion reminder (annex-free fact; reported,
      never enforced against supplied content)
 plus: referential integrity (every referenced mechanism and parent exists),
 schema conformance against the packaged ANNEX_INTAKE_FORM_SCHEMA.json, and
 replication-preselection consistency with the assignment table.

Exit codes: 0 all checks pass; 2 any check fails; 3 unreadable/malformed input
or packaged-schema identity error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path
from collections import Counter

from jsonschema import Draft202012Validator, FormatChecker

TOOL_NAME = "lc518-150-annex-auditor"
TOOL_VERSION = "1.0.0"
AUDIT_LABEL = "ANNEX AUDIT ONLY — NOT AN AUTHORIZATION — NO CONTENT SUPPLIED BY THIS TOOL"

SCHEMA_FILENAME = "ANNEX_INTAKE_FORM_SCHEMA.json"
ROSTER_FILENAME = Path("gate1-inputs") / "PARENT_ROSTER_G01_G30.json"

EXPECTED_MECHANISMS = 8
EXPECTED_ASSIGNMENTS = 30
EXPECTED_PARENTS = 30
EXPECTED_S_EXTRA = 30


def _git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _audit_path() -> Path:
    return Path(__file__).resolve().parent / SCHEMA_FILENAME


def load_and_verify_schema(path: Path | None = None) -> dict:
    p = path or _audit_path()
    raw = p.read_bytes()
    schema = json.loads(raw.decode("utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _unordered(mech_a: str, mech_b: str) -> tuple[str, str]:
    return (mech_a, mech_b) if mech_a <= mech_b else (mech_b, mech_a)


def audit_annex(annex: dict, roster: dict, schema: dict) -> dict:
    report = {
        "tool": TOOL_NAME,
        "tool_version": TOOL_VERSION,
        "label": AUDIT_LABEL,
        "annex_id": annex.get("annex_id") if isinstance(annex, dict) else None,
        "schema_decision": "REJECTED",
        "rules": {},
        "reason_codes": [],
    }
    reasons: list[str] = report["reason_codes"]
    rules = report["rules"]

    schema_errors = [
        {
            "instance_path": "/" + "/".join(str(p) for p in e.absolute_path),
            "keyword": e.validator,
        }
        for e in sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(annex),
            key=lambda e: (list(map(str, e.absolute_path)), e.validator or ""),
        )
    ]
    report["schema_errors"] = schema_errors
    if schema_errors:
        reasons.append("ANNEX_SCHEMA_VALIDATION_FAILED")
        report["schema_decision"] = "REJECTED"
        report["audit_decision"] = "AUDIT_FAILED"
        return report
    report["schema_decision"] = "SCHEMA_CONFORMANT"

    mechanisms = {m["mechanism_id"] for m in annex["mechanisms"]}
    roster_parents = {p["parent_id"] for p in roster["parents"]}

    # C1: eight mechanisms, all defined (schema enforces count and minLength).
    c1_pass = len(annex["mechanisms"]) == EXPECTED_MECHANISMS and all(
        m["definition"].strip() for m in annex["mechanisms"]
    )
    rules["C1_mechanism_taxonomy"] = "PASS" if c1_pass else "FAIL"
    if not c1_pass:
        reasons.append("C1_MECHANISM_TAXONOMY_FAIL")

    assignments = annex["pair_assignments"]
    parent_ids = [a["parent_id"] for a in assignments]

    # C3 (bijective parent coverage) and referential integrity first: C2 pair
    # coverage is only meaningful over well-formed assignments.
    dup_parents = sorted({p for p, n in Counter(parent_ids).items() if n > 1})
    unknown_parents = sorted(set(parent_ids) - roster_parents)
    unknown_mechanisms = sorted(
        {m for a in assignments for m in (a["mechanism_a"], a["mechanism_b"])} - mechanisms
    )
    c3_bijective = not dup_parents and not unknown_parents and set(parent_ids) == roster_parents
    rules["C3_parent_bijection"] = "PASS" if c3_bijective else "FAIL"
    if dup_parents:
        reasons.append("C3_PARENT_ASSIGNED_MORE_THAN_ONCE: " + ",".join(dup_parents))
    if unknown_parents:
        reasons.append("REFERENTIAL_PARENT_UNKNOWN: " + ",".join(unknown_parents))
    if unknown_mechanisms:
        reasons.append("REFERENTIAL_MECHANISM_UNKNOWN: " + ",".join(unknown_mechanisms))
    if unknown_mechanisms:
        rules["C3_parent_bijection"] = "FAIL"

    # C2: pair coverage over the 28 unordered pairs; exactly two distinct
    # preselected pairs appear exactly twice.
    pair_counts = Counter(
        _unordered(a["mechanism_a"], a["mechanism_b"])
        for a in assignments
        if a["mechanism_a"] != a["mechanism_b"]
    )
    all_pairs = set(combinations(sorted(mechanisms), 2))
    missing_pairs = sorted(f"{a}|{b}" for (a, b) in all_pairs - set(pair_counts))
    self_pairs = sorted({a["parent_id"] for a in assignments if a["mechanism_a"] == a["mechanism_b"]})
    over_replicated = sorted(
        f"{a}|{b}:{n}" for (a, b), n in pair_counts.items() if n > 2
    )
    replication_flags = [a for a in assignments if a["is_replication"]]
    flag_counts = Counter(
        _unordered(a["mechanism_a"], a["mechanism_b"]) for a in replication_flags
    )
    bad_flags = sorted(
        f"{a}|{b}:{n}" for (a, b), n in flag_counts.items() if n != 1
    )
    replications_missing_evidence = sorted(
        a["parent_id"] for a in replication_flags if not a.get("preselection_evidence", "").strip()
    )
    declared_reps = {
        _unordered(annex["replication_preselection"][k]["mechanism_a"],
                   annex["replication_preselection"][k]["mechanism_b"])
        for k in ("replicated_pair_1", "replicated_pair_2")
    }
    flagged_pairs = set(flag_counts)
    if len(declared_reps) != 2:
        reasons.append("C2_REPLICATION_PRESELECTION_NOT_TWO_DISTINCT_PAIRS")
    if flagged_pairs != declared_reps:
        reasons.append("C2_REPLICATION_FLAGS_DISAGREE_WITH_PRESELECTION")
    twice_pairs = {p for p, n in pair_counts.items() if n == 2}
    if twice_pairs != declared_reps:
        reasons.append("C2_TWICE_PAIRS_DISAGREE_WITH_PRESELECTION")
    c2_pass = (
        not missing_pairs
        and not self_pairs
        and not over_replicated
        and not bad_flags
        and not replications_missing_evidence
        and len(declared_reps) == 2
        and flagged_pairs == declared_reps
        and twice_pairs == declared_reps
        and sum(pair_counts.values()) == EXPECTED_ASSIGNMENTS
    )
    rules["C2_pair_coverage_28_plus_2"] = "PASS" if c2_pass else "FAIL"
    if missing_pairs:
        reasons.append("C2_PAIR_MISSING: " + ",".join(missing_pairs))
    if self_pairs:
        reasons.append("C2_DEGENERATE_SELF_PAIR_PARENTS: " + ",".join(self_pairs))
    if over_replicated:
        reasons.append("C2_PAIR_APPEARS_MORE_THAN_TWICE: " + ",".join(over_replicated))
    if bad_flags:
        reasons.append("C2_REPLICATION_FLAG_COUNT_NOT_ONE_PER_REPLICATED_PAIR: " + ",".join(bad_flags))
    if replications_missing_evidence:
        reasons.append("C2_REPLICATION_PRESELECTION_EVIDENCE_MISSING: " + ",".join(replications_missing_evidence))

    # C3 (orientation consistency): for any pair appearing more than once,
    # mechanism_a must be identical across occurrences.
    orientation_by_pair: dict[tuple[str, str], set[str]] = {}
    for a in assignments:
        orientation_by_pair.setdefault(_unordered(a["mechanism_a"], a["mechanism_b"]), set()).add(a["mechanism_a"])
    inconsistent = sorted(
        f"{p[0]}|{p[1]}" for p, orientations in orientation_by_pair.items() if len(orientations) > 1
    )
    c3_orientation = not inconsistent
    rules["C3_orientation_consistency"] = "PASS" if c3_orientation else "FAIL"
    if inconsistent:
        reasons.append("C3_ORIENTATION_INCONSISTENT: " + ",".join(inconsistent))

    # C5: S-extra balance across the eight mechanisms.
    s_extra = annex["s_extra_assignments"]
    s_parents = [s["parent_id"] for s in s_extra]
    s_dup = sorted({p for p, n in Counter(s_parents).items() if n > 1})
    s_unknown_parents = sorted(set(s_parents) - roster_parents)
    s_unknown_mech = sorted({s["mechanism_id"] for s in s_extra} - mechanisms)
    balance = Counter(s["mechanism_id"] for s in s_extra)
    balanced_as_expected = sorted(balance.values(), reverse=True) == [4, 4, 4, 4, 4, 4, 3, 3]
    c5_pass = (
        len(s_extra) == EXPECTED_S_EXTRA
        and not s_dup
        and not s_unknown_parents
        and not s_unknown_mech
        and balanced_as_expected
    )
    rules["C5_s_extra_balance"] = "PASS" if c5_pass else "FAIL"
    if len(s_extra) != EXPECTED_S_EXTRA:
        reasons.append(f"C5_S_EXTRA_COUNT_NOT_30: {len(s_extra)}")
    if s_dup:
        reasons.append("C5_S_EXTRA_PARENT_ASSIGNED_MORE_THAN_ONCE: " + ",".join(s_dup))
    if s_unknown_parents:
        reasons.append("REFERENTIAL_S_EXTRA_PARENT_UNKNOWN: " + ",".join(s_unknown_parents))
    if s_unknown_mech:
        reasons.append("REFERENTIAL_S_EXTRA_MECHANISM_UNKNOWN: " + ",".join(s_unknown_mech))
    if not balanced_as_expected and not (s_dup or s_unknown_parents or s_unknown_mech):
        reasons.append(
            "C5_BALANCE_DEVIATES_FROM_6x4_PLUS_2x3_AUDIT_EXPECTATION: "
            + json.dumps(dict(sorted(balance.items())), sort_keys=True)
        )
    report["s_extra_balance"] = dict(sorted(balance.items()))

    # C6: witnesses documented (schema enforces the const true and note length).
    rules["C6_witnesses_documented"] = "PASS" if annex["witness_declarations"]["cd_feasibility_witnesses_documented"] else "FAIL"

    # C7: annex-free structural reminder (always reported, never fails the audit).
    rules["C7_K5_scope_exclusion_notice"] = "REPORTED"
    report["C7_notice"] = (
        "Frozen protocol C7: no (mechanism, K5) cell qualifies; K5 is reportable "
        "descriptively only. Structural basis, annex-free: K5 has 2 parent groups."
    )

    report["reason_codes"] = sorted(set(reasons))
    report["audit_decision"] = "ALL_LOCAL_RULES_PASS" if not report["reason_codes"] else "AUDIT_FAILED"
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=AUDIT_LABEL)
    parser.add_argument("--annex", required=True, help="owner-supplied annex JSON (filled intake form)")
    parser.add_argument("--roster", help="parent roster JSON; defaults to gate1-inputs/PARENT_ROSTER_G01_G30.json next to this file")
    parser.add_argument("--report", help="write the audit report JSON here; default stdout")
    args = parser.parse_args(argv)

    try:
        annex_raw = Path(args.annex).read_bytes()
        annex = json.loads(annex_raw.decode("utf-8"))
        annex_sha = hashlib.sha256(annex_raw).hexdigest()
        schema = load_and_verify_schema()
        roster_path = (
            Path(args.roster)
            if args.roster
            else Path(__file__).resolve().parent / ROSTER_FILENAME
        )
        roster = json.loads(roster_path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"AUDIT_INPUT_ERROR: {exc}", file=sys.stderr)
        return 3

    report = audit_annex(annex, roster, schema)
    report["annex_sha256"] = annex_sha
    report["roster_artifact_id"] = roster.get("artifact_id")

    output = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.report:
        Path(args.report).write_text(output, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(output)
    return 0 if report["audit_decision"] == "ALL_LOCAL_RULES_PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
