O2 review package -- TEMPORARY reviewer-access copy (pre-freeze).
Owner-authorized temporary push (2026-10-17) so GPT/CLAUDE can review the
exact bytes. This branch is a transfer vehicle, NOT part of the study
record, NOT a publication of Revision G, and NOT an adoption of the O2
numbers, which remain provisional pending reviewer sign-off.

Contents:
  o2_calc.py        -- exact calculation script (stdlib only, deterministic)
  o2_results.json   -- machine output of the validated run (all checks PASS)
  o2_report.md      -- human-readable summary of the same run
  o2_review.zip     -- zip of the three files above (primary download)
  MANIFEST.sha256   -- SHA-256 of the stored bytes (see hash list)
  .gitattributes    -- '* -text': pins exact bytes against autocrlf

Provenance: local temporary working copy
  C:\Users\pakla\AppData\Local\Temp\opencode\o2_calc\
  validated run 2026-10-17T12:16:57Z, CPython 3.14.0 (pinned .venv),
  39.3 s, 89 checks, FAILURES: none. Main route: independent train/test
  compositions; validators: direct hypergeometric enumeration (N=16/20/32)
  and A1 joint2 h-table route (N=113). Auxiliary debugging probes
  (diag.py, diag2.py, diag3.py, fullprec.py) remain in the local temp dir
  and are not pushed.

Status/boundaries: numbers provisional; P_atleastone primary, P_each
sensitivity; no matrix-conditioning claim; 3-bucket scenarios excluded;
RevF text unedited; Stage 1 freeze not occurred; Phase 1 NOT AUTHORIZED.
