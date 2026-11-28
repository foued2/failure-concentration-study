# Uploaded Archive Verification Report

**Disposition:** Evidence report. The uploaded preservation bundle was verified; its Git history is now retained in repository refs. The ZIP-labelled upload is committed only as quarantined corrupt evidence. No archive is silently repaired or rewritten.

## 1. Preservation Git bundle and repository-native retention

Input: `LC518_C2_PRESERVATION_HISTORY_2026-11-28.bundle`

- Size: 475,220 bytes
- SHA-256: `df16563f0244ba1e5231d0c40504a2dc2abefd397e455f99f01162819fc5665e`
- Git blob SHA-1: `570dbd11f4ebb1591d855b8c27505e59118efc33`
- `git bundle verify`: PASS, complete history
- Refs in uploaded bundle: six

The bundle's six refs identified commits:
- `0e6c47b26959019cafc6e11eb04e5f7e19a037dd`
- `24e973fc8517d5467807446f915841896b65f8a4`
- `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`
- `6f4b6975dd956ea3303653aa3ac8f7a27be31646`
- `a0f1ba90b92457bfaa43c3ec68c754578243cb0e`
- `e0cddeacc7ea3ff17477708ec3470f71c8ee476b`

The repository now retains these commit lineages through two branches:

- `archive/lc518-c2-superseded-history-2026-11-28` points to `e0cddeacc7ea3ff17477708ec3470f71c8ee476b`, preserving its ancestry through `0e6c47b`, `a0f1ba9`, and base `24e973f`.
- `preserve/lc518-c2-repair-packet-2026-11-28` remains at `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`, whose ancestry includes `6f4b697` and `24e973f`.

Verified parent relationships:
- `a0f1ba9...` parent `24e973f...`;
- `0e6c47b...` parent `a0f1ba9...`;
- `e0cddea...` parent `0e6c47b...`;
- `6f4b697...` parent `24e973f...`;
- `4ab5ce1...` parent `6f4b697...`.

Exactly three commits were superseded: `a0f1ba9...`, `0e6c47b...`, and `e0cddea...`. The bundle's six commit lineages are therefore retained in the repository, although the original 475,220-byte bundle container itself is not duplicated as a `.bundle` file. The branches preserve Git objects and ancestry, not missing GitHub Activity records.

## 2. ZIP-labelled raw upload

Input: `LC518_C2_REPAIR_REVIEW_PACKET_2026-11-28__GITHUB_BLOB_b5998912.zip`

- Size: 13,698 bytes
- SHA-256: `52792b86a7b8f7e656302db477a09ffbb915d3d42f2a38341d1c818c96443189`
- Git blob SHA-1: `b5998912ff9fcee8584ada76ebd370128ba8f6b2`
- Python standard-library ZIP reader: FAIL
- `unzip -t`: FAIL
- Failure: end-of-central-directory record not found; no central-directory entries can be enumerated.

The exact raw bytes are committed at:

`evidence/LC518_C2_REPAIR_REVIEW_PACKET_2026-11-28__GITHUB_BLOB_b5998912_CORRUPT.zip`

This path is quarantine only. Do not use it as a ZIP archive. No repair or recompression has been performed. A previous assistant statement that the first two entries decompressed is withdrawn because this could not be reproduced from the exact uploaded bytes. Claude independently classified the extracted blob as corrupt and noted the absent central directory.

## 3. Preservation and evidence boundary

- Master remains `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a`.
- Preservation branch remains `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`.
- Review branch receives the consolidated Revision 4 review packet only.
- Archive branch retains the superseded commit chain.

Activity coverage after the reported 07:03:30Z force-push remains outstanding because later Activity reads returned HTTP 403 rate-limit responses. The `2026-11-28T07:54:01Z` commit metadata timestamp is not an Activity event time. This report does not authenticate historical TLS responses or substitute for the raw Activity ledger.