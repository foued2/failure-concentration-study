#!/usr/bin/env python3
"""Deterministic population-manifest validator (M1-si structural support).

Implements the contract stated in
``GPT_ADJUDICATION_MANIFEST_VALIDATOR_V0.1_2026-11-17.md`` section 4, with the
corrections A-I:

* A  duplicate-operation coordinates include parent, operator class, site and the
     realization settings; the same site with different settings is admissible.
* B  digest distinctness is scoped to (parent, exact cell); a cross-parent digest
     collision raises a provenance warning, it does not invalidate the population.
* C  k_fail and C_D are recomputed from the eight stratum counts and compared to
     the declared canonical rational value.
* D  construction status and diagnostic status are separate fields; only
     completed, admissible diagnostics can contribute to realized support.
* E  ceilings are bound to an independently identified limits file, whose
     SHA-256 is reported; the manifest must echo the limits id exactly.
* F  qualifying parents are identified by an explicit pair witness.
* G  placeholder scanning applies to machine-readable fields only.
* H  the embedded checks are written by hand; the JSON Schema in
     ``manifest_schema.json`` is cross-checked against ``jsonschema`` when that
     package is available (see ``run_tests.py``).
* I  the tool does not acquire study data; the bundled corpus is synthetic.

Zero runtime dependencies. Exit codes: 0 valid, 1 invalid, 2 usage or IO error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

VERSION = "0.2.1"
STRATA = [f"S{i}" for i in range(1, 9)]
CONSTRUCTION_STATUS = ("PLANNED", "BUILT", "BUILD_FAILED")
DIAGNOSTIC_STATUS = ("NOT_RUN", "COMPLETED", "INVALID", "UNRESOLVED")
OPERATOR_CLASSES = ("OC-A", "OC-B", "OC-C", "OC-D")
NO_FAILURES_LABEL = "NO_OBSERVED_FAILURES"
PLACEHOLDERS = frozenset({"", "UNKNOWN", "TODO", "TBD", "FIXME", "N/A", "NA", "?"})
RATIONAL_RE = re.compile(r"^(0|[1-9][0-9]*)(/([1-9][0-9]*))?$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_bytes(data: bytes) -> bytes:
    """Canonical source representation: LF line endings, bytes otherwise unchanged.

    Source identity must not depend on a checkout's line-ending policy, so the
    canonical digest is computed over CRLF -> LF normalized bytes. The raw digest
    of the file actually read is reported alongside it.
    """
    return data.replace(b"\r\n", b"\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_file(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        "sha256_canonical": sha256_bytes(canonical_bytes(raw)),
        "sha256_working": sha256_bytes(raw),
    }


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_text(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def canonical_rational(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def parse_rational(text):
    """Return a Fraction for a canonical rational string, else None."""
    if not isinstance(text, str) or not RATIONAL_RE.match(text):
        return None
    try:
        value = Fraction(text)
    except (ValueError, ZeroDivisionError):
        return None
    if canonical_rational(value) != text:
        return None
    return value


def placeholder(value) -> bool:
    return isinstance(value, str) and value.strip() in PLACEHOLDERS


# --------------------------------------------------------------------------- #
# validator
# --------------------------------------------------------------------------- #

class Validator:
    def __init__(self, manifest, limits, manifest_digest, limits_digest, schema_digest):
        self.m = manifest if isinstance(manifest, dict) else {}
        self.limits = limits if isinstance(limits, dict) else {}
        self.sha = {
            "manifest": manifest_digest,
            "limits": limits_digest,
            "schema": schema_digest,
        }
        self.errors = []
        self.warnings = []
        self.aliases = []
        self.excluded = []
        self.parents = {}
        self.records = []
        self.cells = []
        self.counts = {}
        self.m1_si = "NOT_ESTABLISHED"

    # -- diagnostics ------------------------------------------------------- #

    def err(self, code, path, message):
        self.errors.append({"code": code, "path": path, "message": message})

    def warn(self, code, path, message):
        self.warnings.append({"code": code, "path": path, "message": message})

    def add_alias(self, record, reason, canonical):
        record["alias_of"] = canonical
        record["alias_reason"].append(reason)
        self.aliases.append(
            {
                "variant_id": record["id"],
                "canonical_variant_id": canonical,
                "reason": reason,
                "cell": list(record["cell_full"]) if record["cell_full"] else None,
            }
        )

    # -- limits ------------------------------------------------------------ #

    def check_limits(self):
        lim = self.limits
        required_int = (
            "max_parents",
            "max_variants_per_parent",
            "max_total_variants",
            "m1_si_min_qualifying_parents",
        )
        for key in required_int:
            value = lim.get(key)
            if not is_int(value) or value < 0:
                self.err("LIMITS_FIELD", f"limits.{key}", "required non-negative integer")
        if not is_text(lim.get("limits_id")) or placeholder(lim.get("limits_id")):
            self.err("LIMITS_FIELD", "limits.limits_id", "required non-empty string")
        if lim.get("strata") != STRATA:
            self.err(
                "LIMITS_FIELD",
                "limits.strata",
                f"must declare exactly {STRATA}",
            )

    def check_manifest_top(self):
        m = self.m
        if not isinstance(m, dict) or not m:
            self.err("MANIFEST_SHAPE", "$", "manifest must be a non-empty JSON object")
            return
        if not is_text(m.get("manifest_id")) or placeholder(m.get("manifest_id")):
            self.err("MANIFEST_FIELD", "manifest_id", "required non-empty string")
        if not is_text(m.get("limits_id")) or placeholder(m.get("limits_id")):
            self.err("MANIFEST_FIELD", "limits_id", "required non-empty string")
        elif m.get("limits_id") != self.limits.get("limits_id"):
            self.err(
                "LIMITS_ECHO_MISMATCH",
                "limits_id",
                "manifest limits_id does not equal the authoritative limits file id",
            )
        counts = m.get("counts")
        if not isinstance(counts, dict):
            self.err("MANIFEST_FIELD", "counts", "required object with parents/variants")
        else:
            for key in ("parents", "variants"):
                if not is_int(counts.get(key)):
                    self.err("MANIFEST_FIELD", f"counts.{key}", "required integer")
        echo = m.get("limits_echo")
        if not isinstance(echo, dict):
            self.err(
                "MANIFEST_FIELD",
                "limits_echo",
                "required object echoing the authoritative ceilings",
            )
        else:
            for key in (
                "max_parents",
                "max_variants_per_parent",
                "max_total_variants",
                "m1_si_min_qualifying_parents",
            ):
                value = echo.get(key)
                if not is_int(value):
                    self.err("MANIFEST_FIELD", f"limits_echo.{key}", "required integer")
                elif value != self.limits.get(key):
                    self.err(
                        "LIMITS_ECHO_VALUE",
                        f"limits_echo.{key}",
                        f"echoed {value} != authoritative {self.limits.get(key)}",
                    )
        for key in ("parents", "variants"):
            if not isinstance(m.get(key), list):
                self.err("MANIFEST_FIELD", key, "required array")

    # -- parents ----------------------------------------------------------- #

    def check_parents(self):
        parents = self.m.get("parents")
        if not isinstance(parents, list):
            return
        max_parents = self.limits.get("max_parents")
        if is_int(max_parents) and len(parents) > max_parents:
            self.err(
                "CEILING_EXCEEDED",
                "parents",
                f"{len(parents)} parents exceeds authoritative ceiling {max_parents}",
            )
        declared = (self.m.get("counts") or {}).get("parents")
        if is_int(declared) and declared != len(parents):
            self.err(
                "COUNT_MISMATCH",
                "counts.parents",
                f"declared {declared}, actual {len(parents)}",
            )
        for index, parent in enumerate(parents):
            path = f"parents[{index}]"
            if not isinstance(parent, dict):
                self.err("PARENT_SHAPE", path, "parent record must be an object")
                continue
            pid = parent.get("parent_id")
            if not is_text(pid) or placeholder(pid):
                self.err("PARENT_FIELD", f"{path}.parent_id", "required non-empty string")
                continue
            if pid in self.parents:
                self.err("DUP_ID", f"{path}.parent_id", f"duplicate parent_id {pid!r}")
                continue
            opclass = parent.get("operator_class")
            if opclass not in OPERATOR_CLASSES:
                self.err(
                    "PARENT_FIELD",
                    f"{path}.operator_class",
                    f"must be one of {OPERATOR_CLASSES}",
                )
            eligible = parent.get("eligible")
            if not isinstance(eligible, bool):
                self.err("PARENT_FIELD", f"{path}.eligible", "required boolean")
                eligible = False
            reason = parent.get("exclusion_reason")
            if eligible is False:
                if not is_text(reason) or placeholder(reason):
                    self.err(
                        "PARENT_FIELD",
                        f"{path}.exclusion_reason",
                        "required non-empty reason when eligible is false",
                    )
            elif reason not in (None, ""):
                self.err(
                    "PARENT_FIELD",
                    f"{path}.exclusion_reason",
                    "must be null when eligible is true",
                )
            self.parents[pid] = {
                "eligible": eligible,
                "operator_class": opclass,
                "reason": reason,
            }

    # -- variants ---------------------------------------------------------- #

    def check_variants(self):
        variants = self.m.get("variants")
        if not isinstance(variants, list):
            return
        max_total = self.limits.get("max_total_variants")
        max_per_parent = self.limits.get("max_variants_per_parent")
        if is_int(max_total) and len(variants) > max_total:
            self.err(
                "CEILING_EXCEEDED",
                "variants",
                f"{len(variants)} variants exceeds authoritative ceiling {max_total}",
            )
        declared = (self.m.get("counts") or {}).get("variants")
        if is_int(declared) and declared != len(variants):
            self.err(
                "COUNT_MISMATCH",
                "counts.variants",
                f"declared {declared}, actual {len(variants)}",
            )
        seen_ids = set()
        per_parent = {}
        for index, variant in enumerate(variants):
            path = f"variants[{index}]"
            if not isinstance(variant, dict):
                self.err("VARIANT_SHAPE", path, "variant record must be an object")
                continue
            vid = variant.get("variant_id")
            if not is_text(vid) or placeholder(vid):
                self.err("VARIANT_FIELD", f"{path}.variant_id", "required non-empty string")
                continue
            if vid in seen_ids:
                self.err("DUP_ID", f"{path}.variant_id", f"duplicate variant_id {vid!r}")
                continue
            seen_ids.add(vid)

            record = {
                "id": vid,
                "variant": variant,
                "parent_id": variant.get("parent_id"),
                "settings_key": None,
                "cell_base": None,
                "cell_full": None,
                "k": None,
                "c": None,
                "realized": False,
                "alias_of": None,
                "alias_reason": [],
            }
            self.records.append(record)

            pid = variant.get("parent_id")
            if not is_text(pid) or placeholder(pid):
                self.err("VARIANT_FIELD", f"{path}.parent_id", "required non-empty string")
            elif pid not in self.parents:
                self.err(
                    "REF_MISSING",
                    f"{path}.parent_id",
                    f"parent_id {pid!r} not present in parents",
                )
            else:
                per_parent[pid] = per_parent.get(pid, 0) + 1

            site = variant.get("site_ref")
            if not is_text(site) or placeholder(site):
                self.err("VARIANT_FIELD", f"{path}.site_ref", "required non-empty string")

            cell = variant.get("cell")
            if not isinstance(cell, dict):
                self.err("VARIANT_FIELD", f"{path}.cell", "required object")
                cell = {}
            for key in ("q", "Z"):
                if not is_text(cell.get(key)) or placeholder(cell.get(key)):
                    self.err(
                        "VARIANT_FIELD",
                        f"{path}.cell.{key}",
                        "required non-empty string",
                    )
            if not is_int(cell.get("k_unresolved")) or cell.get("k_unresolved") < 0:
                self.err(
                    "VARIANT_FIELD",
                    f"{path}.cell.k_unresolved",
                    "required non-negative integer",
                )
            record["cell_base"] = (
                cell.get("q"),
                cell.get("Z"),
                cell.get("k_unresolved"),
            )

            settings = variant.get("settings")
            if not isinstance(settings, dict) or not settings:
                self.err("VARIANT_FIELD", f"{path}.settings", "required non-empty object")
            else:
                bad = [
                    key
                    for key, value in settings.items()
                    if not is_text(key) or not (is_int(value) or isinstance(value, (str, bool)))
                ]
                if bad:
                    self.err(
                        "VARIANT_FIELD",
                        f"{path}.settings",
                        "settings must map string keys to scalar values",
                    )
                else:
                    sentinels = [key for key, value in settings.items() if placeholder(value)]
                    if sentinels:
                        self.err(
                            "VARIANT_FIELD",
                            f"{path}.settings",
                            f"placeholder values in machine-readable settings keys {sentinels}",
                        )
                    record["settings_key"] = canonical_json(settings)

            for key in ("source_digest", "artifact_digest"):
                value = variant.get(key)
                if not isinstance(value, str) or not HEX64_RE.match(value):
                    self.err(
                        "VARIANT_FIELD",
                        f"{path}.{key}",
                        "required lowercase 64-character hex digest",
                    )

            construction = variant.get("construction_status")
            if construction not in CONSTRUCTION_STATUS:
                self.err(
                    "VARIANT_FIELD",
                    f"{path}.construction_status",
                    f"must be one of {CONSTRUCTION_STATUS}",
                )
            if construction == "BUILD_FAILED":
                if not is_text(variant.get("build_failure_reason")):
                    self.err(
                        "VARIANT_FIELD",
                        f"{path}.build_failure_reason",
                        "required when construction_status is BUILD_FAILED",
                    )
            elif variant.get("build_failure_reason") not in (None, ""):
                self.err(
                    "VARIANT_FIELD",
                    f"{path}.build_failure_reason",
                    "must be null unless construction_status is BUILD_FAILED",
                )

            diagnostic = variant.get("diagnostic_status")
            if diagnostic not in DIAGNOSTIC_STATUS:
                self.err(
                    "VARIANT_FIELD",
                    f"{path}.diagnostic_status",
                    f"must be one of {DIAGNOSTIC_STATUS}",
                )
            elif diagnostic == "COMPLETED":
                self.check_concentration(record, path)
            else:
                for key in ("strata_counts", "k_fail", "C_D", "concentration_label"):
                    if variant.get(key) is not None:
                        self.err(
                            "VARIANT_FIELD",
                            f"{path}.{key}",
                            "must be null unless diagnostic_status is COMPLETED",
                        )
                if diagnostic in ("INVALID", "UNRESOLVED"):
                    if not is_text(variant.get("diagnostic_disposition")):
                        self.err(
                            "VARIANT_FIELD",
                            f"{path}.diagnostic_disposition",
                            "required for INVALID or UNRESOLVED diagnostics",
                        )
                elif variant.get("diagnostic_disposition") not in (None, ""):
                    self.err(
                        "VARIANT_FIELD",
                        f"{path}.diagnostic_disposition",
                        "must be null when diagnostic_status is NOT_RUN",
                    )

            # lifecycle gate: a record is realized only if it was built and its
            # diagnostic completed with an admissible disposition.
            if construction != "BUILT":
                record["excluded"] = "NOT_BUILT"
            elif diagnostic != "COMPLETED":
                record["excluded"] = "NOT_DIAGNOSED"
            else:
                record["realized"] = True

        for pid, count in sorted(per_parent.items()):
            if is_int(max_per_parent) and count > max_per_parent:
                self.err(
                    "CEILING_EXCEEDED",
                    f"parents[{pid}]",
                    f"{count} variants exceeds per-parent ceiling {max_per_parent}",
                )

    def check_concentration(self, record, path):
        variant = record["variant"]
        strata = variant.get("strata_counts")
        if not isinstance(strata, dict) or set(strata) != set(STRATA):
            self.err(
                "CD_SHAPE",
                f"{path}.strata_counts",
                f"required object with exactly {STRATA}",
            )
            return
        if any(not is_int(v) or v < 0 for v in strata.values()):
            self.err(
                "CD_SHAPE",
                f"{path}.strata_counts",
                "stratum counts must be non-negative integers",
            )
            return

        computed_k = sum(strata[s] for s in STRATA)
        declared_k = variant.get("k_fail")
        if not is_int(declared_k):
            self.err("CD_SHAPE", f"{path}.k_fail", "required integer when COMPLETED")
        elif declared_k != computed_k:
            self.err(
                "CD_SUM_MISMATCH",
                f"{path}.k_fail",
                f"declared {declared_k} != sum of stratum counts {computed_k}",
            )

        if computed_k == 0:
            if variant.get("C_D") is not None:
                self.err(
                    "CD_ZERO_CONVENTION",
                    f"{path}.C_D",
                    "must be null when k_fail is 0",
                )
            if variant.get("concentration_label") != NO_FAILURES_LABEL:
                self.err(
                    "CD_ZERO_CONVENTION",
                    f"{path}.concentration_label",
                    f"must be {NO_FAILURES_LABEL!r} when k_fail is 0",
                )
            record["k"], record["c"] = 0, None
            return

        if variant.get("concentration_label") is not None:
            self.err(
                "CD_ZERO_CONVENTION",
                f"{path}.concentration_label",
                "must be null when k_fail > 0",
            )

        computed_c = Fraction(max(strata.values()), computed_k)
        declared_c = parse_rational(variant.get("C_D"))
        if declared_c is None:
            self.err(
                "CD_FORMAT",
                f"{path}.C_D",
                "required canonical rational string such as '1', '1/2' or '2/5'",
            )
        elif declared_c != computed_c:
            self.err(
                "CD_MISMATCH",
                f"{path}.C_D",
                f"declared {variant.get('C_D')!r} != recomputed {canonical_rational(computed_c)!r}",
            )
        record["k"], record["c"] = computed_k, computed_c

    # -- duplicate resolution (corrections A and B) ------------------------ #

    def resolve_duplicates(self):
        for record in self.records:
            if not record["realized"] and record.get("excluded"):
                self.excluded.append(self._exclusion(record, record["excluded"]))

        realized = [r for r in self.records if r["realized"]]
        for record in realized:
            pid = record["parent_id"]
            if pid not in self.parents:
                record["excluded"] = "PARENT_MISSING"
                record["realized"] = False
                self.excluded.append(self._exclusion(record, "PARENT_MISSING"))
            elif not self.parents[pid]["eligible"]:
                record["excluded"] = "PARENT_INELIGIBLE"
                record["realized"] = False
                self.excluded.append(self._exclusion(record, "PARENT_INELIGIBLE"))

        for record in self.records:
            if not record["realized"]:
                continue
            cell = record["cell_base"] + (record["k"],)
            record["cell_full"] = cell

        groups = {}
        for record in (r for r in self.records if r["realized"]):
            key = (record["parent_id"], record["cell_full"])
            groups.setdefault(key, []).append(record)

        for key, members in sorted(groups.items(), key=lambda item: canonical_json(list(item[0]))):
            members.sort(key=lambda r: r["id"])

            def collapse(field, reason, allow_cross=True):
                buckets = {}
                for record in members:
                    if record["alias_of"] is not None:
                        continue
                    digest = record["variant"].get(field)
                    if not isinstance(digest, str):
                        continue
                    buckets.setdefault(digest, []).append(record)
                for digest, bucket in sorted(buckets.items()):
                    if len(bucket) < 2:
                        continue
                    canonical = bucket[0]["id"]
                    for duplicate in bucket[1:]:
                        self.add_alias(duplicate, reason, canonical)

            # Correction A: coordinate duplicates include the settings.
            coordinates = {}
            for record in members:
                if record["alias_of"] is not None:
                    continue
                operator = self.parents[record["parent_id"]]["operator_class"]
                coordinate = (
                    operator,
                    record["variant"].get("site_ref"),
                    record["settings_key"],
                )
                coordinates.setdefault(coordinate, []).append(record)
            for coordinate, bucket in sorted(coordinates.items(), key=lambda i: canonical_json(list(i[0]))):
                if len(bucket) < 2:
                    continue
                canonical = bucket[0]["id"]
                for duplicate in bucket[1:]:
                    self.add_alias(duplicate, "DUP_OPERATION_COORDINATE", canonical)

            collapse("artifact_digest", "DUP_ARTIFACT_DIGEST")
            collapse("source_digest", "DUP_SOURCE_DIGEST")

        # Correction B: cross-parent collisions are a provenance event only.
        for field in ("artifact_digest", "source_digest"):
            owners = {}
            for record in (r for r in self.records if r["realized"]):
                digest = record["variant"].get(field)
                if isinstance(digest, str):
                    owners.setdefault(digest, []).append(record)
            for digest, bucket in sorted(owners.items()):
                parents = sorted({r["parent_id"] for r in bucket})
                if digest and len(parents) >= 2:
                    self.warn(
                        "CROSS_PARENT_DIGEST",
                        field,
                        f"digest shared by parents {parents}; provenance review required, "
                        "no automatic invalidation",
                    )

    @staticmethod
    def _exclusion(record, reason):
        return {
            "variant_id": record["id"],
            "reason": reason,
            "construction_status": record["variant"].get("construction_status"),
            "diagnostic_status": record["variant"].get("diagnostic_status"),
        }

    # -- M1-si support (corrections D and F) -------------------------------- #

    def compute_support(self):
        realized = [r for r in self.records if r["realized"] and r["alias_of"] is None]
        floor = self.limits.get("m1_si_min_qualifying_parents")
        floor = floor if is_int(floor) and floor > 0 else 3

        by_cell = {}
        for record in realized:
            by_cell.setdefault(record["cell_full"], {}).setdefault(
                record["parent_id"], []
            ).append(record)

        cells = []
        for cell, parents in by_cell.items():
            q, z, unresolved, k = cell
            parent_reports = []
            candidate_pairs = 0
            for pid in sorted(parents):
                variants = sorted(parents[pid], key=lambda r: r["id"])
                settings = {r["settings_key"] for r in variants}
                concentrations = {r["c"] for r in variants if r["c"] is not None}
                sources = {r["variant"].get("source_digest") for r in variants}
                artifacts = {r["variant"].get("artifact_digest") for r in variants}
                if len(settings) >= 2 and len(concentrations) >= 2:
                    candidate_pairs += 1
                witness = None
                if k is not None and k >= 2:
                    for first, second in combinations(variants, 2):
                        if first["c"] is None or second["c"] is None:
                            continue
                        if first["settings_key"] == second["settings_key"]:
                            continue
                        if first["c"] == second["c"]:
                            continue
                        if first["variant"].get("source_digest") == second["variant"].get("source_digest"):
                            continue
                        if first["variant"].get("artifact_digest") == second["variant"].get("artifact_digest"):
                            continue
                        witness = {
                            "variant_a": first["id"],
                            "variant_b": second["id"],
                            "settings_a": canonical_json(first["variant"].get("settings")),
                            "settings_b": canonical_json(second["variant"].get("settings")),
                            "C_D_a": canonical_rational(first["c"]),
                            "C_D_b": canonical_rational(second["c"]),
                        }
                        break
                parent_reports.append(
                    {
                        "parent_id": pid,
                        "variants": len(variants),
                        "distinct_settings": len(settings),
                        "distinct_C_D": len(concentrations),
                        "distinct_source_digests": len(sources),
                        "distinct_artifact_digests": len(artifacts),
                        "candidate_pair": len(settings) >= 2 and len(concentrations) >= 2,
                        "qualifying": witness is not None,
                        "pair_witness": witness,
                    }
                )
            qualifying = [p["parent_id"] for p in parent_reports if p["qualifying"]]
            cells.append(
                {
                    "cell": {
                        "q": q,
                        "Z": z,
                        "k_unresolved": unresolved,
                        "k_fail": k,
                    },
                    "variants": sum(p["variants"] for p in parent_reports),
                    "parents_present": len(parent_reports),
                    "qualifying_parents": len(qualifying),
                    "qualifying_parent_ids": qualifying,
                    "shortfall": max(0, floor - len(qualifying)),
                    "candidate_support_pairs": candidate_pairs,
                    "parents": parent_reports,
                }
            )

        cells.sort(key=lambda c: canonical_json(c["cell"]))
        best = max((c["qualifying_parents"] for c in cells), default=0)
        self.cells = cells
        self.counts = {
            "parents_total": len(self.parents),
            "parents_eligible": sum(1 for p in self.parents.values() if p["eligible"]),
            "variants_total": len(self.records),
            "variants_realized": sum(1 for r in self.records if r["realized"]),
            "variants_independent": sum(
                1 for r in self.records if r["realized"] and r["alias_of"] is None
            ),
            "variants_aliased": len({a["variant_id"] for a in self.aliases}),
            "exact_cells_with_realized_records": len(cells),
            "max_qualifying_parents_in_one_cell": best,
            "m1_si_min_qualifying_parents": floor,
        }
        self.m1_si = "REALIZED" if best >= floor else "NOT_REALIZED"

    # -- report ------------------------------------------------------------ #

    def report(self):
        errors = sorted(self.errors, key=lambda e: (e["code"], e["path"]))
        warnings = sorted(self.warnings, key=lambda e: (e["code"], e["path"]))
        valid = not errors
        return {
            "validator": {
                "name": "validate_manifest.py",
                "version": VERSION,
                **digest_file(Path(__file__).resolve()),
            },
            "inputs": {
                "manifest": self.sha["manifest"],
                "limits": self.sha["limits"],
                "schema": self.sha["schema"],
            },
            "decision": {
                "valid": valid,
                "m1_si": self.m1_si if valid else "NOT_ESTABLISHED",
                "structural_lopo_support": (
                    "structural only: M1-si support does not guarantee optimizer "
                    "convergence, successful model fitting, or an available B1 test"
                ),
            },
            "errors": errors,
            "warnings": warnings,
            "counts": self.counts,
            "aliases": sorted(self.aliases, key=lambda a: a["variant_id"]),
            "excluded": sorted(self.excluded, key=lambda e: e["variant_id"]),
            "cells": self.cells,
        }


# --------------------------------------------------------------------------- #
# entry point
# --------------------------------------------------------------------------- #

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc


def run(manifest_path: Path, limits_path: Path, schema_path=None):
    manifest_digest = digest_file(manifest_path)
    limits_digest = digest_file(limits_path)
    schema_digest = digest_file(schema_path) if schema_path and schema_path.exists() else None
    validator = Validator(
        load_json(manifest_path),
        load_json(limits_path),
        manifest_digest,
        limits_digest,
        schema_digest,
    )
    try:
        validator.check_limits()
        validator.check_manifest_top()
        validator.check_parents()
        validator.check_variants()
        validator.resolve_duplicates()
        validator.compute_support()
    except Exception as exc:  # never crash on malformed input
        validator.err("INTERNAL_ERROR", "$", f"{type(exc).__name__}: {exc}")
        validator.m1_si = "NOT_ESTABLISHED"
    return validator.report()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Deterministic population-manifest validator (M1-si structural support)."
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--limits", required=True, type=Path)
    parser.add_argument("--schema", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)

    for path in (args.manifest, args.limits):
        if not path.is_file():
            print(f"error: file not found: {path}", file=sys.stderr)
            return 2

    try:
        report = run(args.manifest, args.limits, args.schema)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    text = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0 if report["decision"]["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
