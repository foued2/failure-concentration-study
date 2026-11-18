#!/usr/bin/env python3
"""Deterministically build the synthetic fixture corpus for validate_manifest.py.

The corpus is synthetic: it contains no study data, no real parent identifiers and
no real diagnostic outcomes. Digests are sha256 over fixture-internal labels.

Run from this directory:  python build_fixtures.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STRATA = [f"S{i}" for i in range(1, 9)]
STANDARD = "G0-LIMITS-2026-11-17"
TIGHT = "G0-LIMITS-TIGHT-2026-11-17"

LIMITS = {
    STANDARD: {
        "max_parents": 8,
        "max_variants_per_parent": 8,
        "max_total_variants": 64,
        "m1_si_min_qualifying_parents": 3,
    },
    TIGHT: {
        "max_parents": 2,
        "max_variants_per_parent": 8,
        "max_total_variants": 64,
        "m1_si_min_qualifying_parents": 3,
    },
}

# stratum count vectors for k_fail = 5, giving C_D = 1, 3/5 and 2/5
K5_C1 = (5, 0, 0, 0, 0, 0, 0, 0)
K5_C35 = (3, 1, 1, 0, 0, 0, 0, 0)
K5_C25 = (2, 1, 1, 1, 0, 0, 0, 0)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def rational(counts) -> str:
    total = sum(counts)
    best = max(counts)
    from fractions import Fraction

    value = Fraction(best, total)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def parent(pid, eligible=True, operator="OC-A", reason=None, notes=""):
    return {
        "parent_id": pid,
        "operator_class": operator,
        "eligible": eligible,
        "exclusion_reason": reason if not eligible else None,
        "notes": notes,
    }


def variant(
    vid,
    pid,
    *,
    q="q1",
    Z="z1",
    k_unresolved=0,
    threshold=5,
    site="S17",
    counts=K5_C35,
    src=None,
    art=None,
    construction="BUILT",
    diagnostic="COMPLETED",
    disposition=None,
    build_failure=None,
    notes="",
):
    record = {
        "variant_id": vid,
        "parent_id": pid,
        "site_ref": site,
        "cell": {"q": q, "Z": Z, "k_unresolved": k_unresolved},
        "settings": {"threshold": threshold, "extent": "narrow"},
        "source_digest": src or digest(f"{vid}:source"),
        "artifact_digest": art or digest(f"{vid}:artifact"),
        "construction_status": construction,
        "build_failure_reason": build_failure,
        "diagnostic_status": diagnostic,
        "diagnostic_disposition": disposition,
        "strata_counts": None,
        "k_fail": None,
        "C_D": None,
        "concentration_label": None,
        "notes": notes,
    }
    if construction == "BUILT" and diagnostic == "COMPLETED":
        record["strata_counts"] = dict(zip(STRATA, counts))
        record["k_fail"] = sum(counts)
        if sum(counts) == 0:
            record["concentration_label"] = "NO_OBSERVED_FAILURES"
        else:
            record["C_D"] = rational(counts)
    return record


def manifest(mid, parents, variants, limits_id=STANDARD):
    return {
        "manifest_id": mid,
        "limits_id": limits_id,
        "limits_echo": dict(LIMITS[limits_id]),
        "counts": {"parents": len(parents), "variants": len(variants)},
        "parents": parents,
        "variants": variants,
    }


def three_qualifying_parents():
    """P01-P03, each with two variants in one cell differing in settings, C_D,
    source digest and artifact digest. All share site S17 within a parent, which
    correction A makes admissible."""
    parents = [parent("P01"), parent("P02"), parent("P03")]
    variants = []
    for pid in ("P01", "P02", "P03"):
        variants.append(variant(f"{pid}-V1", pid, threshold=5, counts=K5_C35))
        variants.append(variant(f"{pid}-V2", pid, threshold=10, counts=K5_C1))
    return parents, variants


def build():
    fixtures = {}

    parents, variants = three_qualifying_parents()
    fixtures["valid_realized.json"] = manifest("M-realized", parents, variants)

    parents, variants = three_qualifying_parents()
    fixtures["valid_not_realized.json"] = manifest(
        "M-two-parents", parents[:2], [v for v in variants if v["parent_id"] != "P03"]
    )

    parents, variants = three_qualifying_parents()
    fixtures["cross_parent_digest.json"] = manifest(
        "M-cross-parent-digest",
        parents,
        [
            variant(
                v["variant_id"],
                v["parent_id"],
                threshold=v["settings"]["threshold"],
                counts=K5_C35 if v["variant_id"].endswith("V1") else K5_C1,
                art=digest("SHARED-ARTIFACT") if v["variant_id"] in ("P01-V1", "P02-V1") else None,
            )
            for v in variants
        ],
    )

    parents, variants = three_qualifying_parents()
    variants.append(
        variant("P01-V3", "P01", threshold=5, counts=K5_C35, notes="same site and settings as P01-V1")
    )
    fixtures["dup_settings_alias.json"] = manifest("M-dup-settings", parents, variants)

    parents, variants = three_qualifying_parents()
    for v in variants:
        if v["variant_id"] == "P01-V1":
            v["C_D"] = "1/2"
    fixtures["cd_miscalculated.json"] = manifest("M-cd-mismatch", parents, variants)

    parents, variants = three_qualifying_parents()
    for v in variants:
        if v["variant_id"] == "P01-V1":
            v["k_fail"] = 4
    fixtures["cd_sum_mismatch.json"] = manifest("M-cd-sum", parents, variants)

    parents, variants = three_qualifying_parents()
    zero = variant("P01-V1", "P01", threshold=5, counts=(0, 0, 0, 0, 0, 0, 0, 0))
    zero["C_D"] = "0"
    zero["concentration_label"] = None
    variants[0] = zero
    fixtures["cd_zero_without_convention.json"] = manifest("M-cd-zero", parents, variants)

    parents, variants = three_qualifying_parents()
    echo_mismatch = manifest("M-echo", parents, variants)
    echo_mismatch["limits_id"] = "G0-LIMITS-OTHER"
    fixtures["limits_echo_mismatch.json"] = echo_mismatch

    parents, variants = three_qualifying_parents()
    fixtures["ceiling_exceeded.json"] = manifest("M-ceiling", parents, variants, limits_id=TIGHT)

    parents = [parent("P01")]
    variants = [
        variant("P01-V1", "P01", threshold=5, counts=K5_C35, construction="PLANNED", diagnostic="NOT_RUN"),
        variant("P01-V2", "P01", threshold=10, counts=K5_C1, construction="PLANNED", diagnostic="NOT_RUN"),
    ]
    fixtures["planned_only.json"] = manifest("M-planned", parents, variants)

    parents = [parent("P01")]
    variants = [
        variant("P01-V1", "P01", threshold=5, counts=K5_C35, diagnostic="NOT_RUN"),
        variant("P01-V2", "P01", threshold=10, counts=K5_C1, diagnostic="NOT_RUN"),
    ]
    fixtures["built_not_diagnosed.json"] = manifest("M-built", parents, variants)

    parents = [parent("P01")]
    variants = [
        variant("P01-V1", "P01", threshold=5, counts=K5_C35),
        variant("P01-V2", "P99", threshold=10, counts=K5_C1),
    ]
    fixtures["missing_parent_ref.json"] = manifest("M-missing-ref", parents, variants)

    parents = [parent("P01")]
    variants = [
        variant("P01-V1", "P01", threshold=5, counts=K5_C35, site="TODO"),
        variant("P01-V2", "P01", threshold=10, counts=K5_C1),
    ]
    fixtures["placeholder_machine_field.json"] = manifest("M-placeholder", parents, variants)

    parents, variants = three_qualifying_parents()
    shared_source = digest("SHARED-SOURCE")
    for v in variants:
        if v["parent_id"] == "P01":
            v["source_digest"] = shared_source
    fixtures["same_source_pair.json"] = manifest("M-same-source", parents, variants)

    parents = [parent("P01")]
    variants = [
        variant("P01-V1", "P01", threshold=5, counts=K5_C35),
        variant(
            "P01-V2",
            "P01",
            threshold=10,
            counts=K5_C1,
            construction="BUILD_FAILED",
            diagnostic="NOT_RUN",
            build_failure="compiler rejected generated body",
        ),
    ]
    fixtures["build_failed.json"] = manifest("M-build-failed", parents, variants)

    parents = [parent("P01")]
    variants = [
        variant("P01-V1", "P01", threshold=5, counts=K5_C35, diagnostic="UNRESOLVED", disposition="TIMEOUT"),
    ]
    fixtures["unresolved_outcome.json"] = manifest("M-unresolved", parents, variants)

    parents, variants = three_qualifying_parents()
    broken = manifest("M-count", parents, variants)
    broken["counts"]["variants"] = len(variants) + 1
    fixtures["count_mismatch.json"] = broken

    ineligible = manifest(
        "M-ineligible",
        [parent("P01", eligible=False, reason="outside declared operator class")],
        [variant("P01-V1", "P01", threshold=5, counts=K5_C35)],
    )
    fixtures["ineligible_parent.json"] = ineligible

    # adversarial: three parents, two variants each, but identical settings, so no
    # pair can witness a settings difference even though C_D differs.
    parents, variants = three_qualifying_parents()
    for v in variants:
        v["settings"] = {"threshold": 5, "extent": "narrow"}
    fixtures["no_settings_variation.json"] = manifest("M-no-settings", parents, variants)

    # adversarial: three parents, settings differ, but C_D is identical in each parent.
    parents, variants = three_qualifying_parents()
    for v in variants:
        v["strata_counts"] = dict(zip(STRATA, K5_C1))
        v["C_D"] = "1"
    fixtures["no_concentration_variation.json"] = manifest("M-no-concentration", parents, variants)

    # k_fail = 0 with the labelled convention is admissible but cannot support M1-si.
    parents = [parent("P01")]
    zero_ok = variant("P01-V1", "P01", threshold=5, counts=(0, 0, 0, 0, 0, 0, 0, 0))
    fixtures["zero_failures_labelled.json"] = manifest("M-zero-ok", parents, [zero_ok])

    parents = [parent("P01")]
    bad_setting = variant("P01-V1", "P01", threshold=5, counts=K5_C35)
    bad_setting["settings"] = {"threshold": "TBD", "extent": "narrow"}
    fixtures["settings_placeholder.json"] = manifest("M-settings-placeholder", parents, [bad_setting])

    parents, variants = three_qualifying_parents()
    echo_bad = manifest("M-echo-value", parents, variants)
    echo_bad["limits_echo"]["max_parents"] = 999
    fixtures["limits_echo_mismatch_values.json"] = echo_bad

    for name, payload in sorted(fixtures.items()):
        (HERE / name).write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
        )
    return sorted(fixtures)


if __name__ == "__main__":
    names = build()
    print(f"wrote {len(names)} fixtures")
    for name in names:
        print(f"  {name}")
