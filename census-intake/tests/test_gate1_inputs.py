"""Regression tests for the Gate 1 input-preparation machinery.

Covers roster/family-map integrity, C1-C7 intake boundaries, C4 parent identity
deduplication and adoption binding, C5's compliance-only status, C6 note-
presence versus adequacy, schema hash pinning, real-inventory intake, q-registry
crosswalks, and the synthetic end-to-end manifest demo. All IDs, hashes and
timestamps are invented; no real allocation content is included.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from itertools import combinations
from pathlib import Path

CENSUS_INTAKE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CENSUS_INTAKE))

import build_preregistration_manifest as builder  # noqa: E402
import validate_annex  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402


def _load(path: Path):
    return json.loads(path.read_bytes().decode("utf-8"))


ROSTER = _load(CENSUS_INTAKE / "gate1-inputs" / "PARENT_ROSTER_G01_G30.json")
FAMILY_MAP = _load(CENSUS_INTAKE / "gate1-inputs" / "FAMILY_MAP.json")
ANNEX_SCHEMA = validate_annex.load_and_verify_schema()
def synthetic_adopted_family_map():
    family_map = json.loads(json.dumps(FAMILY_MAP))
    family_map["status"] = "ADOPTED"
    raw = (json.dumps(family_map, indent=2, sort_keys=True, ensure_ascii=False) + chr(10)).encode("utf-8")
    return family_map, hashlib.sha256(raw).hexdigest()


def synthetic_parent_identities(family_map, family_map_sha256):
    parents = [
        {
            "parent_id": p["parent_id"],
            "base_source_path": f"{p['parent_id']}.py",
            "base_source_sha256": f"{i + 1:064x}",
            "Z_id": p["Z_id"],
        }
        for i, p in enumerate(ROSTER["parents"])
    ]
    bundle_rows = [
        {
            "parent_id": p["parent_id"],
            "base_source_path": p["base_source_path"],
            "base_source_sha256": p["base_source_sha256"],
        }
        for p in parents
    ]
    bundle_raw = json.dumps(
        bundle_rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return {
        "artifact_id": "SYNTHETIC-PARENT-IDENTITIES",
        "version": "0.0-synthetic",
        "family_map_adoption_ref": {
            "status": "ADOPTED",
            "artifact_id": family_map["artifact_id"],
            "sha256": family_map_sha256,
        },
        "source_hash_attestation": {
            "algorithm": "SHA-256",
            "hash_subject": "EXACT_BASE_SOURCE_FILE_BYTES",
            "method": "READ_BYTES_AND_HASH_ONLY_NO_IMPORT_OR_EXECUTION",
            "computed_by": "SYNTHETIC TEST FIXTURE ONLY",
            "computed_at_utc": "2026-11-23T00:00:00Z",
            "source_index_sha256": "a" * 64,
            "source_bundle_sha256": hashlib.sha256(bundle_raw).hexdigest(),
            "tool": "lc518-parent-source-hasher",
            "tool_version": "1.0.0",
            "execution_boundary": (
                "File bytes were read and hashed. No source file was imported, "
                "executed, parsed, compiled or modified."
            ),
        },
        "parents": parents,
    }

def synthetic_valid_annex() -> dict:
    mechs = [{"mechanism_id": f"M{i}", "name": f"SYNTHETIC mechanism {i}",
              "definition": f"SYNTHETIC definition {i} (invented for tests only)"}
             for i in range(1, 9)]
    parents = [p["parent_id"] for p in ROSTER["parents"]]
    pairs = list(combinations([f"M{i}" for i in range(1, 9)], 2))[:28]
    assignments = [
        {"parent_id": parents[i], "mechanism_a": pairs[i][0], "mechanism_b": pairs[i][1],
         "is_replication": False}
        for i in range(28)
    ] + [
        {"parent_id": parents[28], "mechanism_a": pairs[0][0], "mechanism_b": pairs[0][1],
         "is_replication": True, "preselection_evidence": "invented synthetic preselection note"},
        {"parent_id": parents[29], "mechanism_a": pairs[1][0], "mechanism_b": pairs[1][1],
         "is_replication": True, "preselection_evidence": "invented synthetic preselection note"},
    ]
    s_extra_mechs = [f"M{(i % 8) + 1}" for i in range(30)]
    return {
        "annex_id": "SYNTHETIC-ANNEX-001",
        "submitted_by": "SYNTHETIC",
        "submitted_at_utc": "2026-11-23T00:00:00Z",
        "provenance_statement": "SYNTHETIC provenance statement (invented).",
        "mechanisms": mechs,
        "pair_assignments": assignments,
        "replication_preselection": {
            "replicated_pair_1": {"mechanism_a": pairs[0][0], "mechanism_b": pairs[0][1]},
            "replicated_pair_2": {"mechanism_a": pairs[1][0], "mechanism_b": pairs[1][1]},
            "declared_before_construction": True,
        },
        "s_extra_assignments": [
            {"parent_id": parents[i], "mechanism_id": s_extra_mechs[i]} for i in range(30)
        ],
        "witness_declarations": {
            "cd_feasibility_witnesses_documented": True,
            "witness_notes": "SYNTHETIC witness notes (invented).",
        },
    }


class TestRosterAndFamilyMap(unittest.TestCase):
    def test_roster_has_30_unique_parents(self):
        ids = [p["parent_id"] for p in ROSTER["parents"]]
        self.assertEqual(len(ids), 30)
        self.assertEqual(len(set(ids)), 30)
        self.assertEqual(ids, [f"G{i:02d}" for i in range(1, 31)])

    def test_family_counts_match_frozen_design(self):
        counts = {"K1": 7, "K2": 8, "K3": 8, "K4": 5, "K5": 2}
        observed: dict[str, int] = {}
        for p in ROSTER["parents"]:
            observed[p["Z_id"]] = observed.get(p["Z_id"], 0) + 1
        self.assertEqual(observed, counts)
        self.assertEqual(ROSTER["family_counts"], counts)
        self.assertEqual(ROSTER["population_total"]["bodies"], 150)

    def test_family_map_partitions_match_roster(self):
        for zid, fam in FAMILY_MAP["families"].items():
            roster_members = sorted(p["parent_id"] for p in ROSTER["parents"] if p["Z_id"] == zid)
            self.assertEqual(sorted(fam["parents"]), roster_members)


class TestAnnexAuditor(unittest.TestCase):
    def setUp(self):
        self.valid = synthetic_valid_annex()
        family_map, family_map_sha256 = synthetic_adopted_family_map()
        report = validate_annex.audit_annex(
            self.valid,
            ROSTER,
            ANNEX_SCHEMA,
            synthetic_parent_identities(family_map, family_map_sha256),
            family_map_sha256,
            family_map,
            family_map_sha256,
        )
        self.assertEqual(
            report["audit_decision"],
            "STRUCTURAL_INTAKE_PASS_C6_ADEQUACY_NOT_ASSESSED",
            report["reason_codes"],
        )

    def audit(self, annex):
        family_map, family_map_sha256 = synthetic_adopted_family_map()
        return validate_annex.audit_annex(
            annex,
            ROSTER,
            ANNEX_SCHEMA,
            synthetic_parent_identities(family_map, family_map_sha256),
            family_map_sha256,
            family_map,
            family_map_sha256,
        )

    def test_missing_mechanism_fails_schema(self):
        annex = synthetic_valid_annex()
        annex["mechanisms"] = annex["mechanisms"][:7]
        report = self.audit(annex)
        self.assertIn("ANNEX_SCHEMA_VALIDATION_FAILED", report["reason_codes"])
        self.assertEqual(report["audit_decision"], "AUDIT_FAILED")
        self.assertEqual(report["schema_decision"], "REJECTED")

    def test_undefined_mechanism_fails_c1(self):
        annex = synthetic_valid_annex()
        annex["mechanisms"][3]["definition"] = "   "
        # minLength 1 still holds for whitespace; C1 requires non-blank content.
        schema_ok = Draft202012Validator(ANNEX_SCHEMA).is_valid(annex)
        self.assertTrue(schema_ok)
        report = self.audit(annex)
        self.assertIn("C1_MECHANISM_TAXONOMY_FAIL", report["reason_codes"])

    def test_missing_pair_fails_c2(self):
        annex = synthetic_valid_annex()
        annex["pair_assignments"][4] = dict(annex["pair_assignments"][0],
                                            parent_id="G05")
        report = self.audit(annex)
        self.assertTrue(
            any(c.startswith("C2_PAIR_MISSING") for c in report["reason_codes"]),
            report["reason_codes"],
        )

    def test_parent_assigned_twice_fails_c3(self):
        annex = synthetic_valid_annex()
        annex["pair_assignments"][4] = dict(annex["pair_assignments"][0])
        report = self.audit(annex)
        self.assertIn("C3_PARENT_ASSIGNED_MORE_THAN_ONCE: G01", report["reason_codes"])

    def test_orientation_inconsistency_fails_c3(self):
        annex = synthetic_valid_annex()
        rep = annex["pair_assignments"][28]
        rep["mechanism_a"], rep["mechanism_b"] = rep["mechanism_b"], rep["mechanism_a"]
        report = self.audit(annex)
        self.assertTrue(
            any(c.startswith("C3_ORIENTATION_INCONSISTENT") for c in report["reason_codes"]),
            report["reason_codes"],
        )

    def test_replication_without_preselection_evidence_fails_c2(self):
        annex = synthetic_valid_annex()
        annex["pair_assignments"][28].pop("preselection_evidence", None)
        report = self.audit(annex)
        self.assertIn(
            "C2_REPLICATION_PRESELECTION_EVIDENCE_MISSING: G29",
            report["reason_codes"],
        )

    def test_s_extra_imbalance_is_recorded_not_an_a2_gate(self):
        annex = synthetic_valid_annex()
        first = annex["s_extra_assignments"][0]
        target = annex["s_extra_assignments"][7]
        target["mechanism_id"] = first["mechanism_id"]
        report = self.audit(annex)
        self.assertEqual(
            report["audit_decision"],
            "STRUCTURAL_INTAKE_PASS_C6_ADEQUACY_NOT_ASSESSED",
            report["reason_codes"],
        )
        self.assertEqual(report["C5_compliance"]["status"], "DEVIATION_RECORDED")
        self.assertFalse(report["C5_compliance"]["is_independent_A2_gate"])

    def test_c4_reports_all_40_mechanism_family_cells(self):
        report = self.audit(synthetic_valid_annex())
        self.assertEqual(report["C4"]["status"], "ASSESSED")
        self.assertEqual(len(report["C4"]["n_m_z"]), 40)

    def test_c4_duplicate_base_hash_same_family_counts_once(self):
        family_map, family_map_sha256 = synthetic_adopted_family_map()
        identities = synthetic_parent_identities(family_map, family_map_sha256)
        identities["parents"][1]["base_source_sha256"] = identities["parents"][0]["base_source_sha256"]
        identities["parents"][1]["base_source_path"] = identities["parents"][0]["base_source_path"]
        report = validate_annex.audit_annex(
            synthetic_valid_annex(), ROSTER, ANNEX_SCHEMA, identities,
            family_map_sha256, family_map, family_map_sha256,
        )
        self.assertEqual(report["C4"]["status"], "ASSESSED")
        cell = next(
            row for row in report["C4"]["n_m_z"]
            if row["mechanism_id"] == "M1" and row["Z_id"] == "K1"
        )
        self.assertEqual(cell["n_effective_parent_groups"], 6)

    def test_c4_parent_source_manifest_is_consumed_without_opening_source(self):
        family_map, digest = synthetic_adopted_family_map()
        identities = synthetic_parent_identities(family_map, digest)
        identities["parents"][0]["base_source_path"] = "source-file-not-mounted.py"
        report = validate_annex.audit_annex(
            synthetic_valid_annex(), ROSTER, ANNEX_SCHEMA,
            identities, digest, family_map, digest,
        )
        self.assertEqual(report["C4"]["status"], "ASSESSED")
        self.assertEqual(report["C4"]["parent_source_hash_attestation_present"], True)
        self.assertEqual(report["C4"]["auditor_source_access"], "NONE_STATIC_MANIFEST_ONLY")

    def test_c4_missing_source_hash_attestation_is_not_assessable(self):
        family_map, digest = synthetic_adopted_family_map()
        identities = synthetic_parent_identities(family_map, digest)
        identities.pop("source_hash_attestation")
        report = validate_annex.audit_annex(
            synthetic_valid_annex(), ROSTER, ANNEX_SCHEMA,
            identities, digest, family_map, digest,
        )
        self.assertEqual(report["C4"]["status"], "NOT_ASSESSABLE")
        self.assertIn(
            "C4_PARENT_SOURCE_HASH_ATTESTATION_MISSING_OR_INVALID",
            report["C4"]["reason_codes"],
        )

    def test_c4_duplicate_hash_across_families_is_blocked(self):
        family_map, family_map_sha256 = synthetic_adopted_family_map()
        identities = synthetic_parent_identities(family_map, family_map_sha256)
        identities["parents"][7]["base_source_sha256"] = identities["parents"][0]["base_source_sha256"]
        identities["parents"][7]["base_source_path"] = identities["parents"][0]["base_source_path"]
        report = validate_annex.audit_annex(
            synthetic_valid_annex(), ROSTER, ANNEX_SCHEMA, identities,
            family_map_sha256, family_map, family_map_sha256,
        )
        self.assertEqual(report["C4"]["status"], "BLOCKED_UNRESOLVED")
        self.assertEqual(report["audit_decision"], "AUDIT_BLOCKED_UNRESOLVED")

    def test_c4_missing_identity_manifest_is_not_assessable(self):
        family_map, family_map_sha256 = synthetic_adopted_family_map()
        report = validate_annex.audit_annex(
            synthetic_valid_annex(), ROSTER, ANNEX_SCHEMA, None,
            None, family_map, family_map_sha256
        )
        self.assertEqual(report["C4"]["status"], "NOT_ASSESSABLE")
        self.assertEqual(report["audit_decision"], "AUDIT_NOT_ASSESSABLE")

    def test_c4_pending_family_map_is_not_assessable(self):
        family_map = json.loads(json.dumps(FAMILY_MAP))
        raw = (json.dumps(family_map, indent=2, sort_keys=True, ensure_ascii=False) + chr(10)).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        identities = synthetic_parent_identities(family_map, digest)
        report = validate_annex.audit_annex(
            synthetic_valid_annex(), ROSTER, ANNEX_SCHEMA,
            identities, digest, family_map, digest,
        )
        self.assertEqual(report["C4"]["status"], "NOT_ASSESSABLE")
        self.assertIn("C4_FAMILY_MAP_ADOPTION_NOT_ESTABLISHED", report["C4"]["reason_codes"])

    def test_c4_family_map_hash_mismatch_is_blocked(self):
        family_map, digest = synthetic_adopted_family_map()
        identities = synthetic_parent_identities(family_map, digest)
        wrong_digest = "b" * 64
        identities["family_map_adoption_ref"]["sha256"] = wrong_digest
        report = validate_annex.audit_annex(
            synthetic_valid_annex(), ROSTER, ANNEX_SCHEMA,
            identities, wrong_digest, family_map, digest,
        )
        self.assertEqual(report["C4"]["status"], "BLOCKED_UNRESOLVED")
        self.assertIn("C4_FAMILY_MAP_HASH_MISMATCH", report["C4"]["reason_codes"])

    def test_c6_notes_presence_is_not_adequacy(self):
        report = self.audit(synthetic_valid_annex())
        self.assertEqual(
            report["rules"]["C6_witness_notes_presence"],
            "PRESENT_ADEQUACY_NOT_ASSESSED",
        )
        self.assertIn("presence only", report["C6_scope"].lower())

    def test_missing_c6_notes_fails_schema(self):
        annex = synthetic_valid_annex()
        annex["witness_declarations"].pop("witness_notes")
        report = self.audit(annex)
        self.assertIn("ANNEX_SCHEMA_VALIDATION_FAILED", report["reason_codes"])

    def test_schema_pin_rejects_other_valid_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            other = Path(tmp) / "valid_but_unpinned.json"
            other.write_text(json.dumps({"type": "object"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ANNEX_SCHEMA_IDENTITY_MISMATCH"):
                validate_annex.load_and_verify_schema(other)

    def test_c7_reported_not_enforced(self):
        report = self.audit(synthetic_valid_annex())
        self.assertEqual(report["rules"]["C7_K5_scope_exclusion_notice"], "REPORTED")


class TestPreregistrationBuilderDemo(unittest.TestCase):
    def test_demo_manifest_passes_intake_checker(self):
        import validate_records

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "demo"
            argv = ["--demo-synthetic", "--out-dir", str(out)]
            rc = builder.main(argv)
            self.assertEqual(rc, 0)

            report = _load(out / "build_report.json")
            self.assertTrue(report["label"].startswith("SYNTHETIC DEMO"))
            self.assertEqual(report["variant_count"], 150)
            self.assertGreater(report["q_registry_entry_count"], 0)
            self.assertEqual(report["q_registry_variant_crosswalk_count"], 150)
            q_registry = _load(out / "q_registry.json")
            self.assertEqual(
                sum(len(entry["variant_ids"]) for entry in q_registry["q_entries"]),
                150,
            )
            self.assertTrue(report["all_rows_not_started"])
            self.assertIsNone(report["first_diagnostic_execution_started_at_utc"])

            manifest_raw = (out / "preregistration_manifest.json").read_bytes()
            manifest = json.loads(manifest_raw.decode("utf-8"))
            schema = validate_records.load_and_verify_schema()
            sha = validate_records.hashlib.sha256(manifest_raw).hexdigest()
            result = validate_records.validate_manifest(manifest, sha, schema)
            self.assertEqual(
                result["manifest_decision"],
                "LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED",
                result["manifest_reason_codes"],
            )
            self.assertTrue(result["manifest_schema_valid"])
            self.assertEqual(len(result["variants"]), 150)
            self.assertTrue(
                all(v["validity_status"] == "EXPECTED_NOT_RUN" for v in manifest["variants"])
            )
            self.assertTrue(
                all(v["measurement"]["state"] == "NO_DIAGNOSTIC_MEASUREMENT"
                    for v in result["variants"])
            )
            self.assertIsNone(
                manifest["diagnostic_run_start_ledger"]["first_diagnostic_execution_started_at_utc"]
            )
            self.assertEqual(
                manifest["outcome_exclusion_assertion"],
                {"correctness_outcomes_included": False,
                 "outcomes_consulted": False,
                 "model_outputs_included": False},
            )

    def test_real_mode_requires_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                builder.main(["--out-dir", tmp])

    def test_builder_requires_adopted_family_map_hash_binding(self):
        family_map, digest = synthetic_adopted_family_map()
        family_map_info = {"sha256": digest}
        allocation_report = {
            "C4": {
                "status": "ASSESSED",
                "family_map_sha256_verified": True,
                "family_map_roster_partition_verified": True,
                "family_map_adoption_ref": {
                    "status": "ADOPTED",
                    "artifact_id": family_map["artifact_id"],
                    "sha256": digest,
                },
            }
        }
        builder._verify_family_map_adoption_binding(
            family_map, family_map_info, allocation_report
        )
        allocation_report["C4"]["family_map_adoption_ref"]["sha256"] = "b" * 64
        with self.assertRaisesRegex(SystemExit, "BUILDER_FAMILY_MAP_ADOPTION_BINDING_MISMATCH"):
            builder._verify_family_map_adoption_binding(
                family_map, family_map_info, allocation_report
            )
        family_map["status"] = "DERIVED_PENDING_ADOPTION"
        with self.assertRaisesRegex(SystemExit, "BUILDER_FAMILY_MAP_NOT_ADOPTED"):
            builder._verify_family_map_adoption_binding(
                family_map, family_map_info, allocation_report
            )

    def test_real_inventory_requires_five_roles_per_parent(self):
        inventory = {
            "artifact_id": "SYNTHETIC-REAL-INVENTORY-INPUT",
            "version": "0.0-synthetic",
            "expected_variant_count": 150,
            "validity_status": "EXPECTED_NOT_RUN",
            "variants": [],
        }
        for parent in ROSTER["parents"]:
            for role in builder.ROLES:
                inventory["variants"].append({
                    "variant_id": f"SYN-{parent['parent_id']}-{role}",
                    "parent_id": parent["parent_id"],
                    "Z_id": parent["Z_id"],
                    "q_id": f"SYN-Q-{parent['parent_id']}-{role}",
                    "role": role,
                    "validity_status": "EXPECTED_NOT_RUN",
                })
        checked = builder._validate_real_inventory(inventory, ROSTER)
        q_registry = builder._build_q_registry(checked, synthetic=True)
        self.assertEqual(
            sum(len(item["variant_ids"]) for item in q_registry["q_entries"]),
            150,
        )
        inventory["variants"].pop()
        with self.assertRaisesRegex(SystemExit, "BUILDER_INVENTORY_VARIANT_COUNT_NOT_150"):
            builder._validate_real_inventory(inventory, ROSTER)



    def test_real_builder_path_accepts_supplied_inventory_end_to_end(self):
        import validate_records

        family_map, family_map_sha256 = synthetic_adopted_family_map()
        allocation_report = validate_annex.audit_annex(
            synthetic_valid_annex(),
            ROSTER,
            ANNEX_SCHEMA,
            synthetic_parent_identities(family_map, family_map_sha256),
            family_map_sha256,
            family_map,
            family_map_sha256,
        )
        self.assertEqual(
            allocation_report["audit_decision"],
            "STRUCTURAL_INTAKE_PASS_C6_ADEQUACY_NOT_ASSESSED",
        )

        inventory = {
            "artifact_id": "SYNTHETIC-REAL-INVENTORY",
            "version": "0.0-synthetic-test",
            "expected_variant_count": 150,
            "validity_status": "EXPECTED_NOT_RUN",
            "variants": [],
        }
        n = 0
        for parent in ROSTER["parents"]:
            for role in builder.ROLES:
                n += 1
                inventory["variants"].append({
                    "variant_id": f"TEST-V{n:03d}",
                    "parent_id": parent["parent_id"],
                    "Z_id": parent["Z_id"],
                    "q_id": f"TEST-Q-{parent['parent_id']}-{role}",
                    "role": role,
                    "validity_status": "EXPECTED_NOT_RUN",
                })

        evidence = {"evidence_id": "SYNTHETIC-EVIDENCE", "sha256": "e" * 64}
        artifact_ref = {
            "artifact_id": "SYNTHETIC-ARTIFACT",
            "version": "0.0-synthetic-test",
            "git_blob_sha1": "f" * 40,
            "sha256": "a" * 64,
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inputs = {
                "roster.json": ROSTER,
                "family_map.json": family_map,
                "inventory.json": inventory,
                "allocation_report.json": allocation_report,
                "bank_identity.json": {
                    "bank_id": "SYNTHETIC-BANK",
                    "version": "0.0-synthetic",
                    "sha256": "b" * 64,
                    "record_manifest_sha256": "c" * 64,
                },
                "governance.json": {
                    "historical_selection_history_status": "NOT_RECONSTRUCTED",
                    "historical_selection_description": "Synthetic test fixture only.",
                    "future_bank_generation_selection_status": "NOT_YET_SPECIFIED",
                    "evidence_refs": [evidence],
                },
                "rule_ref.json": artifact_ref,
                "provenance_refs.json": {
                    "generation_record_ref": evidence,
                    "build_record_ref": evidence,
                    "diagnostic_run_record_ref": evidence,
                },
                "evaluation_row_basis_ref.json": artifact_ref,
            }
            for name, value in inputs.items():
                (root / name).write_text(
                    json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + chr(10),
                    encoding="utf-8",
                )

            out = root / "out"
            rc = builder.main([
                "--roster", str(root / "roster.json"),
                "--family-map", str(root / "family_map.json"),
                "--inventory", str(root / "inventory.json"),
                "--allocation", str(root / "allocation_report.json"),
                "--bank-identity", str(root / "bank_identity.json"),
                "--governance", str(root / "governance.json"),
                "--rule-ref", str(root / "rule_ref.json"),
                "--provenance-refs", str(root / "provenance_refs.json"),
                "--evaluation-row-basis-ref", str(root / "evaluation_row_basis_ref.json"),
                "--out-dir", str(out),
            ])
            self.assertEqual(rc, 0)

            report = _load(out / "build_report.json")
            q_registry = _load(out / "q_registry.json")
            built_inventory = _load(out / "variant_inventory.json")
            ledger = _load(out / "run_start_ledger.json")
            manifest_raw = (out / "preregistration_manifest.json").read_bytes()
            manifest = json.loads(manifest_raw.decode("utf-8"))

            self.assertEqual(report["variant_count"], 150)
            self.assertEqual(report["q_registry_variant_crosswalk_count"], 150)
            self.assertEqual(len(q_registry["q_entries"]), 150)
            self.assertEqual(
                [v["variant_id"] for v in built_inventory["variants"]],
                [v["variant_id"] for v in inventory["variants"]],
            )
            self.assertEqual(len(ledger["rows"]), 150)
            self.assertTrue(all(row["execution_state"] == "NOT_STARTED" for row in ledger["rows"]))

            schema = validate_records.load_and_verify_schema()
            manifest_sha256 = validate_records.hashlib.sha256(manifest_raw).hexdigest()
            validation = validate_records.validate_manifest(manifest, manifest_sha256, schema)
            self.assertEqual(
                validation["manifest_decision"],
                "LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED",
                validation["manifest_reason_codes"],
            )
            self.assertTrue(
                all(row["validity_status"] == "EXPECTED_NOT_RUN" for row in manifest["variants"])
            )

if __name__ == "__main__":
    unittest.main()
