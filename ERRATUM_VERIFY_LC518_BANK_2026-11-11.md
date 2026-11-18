# ERRATUM — `verify_lc518_bank.py` stale oracle-count label ("140")

**Date:** 2026-11-11
**Type:** documented correction (label only). The original verification package is **not altered** — it remains a digest-pinned trust anchor and must never be edited in place.
**Raised by:** GPT (2026-11-11): "The stale `140` label should receive a documented correction. Do not silently alter the original digest-pinned verification package."
**Prepared by:** audit session (Claude-side), who identified and diagnosed the defect on 2026-11-11.

## 1. The defect

In `verify_lc518_bank.py` (Section 3, semantic oracle recompute), the combined oracle check is written:

```python
check("oracle: every answer == independently computed UNBOUNDED LC518 DP (140 entries)",
      not oracle_bad_ans, str(oracle_bad_ans[:5]))
```

The string `"(140 entries)"` is a hard-coded label. The loop above it iterates over all bank records (64 diagnostic + 80 held-out = 144) and resolves each record's canonical to its oracle entry; every record has one, so all 144 records are verified against the **138** distinct oracle entries:

- `bank/diagnostic_oracle_outputs.json`: **60** entries (== 60 unique diagnostic canonicals; 4 duplicate-canonical groups, all size 2)
- `bank/heldout_oracle_outputs.json`: **78** entries (== 78 unique held-out canonicals; 2 duplicate-canonical groups, all size 2)

`140` matches no count that exists in the artifact or the check: not 144 records, not 138 entries, not 138 unique answers. It is a stale label, almost certainly left over from an earlier draft bank size. The check itself is correct and passed.

## 2. Propagation of the wrong figure

The stale label propagates verbatim to two places (byte-identical artifacts of the same run):

1. `lc518-verification-ledger-41591572358.txt` — the PASS line "oracle: every answer == independently computed UNBOUNDED LC518 DP (140 entries)".
2. `MANIFEST.txt` line 57 — "All 140 oracle answers equal an independently implemented unbounded LC518 combination-count DP…".

**Correct statement:** *All 138 oracle answers (covering all 144 bank records, 64 diagnostic + 80 held-out) equal an independently computed unbounded LC518 combination-count DP.*

## 3. Package identity (so this erratum is checkable against the unmodified package)

| Object | SHA-256 |
|---|---|
| `lc518-verification-inputs-41591572358.zip` (outer bundle) | `08c2b121f5cbc50c18d15509b6df1fa4346b1359d73c4381443f9c55395e87b6` |
| `verify_lc518_bank.py` | `cd6fbd54ad0f7eaeed65c0c84e53c052b265fc08a6bc77985174959376b860b8` |
| `lc518-verification-ledger-41591572358.txt` | `41239c3cbd4052db1caec6c79b677a1906d9991cc0b2e2082e6beb52a2b94a73` |
| embedded `zips/lc518-bank-run-41591572358-1.zip` | `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` (== GitHub artifact digest `13210063805`) |
| embedded `zips/lc518-bank-outputs-41591572358.zip` | `d9ec6dee5b16070c95fdd6db13e2b0a3460d98395ac63af234a38e28dcbd92f4` |

Anyone holding the package can re-hash it, confirm these values, reproduce the byte-identical ledger, and see the `140` label in context.

## 4. Independent re-execution record

2026-11-11, CPython 3.13.5 (`uv run --python 3.13.5 --no-project`), fresh unpack of the embedded bank-run ZIP: **91/91 PASS, 0 FAIL, exit 0**, output byte-identical line-for-line to the shipped ledger. Bank-outputs ZIP verified 7/7 bank files byte-identical to the original artifact.

## 5. Disposition

- The original package stays untouched; this file is the documented correction.
- If the verifying agent later issues a revised script, it must be a **new package with new hashes** (corrected label, e.g. "(138 oracle entries / 144 records)"), accompanied by its own manifest — never an in-place edit of the digest-pinned original.
- Downstream readers should cite **138** (not 140) as the oracle-row count everywhere, including in the GLM/Qoder `CLAIM_AUDIT_MATRIX_2026-11-05.csv` if that figure appears there.
- Historical note: the earlier DeepSeek "140 oracle answers" wording matches this stale label, not the bank data; GPT's correction to 138 was correct.

---

## 6. Addendum — precision corrections (2026-11-12, Claude independent review)

Claude's review of this erratum raised two precision points, both confirmed against the script bytes (`verify_lc518_bank.py`, Section 3, verified 2026-11-12):

1. **The loop checks 144 records against 138 unique oracle entries.** Section 1 above says "every record has [an oracle entry]" — true for this artifact, but the loop's actual semantics matter for future use: a record whose canonical has **no** oracle entry is **skipped silently** (`if e is None: continue`), so the combined answer check alone does not prove coverage. Full coverage in this artifact is established only jointly with the separate checks "oracle entries == unique canonicals (60 / 78)" and "oracle canonical set == bank canonical set" (both PASS). Any future revision of the script should make the coverage dependence explicit.
2. **Corrected wording (supersedes the bolded line in §1 and the phrase in §5):**

   > *All 144 bank records (64 diagnostic + 80 held-out) were checked against the 138 unique oracle entries — duplicate-canonical records resolve to the same entry — and every checked answer matches an independently computed unbounded LC518 combination-count DP. Full coverage is guaranteed by the separately checked canonical-set equality, not by the answer loop itself.*

3. The characterization "the code verifies the 138 oracle rows" (used in `B1_DECISION_RECONCILIATION_2026-11-11.md` §6.3) is corrected by the same wording; a cross-reference addendum is recorded there.

No changes to the pinned package; this addendum is part of the documented correction.
