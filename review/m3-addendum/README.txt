M3 specification addendum - provisional review package
=======================================================

Status: PROVISIONAL; NOT FROZEN. This package is not part of the O2 package and does
not alter Revision F. No complete-rule probability is computed or authorized by it, and
no Phase 1 activity is authorized. Owner decisions on the addendum's open items
(section 9) remain pending; this package does not settle them.

Review state: Rev a (draft) -> Rev b, Rev c (GPT corrections) -> Rev d (annotation of
the GPT disposition and follow-up). GPT provisionally accepted the specification
mathematically and confirmed no further mathematical objection; the condition-number
threshold must not be frozen as a scientific eligibility gate.

Contents:
- M3_SPEC_ADDENDUM_DRAFT_2026-10-17.md
    The reviewed M3 conditioning specification addendum, Rev d. Preserved
    byte-for-byte from its source file; line endings enforced by this folder's
    .gitattributes (* -text).
- supporting/m3_cond_probe.py, supporting/m3_cond_results.json
    The exact stdlib-only probe and its results, cited in the addendum header as its
    basis. Evidence only; not a reviewed specification.
- MANIFEST.sha256
    SHA-256 of every file in this folder except the manifest itself.

Provenance: the addendum was authored and revised by the implementation agent (GLM)
in a local temporary folder on 2026-10-17; this commit is the first durable,
versioned repository reference for it, created on the owner's direction to unblock
Revision G v3 publication. Templates follow the review/o2-package conventions.
