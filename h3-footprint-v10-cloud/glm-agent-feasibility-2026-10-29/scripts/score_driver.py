#!/usr/bin/env python3
"""GLM-agent H3 exploratory pilot - scoring stage.

1. Runs the repository's own validate_controls.py (from a clean copy, keeping
   the clone untouched) to re-verify the frozen expected values through three
   independent oracle implementations. This is the independent verification of
   expected probe outcomes required by the work order.
2. Invokes the trusted run_scoring() from copilot_auto_pilot.py UNCHANGED on
   the pilot's candidate-index.json + execution reports.
3. Writes final aggregate JSON with identity/sandbox attribution corrections,
   keeping the raw trusted-scorer output untouched as evidence.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = Path("/home/z/my-project/fcs-verify")
V3_SRC = REPO / "h3-footprint-v3"
V3_COPY = HERE / "trusted_v3_copy"
PILOT = HERE / "pilot-run"
PROVIDER_ROUTE = "z-ai CLI chat (platform-provided GLM access in analysis sandbox)"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    # ---- 1. independent oracle validation (trusted code, clean copy) --------
    if V3_COPY.exists():
        shutil.rmtree(V3_COPY)
    shutil.copytree(V3_SRC, V3_COPY)
    frozen = json.loads((V3_COPY / "FREEZE.json").read_text())["artifact_hashes_sha256"]
    hash_check = {}
    for rel, expected in frozen.items():
        actual = sha256_file(V3_COPY / rel)
        hash_check[rel] = {"match": actual == expected, "expected": expected, "actual": actual}
    all_match = all(v["match"] for v in hash_check.values())
    print(f"freeze-chain hash check: {'ALL MATCH' if all_match else 'MISMATCH'} "
          f"({sum(v['match'] for v in hash_check.values())}/{len(hash_check)})", flush=True)

    val = subprocess.run([sys.executable, "validate_controls.py"], cwd=V3_COPY,
                         capture_output=True, text=True, timeout=600)
    val_report = None
    try:
        val_report = json.loads((V3_COPY / "validation-report.json").read_text())
    except Exception:
        pass
    oracle_ok = bool(val_report and val_report.get("status") == "PASS")
    print(f"validate_controls.py: rc={val.returncode} status="
          f"{val_report.get('status') if val_report else 'NO REPORT'} "
          f"oracle_agreement={val_report['oracle_validation']['oracle_agreement_count'] if val_report else '?'}",
          flush=True)

    # ---- 2. trusted scorer, unchanged ----------------------------------------
    spec = importlib.util.spec_from_file_location(
        "copilot_auto_pilot", REPO / "h3-footprint-v10-cloud" / "copilot_auto_pilot.py")
    trusted = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(trusted)

    raw_out = PILOT / "score-report-RAW-trusted-scorer.json"
    trusted.run_scoring(
        PILOT / "candidate-index.json",
        PILOT / "execution-reports",
        V3_COPY / "expected_values.json",
        V3_COPY / "instrument.py",
        raw_out,
    )

    # ---- 3. final aggregate (identity/sandbox attribution only) --------------
    raw = json.loads(raw_out.read_text(encoding="utf-8"))
    index = json.loads((PILOT / "candidate-index.json").read_text(encoding="utf-8"))
    model_by_request = {r["request_id"]: r.get("endpoint_reported_model") for r in index["requests"]}
    for row in raw.get("candidate_results", []):
        row["model_requested"] = "platform-default"
        row["model_reported_by_endpoint"] = model_by_request.get(row["request_id"])
        row["actual_model_identity_verified"] = False
    raw["provider_route"] = PROVIDER_ROUTE
    raw["model_requested"] = "platform-default"
    raw["endpoint_reported_models"] = sorted({m for m in model_by_request.values() if m})
    raw["actual_model_identity_verified"] = False
    raw["kind"] = "glm_agent_single_provider_exploratory_footprint_screen"
    raw["interpretation"] = ("GLM-agent exploratory screen only; NOT the frozen three-generator "
                             "H3 gate; generator differs from the frozen generator list by design")
    raw["isolation_mechanism"] = ("unshare -r -m -n user/mount/network namespaces + fresh tmpfs "
                                  "overlays + minimal chroot view root + rlimits + 5s probe "
                                  "deadline; verified by hostile controls in isolation-report.json")
    raw["independent_expected_value_verification"] = {
        "method": "validate_controls.py (dijkstra + bellman_ford + brute_force oracle agreement)",
        "status": val_report.get("status") if val_report else None,
        "oracle_agreement_count": val_report["oracle_validation"]["oracle_agreement_count"] if val_report else None,
        "freeze_chain_hashes_match": all_match,
        "unit_test_count": val_report.get("unit_test_count") if val_report else None,
    }
    raw["original_gate_pass_claimed"] = False
    raw["original_gate_verdict"] = "NOT_APPLICABLE_TO_12-REQUEST_GLM_AGENT_SCREEN"
    final_out = PILOT / "score-report-final.json"
    final_out.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "valid_unique_candidates_assigned_k": raw["valid_unique_candidates_assigned_k"],
        "k_distribution_valid_candidates": raw["k_distribution_valid_candidates"],
        "eligible_candidate_count_2_to_24": raw["eligible_candidate_count_2_to_24"],
        "same_k_different_C_observed": raw["same_k_different_C_observed"],
        "supported_cell_count": raw["supported_cell_count"],
        "cross_C_group_pair_count": raw["cross_C_group_pair_count"],
        "eligible_saturation_rate": raw["eligible_saturation_rate"],
        "original_gate_verdict": raw["original_gate_verdict"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
