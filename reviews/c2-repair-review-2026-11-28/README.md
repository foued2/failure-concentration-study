# LC518 C2 repair review packet

**Preservation branch:** `preserve/lc518-c2-repair-packet-2026-11-28`  
**Base commit:** `24e973fc8517d5467807446f915841896b65f8a4`  
**Status:** Draft review artifacts only. Not a canonical protocol, not adopted, and not production authorization.

This branch preserves the four source artifacts individually. It does not alter `master`, rewrite either historical record, or modify the local PyCharm checkout.

The previously assembled ZIP was not included in this branch because byte-for-byte identity of the binary transfer to GitHub could not be established. Its four constituent source files are preserved individually here. The locally retained ZIP passed its own integrity test and remains available as a session download, but is not represented as a GitHub artifact.

| File | SHA-256 of exact local bytes |
|---|---|
| LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28.md | `3264abb45b2f15498064fcf071507caa8bb5e9853390b95c5f4e3b48a9759631` |
| LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28.md | `3d53d06ec9ad2c2998814995c328f3ff5fead8e32a3c38985c83343d79846806` |
| LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28.md | `b27b67ce7125e016cd8c29247b8718bd8369b494f39d7554d03d86286c5a0b2a` |
| verify_lc518_c2_v07_vectors.py | `c9cca1cee8f99222118c096aea6a370c99df6a2bf19b9970fafd05ace7e43950` |

The vector script was executed locally on 2026-11-28 and reported seven passing checks. It does not fetch drand, verify a beacon, or perform a production selection. All four source files in this branch preserve their final newline and their Git blob SHA-1 identities match the original local files.
