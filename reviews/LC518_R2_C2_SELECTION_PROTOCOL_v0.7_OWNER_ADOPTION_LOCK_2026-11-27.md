# LC518 R2 C2 protocol v0.7 owner adoption and lock attempt

**Disposition: VOID FOR PRODUCTION USE. THE REQUIRED PRE-TARGET RECORDING CONDITION WAS NOT MET. NO PRODUCTION DRAW IS AUTHORIZED.**

This record preserves the attempted owner adoption and the reason it did not create a valid production lock. It supersedes the operative effect claimed by the original version of this file, without deleting or rewriting its Git history.

## Exact protocol and review

- Protocol: `LC518_R2_C2_SELECTION_PROTOCOL_v0.7_2026-11-27.md`
- Exact protocol SHA-256: `05f432c1d6caa5eefcf4c8d0d76954aa769e04d1f10f72473daa832855485f3c`
- Claude scoped technical review: **PASS**, for the documentary corrections reviewed.
- Package integrity: the published transfer archive and checksum sidecars passed GitHub read-back verification.
- Owner instruction: on 2026-11-27, the owner instructed GPT to proceed if GPT and Claude agreed. GPT treated this as owner adoption authority because the stated condition was met.

## Attempted timestamp and failed timing condition

- Trusted current-time source timestamp entered in the attempted record: `2026-11-27T16:41:47Z` (Unix time `1795797707`).
- Pinned Quicknet genesis time: `1692803367`.
- Pinned Quicknet period: `3` seconds.
- Under v0.7 §7, the first scheduled round strictly after that timestamp is round `34331448`, scheduled at `2026-11-27T16:41:48Z` (Unix time `1795797708`).
- GitHub's server-side creation time for the attempted adoption commit `8cfa2bbfa90d868b12958e0b09ea8a5c3360d58e` is `2026-11-27T16:41:59Z`.

The adoption record was therefore committed **11 seconds after** the target round's scheduled time. The protocol requires the lock event to be recorded before that scheduled time. The condition was not satisfied. A timestamp written into the record does not override the later server-side recording time.

## Operative disposition

1. The attempted adoption/lock is void for the production selection.
2. Round `34331448` must not be queried or used for this selection.
3. No production beacon was queried, no seed was derived, and no pair was selected.
4. No alternative round may be substituted under this attempted lock.
5. The original attempted record and commit remain preserved as historical audit evidence.
6. A new adoption/lock attempt requires resolving the timing race in the protocol and receiving the necessary scoped technical review before a new exact-hash owner lock.

## Scope unchanged

Original R2 repeat-pair C2 remains **NOT ESTABLISHED**. This attempted adoption does not adopt R2, accept a new allocation, amend Rev11, authorize parent-source or solver construction, authorize solver execution, or support a scientific claim. Round `34323983` remains permanently excluded.
