# LC518 C2 v0.7 package integrity reconciliation

Date: 2026-11-27

## Published transfer archive

A new deterministic transfer ZIP has been assembled from the exact UTF-8 file contents fetched from branch `review/lc518-c2-v07-corrected-2026-11-27` at source commit `474975a9c27228a5374a4edf82237ae73acfed1f`. It is a new archive, not a claim that the earlier local ZIP has been recovered byte-for-byte.

- Repository path: `LC518_C2_V07_CORRECTED_REVIEW_TRANSFER_2026-11-27.zip`
- SHA-256: `dd8d6948b93fc5311edb8db1c969461d99230523bc87ae88f7f97fc545c1fe14`
- Size: 27920 bytes
- ZIP method: stored (no compression)
- ZIP timestamp: 2026-11-27 12:00:00 (fixed for reproducibility)
- Contents: the approved v0.7 protocol, the review handoff, the provenance correction, the protocol SHA-256 sidecar, and `MANIFEST.sha256`

The manifest covers each of the four component files; it does not attempt to hash itself or the containing ZIP. The ZIP's own SHA-256 is recorded in the adjacent repository-root sidecar.

## Earlier local-archive checksum reconciliation

The earlier local archive was not present in GitHub and could not be rehashed by a reviewer from the repository. Its earlier local checksum was recorded as `04f3c110080750905bef7610e0ece85b903c48dbaa244e0ca086fe9019c38f72`. A conflicting `cf25d0cbfe7413771f795da00c0e8fc6a3da319fd95c921dac7aec44f8a07b7f` value was reported later and is withdrawn as a reporting error. Neither value is the checksum of this newly assembled ZIP.

The new archive hash above supersedes the old local-archive hash for repository transfer and verification. The original local ZIP remains a separate historical artifact and is not represented as uploaded.

## Sidecar path correction

The repository-root protocol sidecar now names the actual tracked path, `reviews/LC518_R2_C2_SELECTION_PROTOCOL_v0.7_2026-11-27.md`, so `sha256sum -c LC518_R2_C2_SELECTION_PROTOCOL_v0.7_2026-11-27.md.sha256` from the repository root checks the approved protocol. Inside the transfer ZIP, the protocol and its sidecar are both at the archive root, so the embedded sidecar uses the basename.

## Scope

This is a packaging and integrity correction only. The approved protocol bytes are unchanged at SHA-256 `05f432c1d6caa5eefcf4f8c0d76954aa769e04d1f10f72473daa832855485f3c`. Claude's scoped technical PASS remains limited to the documentary corrections already reviewed. This record does not constitute owner adoption, a prospective lock, a production draw authorization, pair selection, R2 adoption, or authorization for construction or solver execution.
