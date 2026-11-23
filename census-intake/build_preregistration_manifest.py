"""LC518 B1 v1.7 pre-registration manifest builder (design-stage machinery).

MACHINERY ONLY — NOT AN AUTHORIZATION, NOT A CENSUS, NOT A SELECTION ACT.

Assembles the 17-field B1 v1.7 census manifest (schema draft 0.6, pinned blob
0f2865e606fa61400184c09abd01601497637a6b) in its PRE-EXECUTION form:

  - every variant validity_status = EXPECTED_NOT_RUN with an inventory-audit
    status decision (terminal-value and derived-count consultation flags false,
    record-presence metadata false),
  - diagnostic_record_results = [] for every variant,
  - run-start ledger with exactly one NOT_STARTED row per variant and
    first_diagnostic_execution_started_at_utc = null,
  - outcome_exclusion_assertion all false (outcome-blind by construction).

The builder emits the referenced input artifacts itself (run-start ledger,
variant inventory, q registry) and pins them by SHA-256 and Git blob SHA-1
computed from the emitted bytes. It never invents mutation content: allocation
content must come from an owner-supplied annex that has passed
validate_annex.py, or from explicitly labelled synthetic demo inputs
(--demo-synthetic, invented IDs/digests only, for machinery verification).

Inputs (real build):
  --roster        parent roster JSON (e.g. gate1-inputs/PARENT_ROSTER_G01_G30.json)
  --family-map    family map JSON (e.g. gate1-inputs/FAMILY_MAP.json)
  --allocation    annex audit report from validate_annex.py with audit_decision
                  ALL_LOCAL_RULES_PASS (supplies q_id mechanism identities)
  --bank-identity JSON: bank_id, version, sha256, record_manifest_sha256
  --governance    JSON: diagnostic_exposure_disclosure content supplied by the
                  reviewer/owner (selection-history status and description,
                  future-bank status, evidence refs)
  --rule-ref      JSON artifactRef of the governing instrument/rule document
  --out-dir       output directory

Demo mode (--demo-synthetic) fabricates every annex-dependent input with
SYN_-prefixed invented identifiers and 64-hex digests derived from random
bytes, writes them to the output directory, and builds the manifest from
them. Its only purpose is to prove the emitted manifest passes the reviewed
intake checker end to end. It establishes nothing scientifically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

TOOL_NAME = "lc518-b1-preregistration-builder"
TOOL_VERSION = "1.0.0"
LABEL = "PREREGISTRATION MACHINERY — NOT AN AUTHORIZATION — DESIGN STAGE ONLY"
DEMO_LABEL = "SYNTHETIC DEMO — INVENTED IDS AND DIGESTS — MACHINERY VERIFICATION ONLY"

STRATA = [f"D{i}" for i in range(1, 9)]
ROLES = ["S0", "SA", "SB", "SAB", "S-EXTRA"]


def _git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _write_json(path: Path, obj) -> dict:
    raw = (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    path.write_bytes(raw)
    return {"sha256": _sha256(raw), "git_blob_sha1": _git_blob_sha1(raw), "bytes": len(raw)}


def _artifact_ref(artifact_id: str, version: str, info: dict) -> dict:
    return {
        "artifact_id": artifact_id,
        "version": version,
        "git_blob_sha1": info["git_blob_sha1"],
        "sha256": info["sha256"],
    }


def _evidence_ref(evidence_id: str, sha256: str) -> dict:
    return {"evidence_id": evidence_id, "sha256": sha256}


def _synthetic_digest() -> str:
    return secrets.token_hex(32)


def _load_file_ref(path: Path) -> dict:
    raw = path.read_bytes()
    json.loads(raw.decode("utf-8"))
    return {"sha256": _sha256(raw), "git_blob_sha1": _git_blob_sha1(raw), "bytes": len(raw)}


def build_inputs(args) -> dict:
    """Load or fabricate the input artifact set. Returns a context dict."""
    ctx: dict = {"demo": bool(args.demo_synthetic)}
    label = DEMO_LABEL if ctx["demo"] else LABEL
    ctx["label"] = label

    if ctx["demo"]:
        roster = json.loads((Path(args.roster) if args.roster else _default("PARENT_ROSTER_G01_G30.json")).read_bytes().decode("utf-8"))
        family_map = json.loads((Path(args.family_map) if args.family_map else _default("FAMILY_MAP.json")).read_bytes().decode("utf-8"))
        ctx["roster"] = roster
        ctx["family_map"] = family_map
        ctx["roster_info"] = _load_file_ref(Path(args.roster) if args.roster else _default("PARENT_ROSTER_G01_G30.json"))
        ctx["family_map_info"] = _load_file_ref(Path(args.family_map) if args.family_map else _default("FAMILY_MAP.json"))
        # Synthetic allocation: invented mechanism identities over the real
        # frozen parent structure. Labels make the boundary explicit.
        parents = [p["parent_id"] for p in roster["parents"]]
        mech_ids = [f"M{i}" for i in range(1, 9)]
        import itertools
        pairs = list(itertools.combinations(mech_ids, 2))[:28]
        ctx["allocation"] = {
            "demo": True,
            "pair_assignments": [
                {"parent_id": parents[i], "mechanism_a": pairs[i][0], "mechanism_b": pairs[i][1],
                 "is_replication": False}
                for i in range(28)
            ] + [
                {"parent_id": parents[28], "mechanism_a": pairs[0][0], "mechanism_b": pairs[0][1],
                 "is_replication": True, "preselection_evidence": "SYNTHETIC demo preselection"},
                {"parent_id": parents[29], "mechanism_a": pairs[1][0], "mechanism_b": pairs[1][1],
                 "is_replication": True, "preselection_evidence": "SYNTHETIC demo preselection"},
            ],
            "s_extra_assignments": [
                {"parent_id": p, "mechanism_id": mech_ids[i % 8]} for i, p in enumerate(parents)
            ],
        }
        ctx["bank_identity"] = {
            "bank_id": "SYN-DIAGNOSTIC-BANK",
            "version": "0.0-synthetic",
            "sha256": _synthetic_digest(),
            "record_manifest_sha256": _synthetic_digest(),
        }
        ctx["governance"] = {
            "historical_selection_history_status": "NOT_RECONSTRUCTED",
            "historical_selection_description": (
                "SYNTHETIC DEMO VALUE. The real value must be supplied by the "
                "reviewer/owner in the governance input file."
            ),
            "future_bank_generation_selection_status": "NOT_YET_SPECIFIED",
            "evidence_refs": [_evidence_ref("SYN-evidence", _synthetic_digest())],
        }
        ctx["rule_ref"] = {
            "artifact_id": "SYN-governing-instrument",
            "version": "0.0-synthetic",
            "git_blob_sha1": _synthetic_digest()[:40],
            "sha256": _synthetic_digest(),
        }
        ctx["provenance_refs"] = {
            "generation_record_ref": _evidence_ref("SYN-generation-record", _synthetic_digest()),
            "build_record_ref": _evidence_ref("SYN-build-record", _synthetic_digest()),
            "diagnostic_run_record_ref": _evidence_ref("SYN-run-record", _synthetic_digest()),
        }
        return ctx

    # Real build: every input must be supplied; nothing is fabricated.
    required = {
        "roster": args.roster, "family_map": args.family_map, "allocation": args.allocation,
        "bank_identity": args.bank_identity, "governance": args.governance,
        "rule_ref": args.rule_ref, "provenance_refs": args.provenance_refs,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise SystemExit(
            "BUILDER_INPUT_MISSING: real (non-demo) builds require " + ", ".join(missing)
        )
    ctx["roster"] = json.loads(Path(args.roster).read_bytes().decode("utf-8"))
    ctx["family_map"] = json.loads(Path(args.family_map).read_bytes().decode("utf-8"))
    ctx["roster_info"] = _load_file_ref(Path(args.roster))
    ctx["family_map_info"] = _load_file_ref(Path(args.family_map))
    alloc_report = json.loads(Path(args.allocation).read_bytes().decode("utf-8"))
    if alloc_report.get("audit_decision") != "ALL_LOCAL_RULES_PASS":
        raise SystemExit("BUILDER_ALLOCATION_NOT_AUDITED: allocation input must be an ALL_LOCAL_RULES_PASS audit report from validate_annex.py")
    ctx["allocation"] = alloc_report.get("annex") or alloc_report
    ctx["bank_identity"] = json.loads(Path(args.bank_identity).read_bytes().decode("utf-8"))
    ctx["governance"] = json.loads(Path(args.governance).read_bytes().decode("utf-8"))
    ctx["rule_ref"] = json.loads(Path(args.rule_ref).read_bytes().decode("utf-8"))
    ctx["provenance_refs"] = json.loads(Path(args.provenance_refs).read_bytes().decode("utf-8"))
    return ctx


def _default(name: str) -> Path:
    return Path(__file__).resolve().parent / "gate1-inputs" / name


def emit_artifacts(ctx: dict, out_dir: Path, now_utc: str) -> dict:
    """Emit q registry, variant inventory, run-start ledger; return refs+info."""
    roster = ctx["roster"]
    family_parents = {p["Z_id"] for p in roster["parents"]}
    parents = [p["parent_id"] for p in roster["parents"]]
    alloc = ctx["allocation"]
    synth = ctx["demo"]

    pair_by_parent = {a["parent_id"]: a for a in alloc["pair_assignments"]}
    s_extra_by_parent = {s["parent_id"]: s for s in alloc["s_extra_assignments"]}

    # q registry: one q identity per variant slot (150). q carries the
    # mechanism identity (m component of the B1 cell). S0 slots carry the
    # unmutated baseline identity.
    q_registry = {
        "artifact_id": "SYN-q-registry" if synth else "lc518-150-q-registry",
        "version": "0.0-synthetic" if synth else "1.0",
        "label": DEMO_LABEL if synth else LABEL,
        "q_entries": [],
    }
    inventory = {
        "artifact_id": "SYN-variant-inventory" if synth else "lc518-150-variant-inventory",
        "version": "0.0-synthetic" if synth else "1.0",
        "label": DEMO_LABEL if synth else LABEL,
        "expected_variant_count": 150,
        "validity_status": "EXPECTED_NOT_RUN",
        "variants": [],
    }
    ledger_rows = []

    seq = 0
    for parent in roster["parents"]:
        pid, zid = parent["parent_id"], parent["Z_id"]
        if zid not in family_parents:
            raise SystemExit(f"BUILDER_ROSTER_FAMILY_UNKNOWN: {pid} -> {zid}")
        pair = pair_by_parent.get(pid)
        s_extra = s_extra_by_parent.get(pid)
        if pair is None or s_extra is None:
            raise SystemExit(f"BUILDER_ALLOCATION_INCOMPLETE: parent {pid}")
        base = f"SYN-S{seq + 1:03d}" if synth else None
        for role in ROLES:
            seq += 1
            if synth:
                vid = base if role == "S0" else f"{base}-{role}"
                q_id = {
                    "S0": f"SYN-Q-BASE-{pid}",
                    "SA": f"SYN-Q-A-{pair['mechanism_a']}-{pid}",
                    "SB": f"SYN-Q-B-{pair['mechanism_b']}-{pid}",
                    "SAB": f"SYN-Q-AB-{pair['mechanism_a']}+{pair['mechanism_b']}-{pid}",
                    "S-EXTRA": f"SYN-Q-X-{s_extra['mechanism_id']}-{pid}",
                }[role]
            else:
                vid = None  # assigned at construction (opaque permutation)
                q_id = None
            if vid is None:
                raise SystemExit(
                    "BUILDER_VARIANT_ID_UNASSIGNED: variant_id and q_id for real "
                    "builds are assigned at construction (PARENT_DESIGN.md Section 1); "
                    "supply a filled inventory or run --demo-synthetic."
                )
            inventory["variants"].append({
                "variant_id": vid,
                "parent_id": pid,
                "Z_id": zid,
                "q_id": q_id,
                "role": role,
                "validity_status": "EXPECTED_NOT_RUN",
            })
            ledger_rows.append({
                "variant_id": vid,
                "execution_state": "NOT_STARTED",
                "started_at_utc": None,
            })

    q_reg_info = _write_json(out_dir / "q_registry.json", q_registry)
    inv_info = _write_json(out_dir / "variant_inventory.json", inventory)
    ledger = {
        "artifact_id": "SYN-run-start-ledger" if synth else "lc518-b1-run-start-ledger",
        "version": "0.0-synthetic" if synth else "1.0",
        "label": DEMO_LABEL if synth else LABEL,
        "snapshot_as_of_utc": now_utc,
        "rows": ledger_rows,
    }
    ledger_info = _write_json(out_dir / "run_start_ledger.json", ledger)
    if seq != 150:
        raise SystemExit(f"BUILDER_POPULATION_COUNT_NOT_150: built {seq}")
    return {
        "q_registry": q_reg_info,
        "inventory": inv_info,
        "ledger": ledger_info,
        "inventory_obj": inventory,
        "ledger_obj": ledger,
    }


def build_manifest(ctx: dict, emitted: dict, out_dir: Path, now_utc: str) -> dict:
    roster = ctx["roster"]
    family_map = ctx["family_map"]
    synth = ctx["demo"]
    ledger_obj = emitted["ledger_obj"]

    exposure = {
        "historical_public_heldout_bank_status": "PUBLICLY_EXPOSED",
        "historical_used_for_candidate_filtering": True,
        "historical_selection_history_status": ctx["governance"]["historical_selection_history_status"],
        "historical_selection_description": ctx["governance"]["historical_selection_description"],
        "future_bank_generation_selection_status": ctx["governance"]["future_bank_generation_selection_status"],
        "evidence_refs": ctx["governance"]["evidence_refs"],
        "independence_claim_permitted": False,
    }

    status_reason = (
        "Pre-registration inventory audit: variant registered before diagnostic "
        "execution; run-start ledger row NOT_STARTED." + (" SYNTHETIC DEMO." if synth else "")
    )
    variants = []
    for row in emitted["inventory_obj"]["variants"]:
        variants.append({
            "variant_id": row["variant_id"],
            "parent_id": row["parent_id"],
            "Z_id": row["Z_id"],
            "q_id": row["q_id"],
            "validity_status": "EXPECTED_NOT_RUN",
            "status_reason": status_reason,
            "status_decision": {
                "rule_ref": ctx["rule_ref"],
                "decision_record_ref": _evidence_ref(
                    "SYN-variant-inventory" if synth else "variant-inventory-preregistration",
                    emitted["inventory"]["sha256"],
                ),
                "decided_at_utc": now_utc,
                "decision_basis": "EXPECTED_NOT_RUN_INVENTORY_AUDIT",
                "diagnostic_terminal_values_consulted": False,
                "derived_failure_unresolved_counts_consulted": False,
                "record_presence_identity_metadata_consulted": False,
            },
            "diagnostic_record_results": [],
        })

    manifest = {
        "schema_version": "0.6-draft",
        "study_id": "LC518",
        "analysis_plan": {
            "name": "B1",
            "version": "1.7",
            "git_blob_sha1": "8c666e501a31726c728447d155045c0b20adc178",
            "sha256": "797bd9f72cf94fdc0eff4a03b1544823d4042f8e530b27f4fb70cbd7f2baca7c",
        },
        "measurement_spec": {
            "name": "C_D measurement specification and exposure register",
            "date": "2026-11-19",
            "git_blob_sha1": "923655f20337b99f11e400f3428d1d18ac34c96d",
        },
        "measurement_basis": "record_level_64",
        "diagnostic_bank": {
            "bank_id": ctx["bank_identity"]["bank_id"],
            "version": ctx["bank_identity"]["version"],
            "sha256": ctx["bank_identity"]["sha256"],
            "record_manifest_sha256": ctx["bank_identity"]["record_manifest_sha256"],
            "stratum_ids": STRATA,
            "records_per_stratum": 8,
            "total_records": 64,
        },
        "diagnostic_exposure_disclosure": exposure,
        "parent_roster_ref": _artifact_ref(
            roster["artifact_id"], roster["version"], ctx["roster_info"]
        ),
        "q_registry_ref": _artifact_ref(
            emitted and json.loads((out_dir / "q_registry.json").read_bytes().decode("utf-8"))["artifact_id"],
            "0.0-synthetic" if synth else "1.0",
            emitted["q_registry"],
        ),
        "family_map_ref": _artifact_ref(
            family_map["artifact_id"], family_map["version"], ctx["family_map_info"]
        ),
        "variant_inventory_ref": _artifact_ref(
            json.loads((out_dir / "variant_inventory.json").read_bytes().decode("utf-8"))["artifact_id"],
            "0.0-synthetic" if synth else "1.0",
            emitted["inventory"],
        ),
        "diagnostic_run_start_ledger": {
            "ledger_ref": _evidence_ref(
                "SYN-run-start-ledger" if synth else "run-start-ledger-preregistration",
                emitted["ledger"]["sha256"],
            ),
            "first_diagnostic_execution_started_at_utc": None,
            "snapshot_as_of_utc": ledger_obj["snapshot_as_of_utc"],
        },
        "provenance": {
            "generation_record_ref": ctx["provenance_refs"]["generation_record_ref"],
            "build_record_ref": ctx["provenance_refs"]["build_record_ref"],
            "diagnostic_run_record_ref": ctx["provenance_refs"]["diagnostic_run_record_ref"],
        },
        "parent_roster": [
            {"parent_id": p["parent_id"], "Z_id": p["Z_id"]} for p in roster["parents"]
        ],
        "variants": variants,
        "outcome_exclusion_assertion": {
            "correctness_outcomes_included": False,
            "outcomes_consulted": False,
            "model_outputs_included": False,
        },
        "evaluation_row_basis": {
            "row_count": 78,
            "source_ref": ctx["evaluation_row_basis_source_ref"],
        },
    }
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=LABEL)
    parser.add_argument("--roster")
    parser.add_argument("--family-map")
    parser.add_argument("--allocation", help="audit report JSON from validate_annex.py (ALL_LOCAL_RULES_PASS)")
    parser.add_argument("--bank-identity")
    parser.add_argument("--governance")
    parser.add_argument("--rule-ref")
    parser.add_argument("--provenance-refs")
    parser.add_argument("--evaluation-row-basis-ref", help="JSON artifactRef for evaluation_row_basis.source_ref (e.g. the frozen B1_78 canonical ID manifest)")
    parser.add_argument("--demo-synthetic", action="store_true", help="fabricate SYN_-labelled synthetic inputs for machinery verification")
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    ctx = build_inputs(args)
    if ctx["demo"]:
        # Demo evaluation-row-basis source: synthetic artifactRef.
        ctx["evaluation_row_basis_source_ref"] = {
            "artifact_id": "SYN-b1-78-canonical-id-manifest",
            "version": "0.0-synthetic",
            "git_blob_sha1": _synthetic_digest()[:40],
            "sha256": _synthetic_digest(),
        }
    else:
        if not args.evaluation_row_basis_ref:
            raise SystemExit("BUILDER_INPUT_MISSING: --evaluation-row-basis-ref (e.g. the frozen B1_78 canonical ID manifest artifactRef)")
        ctx["evaluation_row_basis_source_ref"] = json.loads(
            Path(args.evaluation_row_basis_ref).read_bytes().decode("utf-8")
        )

    emitted = emit_artifacts(ctx, out_dir, now_utc)
    manifest = build_manifest(ctx, emitted, out_dir, now_utc)
    manifest_info = _write_json(out_dir / "preregistration_manifest.json", manifest)

    build_report = {
        "tool": TOOL_NAME,
        "tool_version": TOOL_VERSION,
        "label": ctx["label"],
        "built_at_utc": now_utc,
        "variant_count": len(emitted["inventory_obj"]["variants"]),
        "ledger_row_count": len(emitted["ledger_obj"]["rows"]),
        "all_rows_not_started": all(r["execution_state"] == "NOT_STARTED" for r in emitted["ledger_obj"]["rows"]),
        "first_diagnostic_execution_started_at_utc": None,
        "artifacts": {
            "q_registry.json": emitted["q_registry"],
            "variant_inventory.json": emitted["inventory"],
            "run_start_ledger.json": emitted["ledger"],
            "preregistration_manifest.json": manifest_info,
        },
        "boundary": (
            "This manifest is a design-stage pre-registration artifact. Passing the "
            "intake checker proves schema/semantic conformance only; it is not census "
            "admissibility, not a Gate 1 decision, and authorizes no execution."
        ),
    }
    _write_json(out_dir / "build_report.json", build_report)
    sys.stdout.write(json.dumps(build_report, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
