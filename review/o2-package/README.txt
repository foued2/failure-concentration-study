O2 review package rev 2 -- TEMPORARY reviewer-access copy (pre-freeze).
Owner-authorized temporary push (2026-10-17) so GPT/CLAUDE can review the
exact bytes. This branch is a transfer vehicle, NOT part of the study
record, NOT a publication of Revision G, and NOT an adoption of the O2
numbers, which remain provisional pending reviewer sign-off.

Rev 2 corrections per GPT's source review of rev 1 (ae4eca2):
  - V0: the FTABLE check is now a genuine exact comparison of the S1-m4
    k=5/k=10 arrays actually used against A.FTABLE (rev 1 hardcoded True);
  - the four N=16/20 direct-vs-RS checks are labelled VACUOUS with the
    reason (test block 4/5 < 8 => complete event mass identically zero),
    not presented as agreement evidence; N=32 is the first informative
    small-N comparison;
  - check counts reconciled: 56 records = 52 PASS + 4 VACUOUS + 0 FAIL
    (rev 1 README said 89; the JSON has always had 56 records).
Machine counts are in o2_results.json (meta.checks_*) and in the report.
Probabilities are unchanged from rev 1; this is a validation-record fix.

Contents:
  o2_calc.py        -- exact calculation script (stdlib only, deterministic)
  o2_results.json   -- machine output of the validated run (rev 2)
  o2_report.md      -- human-readable summary of the same run
  o2_review.zip     -- zip of the three files above (primary download)
  MANIFEST.sha256   -- SHA-256 of the stored bytes (see hash list)
  .gitattributes    -- '* -text': pins exact bytes against autocrlf

Provenance: local temporary working copy
  C:\Users\pakla\AppData\Local\Temp\opencode\o2_calc\
  validated run 2026-10-17T13:18:25Z (rev 2), CPython 3.14.0 (pinned
  .venv), 39.5 s, 56 check records: 52 PASS + 4 VACUOUS + 0 FAIL.
  Main route: independent train/test compositions; validators: direct
  hypergeometric enumeration (N=16/20/32) and A1 joint2 h-table route
  (N=113). Auxiliary debugging probes (diag.py, diag2.py, diag3.py,
  fullprec.py) remain in the local temp dir and are not pushed.

Dependency: imports v03p/a1/a1_support_comparison.py (A1 rev 3, f69cc9b)
read-only via an absolute path (A1DIR); NOT self-contained or portable.

Status/boundaries: numbers provisional; P_atleastone primary, P_each
sensitivity; no matrix-conditioning claim; 3-bucket scenarios excluded;
RevF text unedited; Stage 1 freeze not occurred; Phase 1 NOT AUTHORIZED.
