"""LC518/150 owner mutation-design annex structural-intake auditor.

AUDIT ONLY — NOT AN AUTHORIZATION. Implements mechanical C1-C7 intake
checks from A2 Rev 11. C4 counts distinct effective parent groups in all
40 (mechanism, family) cells, using immutable parent IDs and pinned
base-source hashes. Only the single-mutation roles SA, SB and S-extra
contribute; S0 and SAB are excluded. The actual ADOPTED family-map bytes
must match the hash recorded in the parent-identity manifest and must
partition the roster exactly. C5 is compliance reporting, not an
independent A2 gate. C6 checks witness-note presence only; it does NOT
assess vector validity, mechanism reach, joint attainability, C_D
feasibility, or the aggregate A2 verdict.

Exit codes: 0 structural intake pass (C6 adequacy remains unassessed);
2 failed, blocked, or not-assessable input; 3 unreadable/malformed input or
packaged-schema identity error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path, PurePosixPath
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
EXPECTED_SCHEMA_GIT_BLOB_SHA1 = "1cc7bd81701c7cdb1c6f43c7058f59943c8ca25b"
MECHANISM_IDS = [f"M{i}" for i in range(1, 9)]


def _git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _audit_path() -> Path:
    return Path(__file__).resolve().parent / SCHEMA_FILENAME


def load_and_verify_schema(path: Path | None = None) -> dict:
    p = path or _audit_path()
    raw = p.read_bytes()
    actual = _git_blob_sha1(raw)
    if actual != EXPECTED_SCHEMA_GIT_BLOB_SHA1:
        raise ValueError(
            "ANNEX_SCHEMA_IDENTITY_MISMATCH: "
            f"expected Git blob SHA-1 {EXPECTED_SCHEMA_GIT_BLOB_SHA1}, got {actual}"
        )
    schema = json.loads(raw.decode("utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _unordered(mech_a: str, mech_b: str) -> tuple[str, str]:
    return (mech_a, mech_b) if mech_a <= mech_b else (mech_b, mech_a)


def _verified_parent_source_sha256(source_root: Path, relative_path: str) -> str:
    """Hash an actual parent source file without importing or executing it.

    Paths are POSIX-style, relative to the supplied source root, and may not
    traverse outside it or pass through symlinks.
    """
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ValueError("PARENT_SOURCE_PATH_MISSING")
    if "\\" in relative_path:
        raise ValueError("PARENT_SOURCE_PATH_MUST_USE_POSIX_SEPARATORS")
    rel = PurePosixPath(relative_path)
    if rel.is_absolute() or not rel.parts or any(part in (".", "..") for part in rel.parts):
        raise ValueError("PARENT_SOURCE_PATH_NOT_SAFE_RELATIVE_PATH")

    root = source_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("PARENT_SOURCE_ROOT_NOT_DIRECTORY")
    candidate = root
    for part in rel.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError("PARENT_SOURCE_PATH_CONTAINS_SYMLINK")
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise ValueError("PARENT_SOURCE_PATH_ESCAPES_ROOT")
    if not resolved.is_file():
        raise ValueError("PARENT_SOURCE_PATH_NOT_FILE")
    return hashlib.sha256(resolved.read_bytes()).hexdigest()


def audit_c4_incidence(
    annex: dict,
    roster: dict,
    parent_identities: dict | None,
    family_map: dict | None,
    family_map_sha256: str | None,
    parent_source_root: Path | None = None,
) -> dict:
    """Compute effective n(m,z) for all 40 cells, deduplicating base hashes."""
    result = {
        "status": "NOT_ASSESSABLE",
        "reason_codes": [],
        "n_m_z": [],
        "qualifying_cells": [],
        "scope_rule": "qualifies_structurally_iff_n_effective_parent_groups_gte_3",
    }
    if parent_identities is None:
        result["reason_codes"] = ["C4_PARENT_IDENTITY_MANIFEST_MISSING"]
        return result
    if not isinstance(parent_identities, dict) or not isinstance(parent_identities.get("parents"), list):
        result["reason_codes"] = ["C4_PARENT_IDENTITY_MANIFEST_MALFORMED"]
        return result
    if parent_source_root is None:
        result["reason_codes"] = ["C4_PARENT_SOURCE_ROOT_NOT_SUPPLIED"]
        return result
    if not isinstance(family_map, dict) or not isinstance(family_map_sha256, str):
        result["reason_codes"] = ["C4_FAMILY_MAP_FILE_MISSING"]
        return result

    adoption = parent_identities.get("family_map_adoption_ref")
    if (
        family_map.get("status") != "ADOPTED"
        or not isinstance(adoption, dict)
        or adoption.get("status") != "ADOPTED"
        or not isinstance(adoption.get("artifact_id"), str)
        or not adoption.get("artifact_id").strip()
        or adoption.get("artifact_id") != family_map.get("artifact_id")
        or not isinstance(adoption.get("sha256"), str)
        or len(adoption.get("sha256")) != 64
        or any(ch not in "0123456789abcdef" for ch in adoption.get("sha256"))
    ):
        result["reason_codes"] = ["C4_FAMILY_MAP_ADOPTION_NOT_ESTABLISHED"]
        return result
    if adoption["sha256"] != family_map_sha256:
        result["status"] = "BLOCKED_UNRESOLVED"
        result["reason_codes"] = ["C4_FAMILY_MAP_HASH_MISMATCH"]
        return result

    expected = {p["parent_id"]: p["Z_id"] for p in roster.get("parents", [])}
    if len(expected) != 30:
        result["reason_codes"] = ["C4_ROSTER_NOT_EXACTLY_30_PARENTS"]
        return result

    mapped = {}
    family_rows = family_map.get("families")
    if not isinstance(family_rows, dict):
        result["reason_codes"] = ["C4_FAMILY_MAP_FAMILIES_MISSING"]
        return result
    for zid, family in family_rows.items():
        members = family.get("parents") if isinstance(family, dict) else None
        if not isinstance(members, list):
            result["reason_codes"] = [f"C4_FAMILY_MAP_PARENT_LIST_INVALID:{zid}"]
            return result
        for pid in members:
            if not isinstance(pid, str) or pid in mapped:
                result["status"] = "BLOCKED_UNRESOLVED"
                result["reason_codes"] = ["C4_FAMILY_MAP_PARENT_COLLISION_OR_INVALID_ID"]
                return result
            mapped[pid] = zid
    if mapped != expected:
        result["status"] = "BLOCKED_UNRESOLVED"
        result["reason_codes"] = ["C4_ADOPTED_FAMILY_MAP_ROSTER_MISMATCH"]
        return result

    by_parent = {}
    hash_families = {}
    malformed, blocked = [], []
    verified_source_hashes: dict[str, str] = {}
    source_missing: list[str] = []
    for index, row in enumerate(parent_identities["parents"]):
        if not isinstance(row, dict):
            malformed.append(f"ROW_{index}_NOT_OBJECT")
            continue
        pid, digest, zid = row.get("parent_id"), row.get("base_source_sha256"), row.get("Z_id")
        if not isinstance(pid, str) or pid not in expected:
            malformed.append(f"ROW_{index}_UNKNOWN_PARENT")
            continue
        if (
            not isinstance(digest, str) or len(digest) != 64
            or any(ch not in "0123456789abcdef" for ch in digest)
        ):
            malformed.append(f"{pid}_BASE_SOURCE_SHA256_INVALID")
            continue
        if zid not in expected.values():
            malformed.append(f"{pid}_UNKNOWN_FAMILY")
            continue
        try:
            actual_digest = _verified_parent_source_sha256(
                parent_source_root, row.get("base_source_path")
            )
        except FileNotFoundError:
            source_missing.append(f"C4_PARENT_SOURCE_FILE_MISSING:{pid}")
            continue
        except (OSError, ValueError) as exc:
            malformed.append(f"C4_PARENT_SOURCE_PATH_INVALID:{pid}:{exc}")
            continue
        if actual_digest != digest:
            blocked.append(f"C4_PARENT_SOURCE_HASH_MISMATCH:{pid}")
            continue
        verified_source_hashes[pid] = actual_digest
        current = (digest, zid)
        if pid in by_parent:
            if by_parent[pid] != current:
                blocked.append(f"PARENT_ID_MULTIPLE_IDENTITIES:{pid}")
            else:
                malformed.append(f"DUPLICATE_PARENT_IDENTITY_ROW:{pid}")
            continue
        if zid != expected[pid]:
            blocked.append(f"PARENT_FAMILY_CONFLICT:{pid}")
        by_parent[pid] = current
        hash_families.setdefault(digest, set()).add(zid)

    for digest, families in hash_families.items():
        if len(families) > 1:
            blocked.append("BASE_SOURCE_HASH_CROSSES_FAMILIES:" + digest)
    missing = sorted(set(expected) - set(by_parent))
    if missing:
        malformed.append("C4_PARENT_IDENTITY_COVERAGE_INCOMPLETE:" + ",".join(missing))
    if source_missing:
        result["reason_codes"] = sorted(set(malformed + blocked + source_missing))
        result["status"] = "BLOCKED_UNRESOLVED" if blocked else "NOT_ASSESSABLE"
        return result
    if malformed:
        result["reason_codes"] = sorted(set(malformed + blocked))
        result["status"] = "BLOCKED_UNRESOLVED" if blocked else "NOT_ASSESSABLE"
        return result
    if blocked:
        result["status"] = "BLOCKED_UNRESOLVED"
        result["reason_codes"] = sorted(set(blocked))
        return result

    # Distinct parent groups are base-source hashes within a single family.
    # Duplicate IDs with the same hash/family cannot inflate independent n(m,z).
    hash_to_family = {h: next(iter(families)) for h, families in hash_families.items()}
    hash_to_mechanisms = {h: set() for h in hash_to_family}
    pair_by_parent = {
        row["parent_id"]: (row["mechanism_a"], row["mechanism_b"])
        for row in annex["pair_assignments"]
    }
    extra_by_parent = {
        row["parent_id"]: row["mechanism_id"] for row in annex["s_extra_assignments"]
    }
    for pid, (digest, _zid) in by_parent.items():
        hash_to_mechanisms[digest].update(pair_by_parent[pid])
        hash_to_mechanisms[digest].add(extra_by_parent[pid])

    families = sorted(set(expected.values()))
    counts = {(m, z): 0 for m in MECHANISM_IDS for z in families}
    for digest, mechanisms in hash_to_mechanisms.items():
        zid = hash_to_family[digest]
        for mechanism in mechanisms:
            if mechanism in MECHANISM_IDS:
                counts[(mechanism, zid)] += 1

    rows, qualifying = [], []
    for mechanism in MECHANISM_IDS:
        for zid in families:
            n = counts[(mechanism, zid)]
            rows.append({
                "mechanism_id": mechanism,
                "Z_id": zid,
                "n_effective_parent_groups": n,
                "qualifies_structurally": n >= 3,
            })
            if n >= 3:
                qualifying.append({"mechanism_id": mechanism, "Z_id": zid})
    result.update({
        "status": "ASSESSED",
        "reason_codes": [],
        "n_m_z": rows,
        "qualifying_cells": qualifying,
        "effective_parent_group_count": len(hash_to_family),
        "family_map_adoption_ref": adoption,
        "family_map_sha256_verified": True,
        "family_map_roster_partition_verified": True,
        "parent_source_bytes_verified": True,
        "verified_parent_source_count": len(verified_source_hashes),
    })
    return result


def audit_annex(
    annex: dict,
    roster: dict,
    schema: dict,
    parent_identities: dict | None = None,
    parent_identity_manifest_sha256: str | None = None,
    family_map: dict | None = None,
    family_map_sha256: str | None = None,
    parent_source_root: Path | None = None,
) -> dict:
    report = {
        "tool": TOOL_NAME,
        "tool_version": TOOL_VERSION,
        "label": AUDIT_LABEL,
        "annex_id": annex.get("annex_id") if isinstance(annex, dict) else None,
        "schema_decision": "REJECTED",
        "rules": {},
        "reason_codes": [],
        "C4": {"status": "NOT_ASSESSABLE", "reason_codes": [], "n_m_z": [], "qualifying_cells": []},
        "C6_scope": "PRESENCE_ONLY_NOT_ADEQUACY",
        "parent_identity_manifest_sha256": parent_identity_manifest_sha256,
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

    # C4 depends on a valid C3 one-to-one parent assignment and consistent
    # SA/SB orientation. Do not let malformed C3 input reach incidence indexing.
    if c3_bijective and c3_orientation:
        c4 = audit_c4_incidence(
            annex, roster, parent_identities, family_map, family_map_sha256,
            parent_source_root,
        )
    else:
        c4 = {
            "status": "NOT_ASSESSABLE",
            "reason_codes": ["C4_C3_ALLOCATION_PREREQUISITE_NOT_MET"],
            "n_m_z": [],
            "qualifying_cells": [],
        }
    report["C4"] = c4
    rules["C4_incidence_by_family"] = c4["status"]
    if c4["status"] != "ASSESSED":
        reasons.extend(c4.get("reason_codes", []))

    # C5: S-extra balance is a work-order compliance record, not an A2 gate.
    s_extra = annex["s_extra_assignments"]
    s_parents = [s["parent_id"] for s in s_extra]
    s_dup = sorted({p for p, n in Counter(s_parents).items() if n > 1})
    s_unknown_parents = sorted(set(s_parents) - roster_parents)
    s_unknown_mech = sorted({s["mechanism_id"] for s in s_extra} - mechanisms)
    balance = Counter(s["mechanism_id"] for s in s_extra)
    balanced_as_expected = sorted(balance.values(), reverse=True) == [4, 4, 4, 4, 4, 4, 3, 3]
    c5_compliant = (
        len(s_extra) == EXPECTED_S_EXTRA
        and not s_dup
        and not s_unknown_parents
        and not s_unknown_mech
        and balanced_as_expected
    )
    c5_reasons = []
    if len(s_extra) != EXPECTED_S_EXTRA:
        c5_reasons.append(f"C5_S_EXTRA_COUNT_NOT_30: {len(s_extra)}")
    if s_dup:
        c5_reasons.append("C5_S_EXTRA_PARENT_ASSIGNED_MORE_THAN_ONCE: " + ",".join(s_dup))
    if s_unknown_parents:
        c5_reasons.append("REFERENTIAL_S_EXTRA_PARENT_UNKNOWN: " + ",".join(s_unknown_parents))
    if s_unknown_mech:
        c5_reasons.append("REFERENTIAL_S_EXTRA_MECHANISM_UNKNOWN: " + ",".join(s_unknown_mech))
    if not balanced_as_expected and not (s_dup or s_unknown_parents or s_unknown_mech):
        c5_reasons.append(
            "C5_BALANCE_DEVIATES_FROM_6x4_PLUS_2x3_AUDIT_EXPECTATION: "
            + json.dumps(dict(sorted(balance.items())), sort_keys=True)
        )
    rules["C5_s_extra_balance"] = "COMPLIANT" if c5_compliant else "DEVIATION_RECORDED"
    report["C5_compliance"] = {
        "status": rules["C5_s_extra_balance"],
        "is_independent_A2_gate": False,
        "reason_codes": c5_reasons,
    }
    report["s_extra_balance"] = dict(sorted(balance.items()))

    # C6: witness-note presence only. The declaration boolean is not proof.
    witness_notes = annex["witness_declarations"].get("witness_notes", "")
    if isinstance(witness_notes, str) and witness_notes.strip():
        rules["C6_witness_notes_presence"] = "PRESENT_ADEQUACY_NOT_ASSESSED"
    else:
        rules["C6_witness_notes_presence"] = "MISSING"
        reasons.append("C6_WITNESS_NOTES_MISSING")
    report["C6_scope"] = (
        "PRESENCE ONLY. Witness-vector validity, mechanism reach, joint "
        "attainability, structural absence and C_D feasibility were not assessed."
    )

    # C7: annex-free structural reminder (always reported, never fails the audit).
    rules["C7_K5_scope_exclusion_notice"] = "REPORTED"
    report["C7_notice"] = (
        "Frozen protocol C7: no (mechanism, K5) cell qualifies; K5 is reportable "
        "descriptively only. Structural basis, annex-free: K5 has 2 parent groups."
    )

    report["reason_codes"] = sorted(set(reasons))
    core_fail = (
        rules.get("C1_mechanism_taxonomy") == "FAIL"
        or rules.get("C2_pair_coverage_28_plus_2") == "FAIL"
        or rules.get("C3_parent_bijection") == "FAIL"
        or rules.get("C3_orientation_consistency") == "FAIL"
        or rules.get("C6_witness_notes_presence") == "MISSING"
    )
    if core_fail or report["schema_errors"]:
        report["audit_decision"] = "AUDIT_FAILED"
    elif c4["status"] == "BLOCKED_UNRESOLVED":
        report["audit_decision"] = "AUDIT_BLOCKED_UNRESOLVED"
    elif c4["status"] != "ASSESSED":
        report["audit_decision"] = "AUDIT_NOT_ASSESSABLE"
    else:
        report["audit_decision"] = "STRUCTURAL_INTAKE_PASS_C6_ADEQUACY_NOT_ASSESSED"
    report["boundary"] = (
        "Structural intake only. C4 verifies each declared base-source SHA-256 against "
        "the actual source-file bytes under the supplied source root, and verifies the "
        "adopted family-map bytes. C5 is compliance reporting only. C6 note presence was "
        "checked, not adequacy or semantic attainability."
    )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=AUDIT_LABEL)
    parser.add_argument("--annex", required=True, help="owner-supplied annex JSON (filled intake form)")
    parser.add_argument("--roster", help="parent roster JSON; defaults to gate1-inputs/PARENT_ROSTER_G01_G30.json next to this file")
    parser.add_argument("--parent-identities", help="separate parent-ID/base-source-SHA256/Z_id manifest and family-map adoption reference")
    parser.add_argument("--family-map", help="actual family-map JSON; C4 verifies ADOPTED status and file SHA-256")
    parser.add_argument(
        "--parent-source-root",
        help="root containing the exact base-source files named by base_source_path in the identity manifest; files are hashed, never executed",
    )
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
        parent_identities = None
        parent_identity_sha256 = None
        if args.parent_identities:
            identity_raw = Path(args.parent_identities).read_bytes()
            parent_identities = json.loads(identity_raw.decode("utf-8"))
            parent_identity_sha256 = hashlib.sha256(identity_raw).hexdigest()
        family_map_path = (
            Path(args.family_map) if args.family_map
            else Path(__file__).resolve().parent / "gate1-inputs" / "FAMILY_MAP.json"
        )
        family_map_raw = family_map_path.read_bytes()
        family_map = json.loads(family_map_raw.decode("utf-8"))
        family_map_sha256 = hashlib.sha256(family_map_raw).hexdigest()
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"AUDIT_INPUT_ERROR: {exc}", file=sys.stderr)
        return 3

    report = audit_annex(
        annex, roster, schema, parent_identities, parent_identity_sha256,
        family_map, family_map_sha256,
        Path(args.parent_source_root) if args.parent_source_root else None,
    )
    report["annex_sha256"] = annex_sha
    report["roster_artifact_id"] = roster.get("artifact_id")

    output = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.report:
        Path(args.report).write_text(output, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(output)
    return 0 if report["audit_decision"] == "STRUCTURAL_INTAKE_PASS_C6_ADEQUACY_NOT_ASSESSED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
