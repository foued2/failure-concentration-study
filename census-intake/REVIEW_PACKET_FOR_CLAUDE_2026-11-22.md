# Independent code review requested — B1 census intake prototype

**Date:** 2026-11-22
**Artifact under review:** commit `0060e7b413b709f7ff66f7d9f89780fa2b1a1703`, branch
`work/b1-census-intake-validator-2026-11-22`. Not merged. No PR exists for this branch.
**Reviewer:** Claude. **Requested output:** an explicit **PASS** or **NOT PASS**.
**Status:** held. No correction will be implemented, and no real record will be admitted, before that verdict.

## 1. What the artifact is

A standard-library Python validator and 18 synthetic tests for a per-variant diagnostic record
format, plus a descriptive JSON Schema and a one-line root README index entry. It was produced under
the owner's step-1 authorization (validator plus synthetic tests only).

The author's own `AUTHORIZATION_AND_RESULT_2026-11-22.md` reports 18/18 synthetic tests passing. GPT
inspected the tests but did not independently reproduce the run. The local agent re-ran them during
review preparation and observed 18/18 passing; this is a software fact about synthetic fixtures only.

## 2. Findings raised by GPT, with local fact-check

### Finding 1 — prohibited measurement basis is admitted as primary

**Claim.** The validator accepts `exposure_basis = "canonical"` (60 records; four in D6) as an
admissible primary basis, and a passing test covers it. The reviewed B1 census instrument fixes
`measurement_basis = record_level_64` and forbids substituting the canonical basis.

**Local check: CONFIRMED.** `validate_records.py:24` defines both bases; `:145–148` accepts either;
`tests/test_b1_census_intake.py::test_valid_canonical_basis_admitted` asserts admission. Register
§15.5 confirms the protocol-prescribed primary statistic is record-level, with canonical explicitly
a recomputed sensitivity that must not be silently substituted.

**Question for Claude.** Is the correct remedy to remove `canonical` from the primary intake path
entirely, or to retain it only behind an explicit `sensitivity_only` field with a distinct admission
decision? State which, and whether the existing canonical test should be deleted or rewritten.

### Finding 2 — aggregates are validated, individual diagnostic results are not

**Claim.** The frozen B1 structure requires 64 individual diagnostic results per variant, each with a
diagnostic record ID, a D1–D8 stratum, and a terminal status of `DEFINITE_PASS`, `DEFINITE_FAILURE`
or `UNRESOLVED`. The prototype accepts supplied `f`/`u` vectors plus arrays of record IDs and never
inspects per-record terminal status, so it cannot verify that the counts were derived from the records.
A record with all eight IDs per stratum and zero failures/unresolved is admitted without evidence
that the underlying results were definite passes.

**Local check: CONFIRMED.** `validate_records.py:154–161` validates supplied vectors; `:157–181`
checks ID arrays for shape, count and duplication. No terminal-status field exists anywhere in the
record contract or schema.

**Question for Claude.** Can this be retained as a thin preliminary adapter that derives `f`/`u` from
a per-result list, or must it be reshaped around the actual B1 `diagnostic_record_results` structure?
Give the required record shape and derivation rule if the latter.

### Finding 3 — provenance check is syntactic only

**Claim.** `source_digest` is checked only for a 64-character lowercase hex string. The validator does
not verify it against an actual diagnostic source artifact, nor that the supplied record IDs belong
to the frozen diagnostic bank, nor that the vectors correspond to referenced evidence.

**Local check: CONFIRMED.** `validate_records.py:150–152` applies only a regex. No bank or artifact is
read, consistent with the no-bank-access authorization.

**Question for Claude.** Given that bank access is not authorized in step 1, what is the maximum
honest provenance guarantee this tool can make, and how must its output be labelled so that a
syntactically valid hash is never presented as provenance verification?

### Finding 4 — two untested input-handling defects

**Claim (a).** An empty JSON array is admitted with zero rejected records and the CLI exits 0.
**Local check: CONFIRMED.** `validate_manifest([])` returns `count=0, rejected=0`; `main()` returns 0.
No test covers the empty manifest.

**Claim (b).** An `exposure_basis` supplied as an array or object raises an uncaught `TypeError`.
**Local check: CONFIRMED.** Reproduction:

```
py -c "import sys; sys.path.insert(0,'census-intake'); import validate_records as v; v.validate_manifest([{'exposure_basis':['record']}])"
TypeError: cannot use 'list' as a dict key
```

Cause: `validate_records.py:146` tests `basis not in CAPACITY` before any type check. No test covers
a non-string basis.

**Question for Claude.** Confirm the required controlled rejection behaviour and reason codes for
both cases, and specify the adversarial tests to be added.

## 3. What the 18 tests do not establish

- Compatibility with the complete B1 v1.7 / reviewed census manifest schema.
- Handling of 64 individual terminal results.
- Consistency between supplied counts and underlying diagnostic evidence.
- Parent-family and mutation-registry consistency.
- Full diagnostic-bank provenance.
- LOPO eligibility or census coverage.

The artifact should therefore be described, until reviewed, as a **synthetic-tested summary-record
intake prototype**, not the B1 semantic validator specified in revision 0.6.

## 4. Required verdict

Claude must return one of:

- **PASS** — the implementation may be retained as a small preliminary adapter, with a named list of
  changes required before it may be relied on; or
- **NOT PASS** — it must be reshaped around the actual B1 `diagnostic_record_results` structure,
  with the required shape and derivation rule stated.

The verdict should address each of the four findings separately. It is a code review, not a
scientific result, not a census decision, and not an authorization to implement.

## 5. Governance note

GPT's instruction is explicit: preserve the branch, do not merge it, do not run it on real records,
and implement no correction before Claude's agreement. The local agent has complied: no code change
was made after the review findings were received; this packet and the dated record entry are the
only additions. No bank access, solver work, diagnostics, or census activity occurred.

---

## 6. Dated correction to the 4(b) reproduction — 2026-11-22

**This section appends to the original review; it does not rewrite it.** The 4(b) reproduction in §2 was
incomplete as stated, and the distinction matters for the corrected implementation.

The local agent re-executed the old prototype (`639ee3f`) against the exact cases:

| Input to the old prototype | Observed result |
|---|---|
| Minimal object with only `exposure_basis` as a list | `MISSING_FIELD`, `MISSING_UNRESOLVED_VECTOR` — the basis check was never reached |
| Complete record with `exposure_basis` as a **list** | `TypeError: cannot use 'list' as a dict key` |
| Complete record with `exposure_basis` as a **dictionary** | `TypeError: cannot use 'dict' as a dict key` |
| Complete record with `exposure_basis` as a **number**, **Boolean** or **null** | Controlled `INVALID_EXPOSURE_BASIS` rejection (no exception) |

So the original claim was directionally right but over-broad: the uncaught `TypeError` requires a
complete record and applies specifically to unhashable types (list, dictionary). Number, Boolean and
null take a different, already-controlled path. The original minimal reproduction could not reach the
basis check because required fields were absent.

This correction was reproduced before the successor implementation was written. The successor checks
`isinstance(basis, str)` before any dictionary lookup, so all five non-string types produce the
controlled reason `NON_STRING_EXPOSURE_BASIS`, and tests cover each type separately.
