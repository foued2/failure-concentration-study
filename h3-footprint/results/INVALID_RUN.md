# INVALID_RUN

The verdict in `REPORT.md` and `footprint.json` in this directory was produced by the frozen gate, but it is
**invalid and uninterpretable** because the frozen `generate.py:extract()` dropped module-level imports from
candidate bodies.

Do not treat `FAIL (degeneracy)` as an H3 finding. See `../INVALID_RUN_2026-10-27.md` and
`../audit/extractor_defect.json`.
