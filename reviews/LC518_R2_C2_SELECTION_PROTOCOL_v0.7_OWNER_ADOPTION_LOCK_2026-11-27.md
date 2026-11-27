# LC518 R2 C2 protocol v0.7 owner adoption and lock

**Disposition: ADOPTED AND LOCKED FOR ONE PRODUCTION SELECTION ONLY.**

- Protocol: `LC518_R2_C2_SELECTION_PROTOCOL_v0.7_2026-11-27.md`
- Exact protocol SHA-256: `05f432c1d6caa5eefcf4c8d0d76954aa769e04d1f10f72473daa832855485f3c`
- Protocol review: Claude scoped technical **PASS** on the documentary corrections.
- Package integrity: published transfer archive and checksum sidecars verified by GitHub read-back.
- Owner authorization: explicit instruction in the project conversation on 2026-11-27: “IF YOU TO AND CLAUDE AGREE THEN PROCEED AND FINISH”. This is treated as the owner's adoption decision because the stated condition was met.
- Whole-second UTC lock timestamp from the trusted current-time source: **2026-11-27T16:41:47Z**.

## Effect of this adoption and lock

This adoption locks the exact protocol identified above and authorizes exactly one production selection of the two distinct repeated mechanism pairs, using the target-round rule in protocol §7.

The target is the smallest integer round (r \geq 1) for which:

`genesisTime + period × (r − 1) > 1795797707`

where `1795797707` is the Unix-second value of the lock timestamp above, and the pinned Quicknet genesis time and period remain those stated in the protocol. No person may choose a different round.

The production selection must obtain the target round from both pinned relay origins, validate both signatures with the pinned native drand client and pinned chain identity, and require exact relay agreement before deriving the seed. Any failure aborts the one selection. No alternative round, retry with another round, reroll, or manual substitution is permitted.

## Explicit limits

This adoption does not establish original R2 C2 compliance, adopt R2, accept a new allocation, amend Rev11, authorize parent-source or solver construction, authorize solver execution, or support a scientific claim. Original R2 repeat-pair C2 remains NOT ESTABLISHED. Round `34323983` remains permanently excluded.

Any new allocation built from the selected pairs requires its own documented checks and Claude review before owner adoption. All downstream execution gates remain in force.
