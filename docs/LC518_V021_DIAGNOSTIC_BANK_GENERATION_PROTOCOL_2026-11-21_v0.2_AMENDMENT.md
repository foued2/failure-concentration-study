# LC518 v0.21 diagnostic-bank generation protocol
## v0.2 amendment: eligible-set selector, identity invariants and external preflight

**Document ID:** LC518-V021-DIAG-GEN-PROTOCOL-2026-11-21  
**Version:** 0.2 amendment to v0.1  
**Date:** 2026-11-21  
**Status:** DRAFT FOR INDEPENDENT REVIEW; DESIGN-ONLY; NOT FROZEN; NO GENERATION OR EXECUTION GO  
**Base protocol:** v0.1, exact blob 96e454b4bb0b1582635d47e89358a7feee021512  
**Governing taxonomy:** v0.21 operational diagnostic-strata specification v0.4, exact blob 8873389a0b38a7c9a1307f1c4f9fe4f7dee13def  
**Owner acceptance record:** docs/LC518_V021_V04_OWNER_ACCEPTANCE_2026-11-21.md, exact blob 472b7f1f94ee6fa1792f3f833a5418a77e93e9e9  
**Design purpose:** Resolve Claude's three v0.1 implementation-logic challenges without creating candidates, a bank, a manifest, or generator code.

---

## 1. Authority and precedence

This document is a controlled amendment to v0.1. It is to be read together with the exact v0.1 blob identified above. It does not amend owner-accepted v0.4, accepted B1 v1.7, or accepted Rev 1.4.

The following v0.1 sections are superseded in full by this amendment:

| v0.1 section | v0.2 disposition |
|---|---|
| §2.3 Slot-order convention | Replaced by §2 below |
| §4.3 Simultaneous identity and collision proof | Retained as a mathematical proof, with the executable selector and mandatory runtime checks added in §3 |
| §4.4 What this proof does not establish | Supplemented by §3.5 |
| §6.1 Attempt unit and slot accounting | Replaced by §4.1 |
| §6.2 Rejection reason codes | Replaced by §4.2 |
| §6.3 Retry policy | Replaced by §4.3 |
| §6.4 Rejection sidecar | Replaced by §4.4 |
| §9 B1 and protected-evaluation hard stop | Replaced by §5 |
| §10 Freeze sequence | Replaced by §6 |
| §11 Unresolved decisions | Supplemented by §7 |
| §12 Current disposition | Replaced by §8 |

All v0.1 provisions not listed above remain unchanged. If any wording in v0.1 conflicts with this amendment, v0.2 controls for the sections identified in the table. The accepted v0.4 predicates and domain conditions always control over either protocol draft.

This amendment addresses only construction logic. It does not authorize selector execution, candidate enumeration, candidate-list creation, bank generation, oracle generation, manifest creation, protected-data access, solver work, or any other experimental activity. The project pause remains in force.

## 2. Slot order and finite eligible-set selector

### 2.1 Slot order

The slot sequence is fixed for this proposal as D1, D2, D3, D4, D5, D6, D7, D8, with slots within each stratum numbered in ascending order. D6 has four pair slots, each producing members A and B:

- D1-01 through D1-08
- D2-01 through D2-08
- D3-01 through D3-08
- D4-01 through D4-08
- D5-01 through D5-08
- D6-P01 through D6-P04, each with members A and B
- D7-01 through D7-08
- D8-01 through D8-08

D6 member A is the denomination tuple in ascending order. Member B is the exact reverse of member A. Both have the same amount and canonical identity. The reverse is non-identity because every D6 input has at least 11 distinct denominations.

### 2.2 Eligible sets are enumerated before selection

The selector does not draw arbitrary inputs from a broad domain and reject most of them. For each stratum, it first defines a finite, ordered eligible parameter set using only the v0.4 predicates and the constructions below. A selector may choose only members of that set. It must never propose an out-of-set candidate and rely on a rejection loop to reach the quota.

All integer sets below are ordered in ascending numeric order. The eligible-set definition, cardinality, amount-to-input construction, and selection rule are fixed in this amendment. They are not inferred from a seed or from solver outcomes.

| Stratum | Eligible parameter set | Cardinality | Selection |
|---|---|---:|---|
| D1 | Fixed target list {0, 1, 2, 4, 5, 7, 8, 10}, with C={3,11} | 8 | Use all eight, once each |
| D2 | Amount a in [2,1500], with C={a} | 1499 | Select 8 distinct amounts without replacement |
| D3 | Fixed amount list {2,3,4,5,6,7,8,9}, with C={a,10,11} | 8 | Use all eight, once each |
| D4 | Odd amount a in [5,1499], with C={4,6} | 748 | Select 8 distinct amounts without replacement |
| D5 | Amount a in [10,1500], with C={1,3} | 1491 | Select 8 distinct amounts without replacement |
| D6 | x in {3,7,9,11,13,17,19,21,23,27,29,31,33,37,39,41,43,47,49}, with a=100 and C={x,100-x} union {101,...,109} | 19 | Select 4 distinct x values without replacement; each selected x defines one complete pair |
| D7 | For each fixed a in {100,101,102,103,104,105,106,107}, let E_a={x: 2<=x<=floor((a-1)/2) and gcd(x,a)=1}; C={x,a-x} union {a+1,...,a+48} | See §2.3 | Select one x from each E_a |
| D8 | Fixed amount list {2000,2001,2002,2003,2004,2005,2006,2007}, with C={1,a-1,5000} | 8 | Use all eight, once each |

The selector constructs the denomination set only after choosing a parameter from its corresponding eligible set. The generated denomination tuple must then be sorted for canonical identity. D6 presentation order is applied only after the canonical input has been selected.

### 2.3 Exact D7 eligible-set enumeration and sizes

For each a in {100,...,107}, enumerate integers x in ascending order from 2 through floor((a-1)/2), retaining x exactly when gcd(x,a)=1. This is a bounded arithmetic enumeration of at most 53 integers per amount. It is not a combinatorial subset search.

The exact eligible-set sizes are:

| Amount a | Euler phi(a) | Eligible x count (phi(a)-2)/2 |
|---:|---:|---:|
| 100 | 40 | 19 |
| 101 | 100 | 49 |
| 102 | 32 | 15 |
| 103 | 102 | 50 |
| 104 | 48 | 23 |
| 105 | 48 | 23 |
| 106 | 52 | 25 |
| 107 | 106 | 52 |

Every E_a is therefore non-empty and contains at least 15 values. The selector draws exactly one x from each E_a. It does not draw an arbitrary x and reject it for failing the gcd predicate.

For every selected x, x and a-x are distinct, both are greater than one, both are below a, and their sum is a. The 48 fillers a+1 through a+48 are distinct and exceed a. Thus each D7 construction has exactly 50 distinct denominations, none equal to the target, gcd one, and exactly one unordered unlimited-use solution and one unordered 0/1 solution.

### 2.4 Selection algorithm

The parameter selector is a finite-set sampler without replacement where a stratum requires multiple values from one set:

1. Materialize the relevant eligible parameter set in the exact ascending order specified in §§2.2-2.3.
2. Apply a deterministic pseudorandom permutation to that finite list using the single frozen PRNG stream.
3. Take the first q values, where q is the exact stratum quota. For D7, process amounts in ascending order and take one value from each corresponding E_a.
4. Do not generate a proposal outside the eligible list. Do not run a broad-domain rejection loop.
5. Preserve the selected parameter values, their zero-based eligible-list indices, PRNG draw positions, and slot assignments in the future run manifest.
6. Do not select replacement values after any downstream validation or external preflight failure.

For a partial Fisher-Yates sample of q values from a list L of length n, initialize i=0 and repeat while i<q: draw an unbiased integer r from [0,n-i-1], set j=i+r, swap L[i] and L[j], then increment i. The first q values after these q swaps are the ordered sample without replacement. This direction and selected prefix are normative. The exact PRNG algorithm, implementation, seed bytes, integer-range mapping for randbelow(m), interpreter/runtime, and code hash remain freeze-blocking decisions under §7. They must be specified exactly before implementation or execution. The algorithm must not be silently replaced by a language library's unspecified default sampling method.

The PRNG is used only to select among already eligible parameters. It does not determine whether an input satisfies a stratum predicate. All members of every eligible set are valid by construction.

### 2.5 Draw order

The proposed PRNG draw order is:

1. D2: one sample of 8 from the ascending 1499-value list.
2. D4: one sample of 8 from the ascending 748-value list.
3. D5: one sample of 8 from the ascending 1491-value list.
4. D6: one sample of 4 from the ascending 19-value list.
5. D7: one draw from E_100, then E_101, E_102, E_103, E_104, E_105, E_106, and E_107 in that order.

D1, D3, and D8 have fixed eight-value lists and consume no PRNG draws. The bounded-draw schedule therefore contains exactly 36 randbelow calls: 8 for D2, 8 for D4, 8 for D5, 4 for D6, and 1 for each of the eight D7 amounts. Rejected raw PRNG words, if the unbiased randbelow mapping requires them, are recorded separately and do not count as candidate attempts. There is no interleaving, parallel consumption, hidden bounded draw, or draw after a failure. The seed and PRNG engine are not yet selected or frozen.

## 3. Selector-to-invariant proof and mandatory construction checks

### 3.1 Within-stratum identity uniqueness

The selector guarantees within-stratum uniqueness as follows:

- D1 uses eight distinct target amounts, exactly the eight prescribed positions.
- D2, D4, and D5 sample amounts without replacement.
- D3 and D8 use fixed lists of eight distinct amounts.
- D6 samples four distinct x values without replacement. At a=100, different x values in the listed interval produce different sorted denomination tuples.
- D7 has one fixed, distinct target amount per slot. Different target amounts imply different canonical identities even if selected x values happen to coincide.

The selector must verify these conditions before assigning raw input IDs. A duplicate parameter assignment is an invariant failure, not a reason to draw another value.

### 3.2 Cross-stratum identity separation

The mathematical family separation from v0.1 remains valid for every selection permitted by §2:

- D2 has one denomination; no other stratum does.
- D3 and D8 each have three denominations, but their amount ranges are disjoint: 2-9 versus 2000-2007.
- D6 has exactly 11 denominations; D7 has exactly 50.
- D1, D4, and D5 each have two denominations, but their fixed denomination tuples are respectively {3,11}, {4,6}, and {1,3}.
- The remaining strata differ by denomination count or by the amount/denomination tuple as described above.

Consequently, every selector-permitted parameter combination has 60 distinct canonical identities: 56 singleton identities and four D6 identities intended to appear twice in raw presentation. This conclusion is about the complete eligible-set selector, not just an existence witness.

### 3.3 Global identity registry is mandatory

The generator must maintain a construction-time registry keyed by the full canonical identity tuple (amount, sorted denominations), not solely by its SHA-256 digest. Each proposed canonical input is checked against the registry before its slot is accepted.

The registry must enforce all of the following:

1. Exactly eight canonical identities for each of D1, D2, D3, D4, D5, D7, and D8.
2. Exactly four canonical identities for D6.
3. No canonical tuple appears under two different strata.
4. No within-stratum duplicate occurs except the deliberate two-row expansion of a single D6 pair identity.
5. Exactly four D6 pair IDs exist, each with one A member and one B member.
6. Each D6 A/B pair has the same amount and sorted denomination tuple, while B is a non-identity permutation of A.
7. The final registry contains exactly 60 canonical identities.
8. The raw-row multiplicity profile is exactly 56 identities with multiplicity one and four D6 identities with multiplicity two.

A digest is a serialized identifier, not a substitute for comparing the full canonical tuple. The independently implemented validator repeats every check from the frozen bytes.

### 3.4 D1 position and slot assertions

Before the bank can pass validation, the set of D1 target positions must equal exactly {0,1,2,4,5,7,8,10}, and each position must occur once. D6 must have four complete pairs, not eight independently selected rows. Slot quotas are checked by slot ID and by recomputed predicate, never by trusting a stored stratum label.

### 3.5 Failure behavior

Any violation of §§3.1-3.4 terminates the entire run with a run-level invariant failure. The selector must not skip the offending value, select the next eligible value, change the seed, reassign a slot, relabel the candidate, or refill the quota. The mathematical proof makes such a failure unexpected for a correct implementation; it is not a candidate-replacement mechanism.

This amendment does not establish external disjointness, population representativeness, equal difficulty, or any scientific outcome. Those limits in v0.1 remain in force.

## 4. Candidate accounting, rejection and no-replacement rule

### 4.1 Attempt unit

An attempt is one eligible parameter selection assigned to a predeclared slot. For D6, one attempt is one selected x and its complete A/B pair. PRNG words discarded by an unbiased integer-range mapping are not candidate attempts and are not candidate retries.

No selector may propose a value outside its finite eligible set. Therefore the expected number of candidate proposals rejected for failing a D1-D8 predicate is zero.

### 4.2 Candidate-level rejection codes

The candidate-level sidecar may contain only construction or validation failures that are actually attributable to the proposed input or its serialized representation. The protocol-local codes are:

| Code | Meaning |
|---|---|
| TYPE_OR_RANGE_INVALID | Amount or denomination violates the LC518 type/range domain |
| DUPLICATE_DENOMINATION | A denomination is repeated within one input |
| COIN_COUNT_INVALID | Denomination count is outside 1-300 |
| W_ABOVE_INT32 | Independently computed W exceeds the signed-int32 limit |
| EXACT_COUNT_COMPUTATION_FAILED | Either exact-count implementation fails |
| W_IMPLEMENTATIONS_DISAGREE | The two exact W values differ |
| N0_IMPLEMENTATIONS_DISAGREE | The two exact N0 values differ |
| STRATUM_MATCH_COUNT_ZERO | Candidate matches none of D1-D8 |
| STRATUM_MATCH_COUNT_MULTIPLE | Candidate matches more than one of D1-D8 |
| SLOT_PREDICATE_FAIL | Candidate fails its predeclared slot predicate |
| D1_POSITION_DUPLICATE_OR_MISSING | D1 position quota is not met exactly once |
| D6_PAIR_INCOMPLETE | A complete D6 pair is not available |
| D6_PERMUTATION_NOT_NONIDENTITY | D6 member B is not a non-identity permutation |
| ORACLE_MAPPING_MISMATCH | Oracle key or W value differs from the independently recomputed result |
| HASH_OR_SERIALIZATION_MISMATCH | A required byte-level hash or canonical serialization check fails |
| SELECTOR_OUTSIDE_ELIGIBLE_SET | A selector output is not a member of its frozen eligible set |

B1-development overlap and protected-evaluation overlap are deliberately not candidate-level rejection codes. They are external preflight outcomes under §5. A canonical-identity invariant violation is a run-level failure, not a request to reject and replace one candidate.

### 4.3 No candidate retries or replacements

The no-replacement rule is retained, with its mechanism now defined:

- The selector samples directly from each frozen eligible set.
- Sampling without replacement is applied wherever multiple values are selected from one eligible set.
- No broad-domain proposal followed by candidate rejection is permitted.
- The candidate retry limit is zero.
- If any selected item fails a mandatory check, the complete run aborts.
- No next eligible value, alternate seed, alternate PRNG, new draw, slot transfer, stratum reassignment, or silent replacement is permitted.
- Any future change to a failed selector configuration requires a new reviewed protocol version and explicit owner acceptance before a new run configuration can be considered.

A zero-retry policy is workable here because all possible selector outputs are members of the enumerated eligible sets, and all combinations of those sets satisfy the internal quota and identity proofs. It is not being applied to raw-domain random proposals.

### 4.4 Sidecar and terminal run statuses

A future candidate-level rejection sidecar records each actual candidate validation failure, if any, with event index, slot/pair ID, selected parameter and eligible-list index, attempt index, candidate values if materialized, applicable reason codes, validator version/hash, and terminal run status.

Under a correct implementation of this selector, the candidate-level rejection sidecar is expected to contain zero events. A non-empty sidecar means the construction did not follow the eligible-set selector or an asserted property failed. The first such event terminates the run. There is no retry.

Run-level terminal statuses are separate from candidate reason codes:

- RUN_ABORTED_INTERNAL_INVARIANT
- RUN_ABORTED_EXACT_COUNT_ORACLE_CHECK
- RUN_ABORTED_SERIALIZATION_OR_HASH_CHECK
- PREFLIGHT_BLOCKED_B1_IDENTITY_SOURCE_MISSING
- PREFLIGHT_BLOCKED_PROTECTED_FRAME_OR_CUSTODIAN_MISSING
- PREFLIGHT_EXTERNAL_OVERLAP
- PREFLIGHT_ERROR
- PREFLIGHT_PASS

The preflight statuses are not candidate rejection events and are not included in the candidate rejection count.

### 4.5 Counting argument for zero candidate-rejection aborts

The selector's parameter-selection space has the following exact number of eligible parameter combinations:

N = P(1499,8) × P(748,8) × P(1491,8) × P(19,4) × 19 × 49 × 15 × 50 × 23 × 23 × 25 × 52, where P(n,q)=n!/(n-q)! counts ordered samples without replacement.

The factors correspond respectively to the ordered D2, D4, D5, and D6 selections, followed by one eligible x choice for each of the eight fixed D7 target amounts. D1, D3, and D8 have no parameter-choice degrees of freedom because their complete eight-item lists are fixed. The order of each sample determines its mapping to the ascending slot IDs.

Every ordered selector output counted by N satisfies the slot predicates, within-stratum uniqueness and cross-stratum identity separation proved in §§2-3. Thus the number of eligible ordered outputs that cause a candidate-level rejection or internal quota/collision failure is zero. Conditional on correct selector and validator implementations, the candidate-rejection abort proportion is exactly 0/N = 0. This is a finite counting result, not a simulated failure rate or a probability estimate from sampled runs.

External preflight is a separate Boolean gate. Its result cannot be counted or estimated until the authoritative B1 key source and protected evaluation frame exist. A preflight overlap aborts the entire frozen selector configuration; it does not reject an individual candidate or authorize another seed.

## 5. External disjointness is a whole-configuration preflight

### 5.1 Remove external overlap from candidate rejection

The former v0.1 reason codes B1_DEVELOPMENT_OVERLAP and PROTECTED_EVALUATION_OVERLAP are deleted from the candidate-level rejection taxonomy. An external key collision does not make a candidate invalid under D1-D8. It makes the complete proposed diagnostic configuration ineligible for use alongside the specified external bank.

The construction must not search for a different candidate, replace a slot, draw another seed, or move a record to another stratum to avoid an external collision. Such replacement would create an outcome-dependent or externally selected bank and is prohibited by this protocol.

### 5.2 Preflight sequence and information boundary

Only after an explicit separate authorization for preflight may the frozen selector configuration be evaluated to derive the 60 canonical identities for comparison. The custodian or authorized comparison service receives the diagnostic canonical identities or their approved canonical digests. The construction agent does not receive protected evaluation inputs or keys.

The preflight compares the complete set of 60 unique diagnostic canonical identities against:

1. the authoritative 78-row B1 v1.7 development identity set; and
2. the exact protected evaluation identity frame defined by the separately accepted B1 amendment.

The protected-set comparison is performed by the independent custodian. The custodian reports only the predeclared outcome, set identifiers, compared cardinalities and an authenticated report/hash. It does not disclose protected rows or keys.

No selector or bank construction may proceed to final generation while either external identity source is missing, unauthenticated, or not defined.

### 5.3 Current B1 hard stop

The authoritative row-level identity source for the 78 records of accepted B1 v1.7 remains OPEN / NOT ESTABLISHED. H80's 78 unique canonical identities must not be substituted. Equal cardinality is not evidence of identity, intersection, or disjointness.

Therefore the B1 preflight is currently blocked. No B1 overlap comparison can be performed and no preflight PASS can be claimed. This amendment does not resolve the missing source.

### 5.4 Protected evaluation hard stop

The protected evaluation frame, canonical identity definition, accepted separate B1 amendment, independent custodian appointment and custody controls remain OPEN. No blind E3 or other protected record may be accessed by the construction agent.

Therefore the protected-set preflight is also currently blocked. No comparison, hash request, inspection, or protected-data access is authorized by this draft.

### 5.5 Preflight outcomes

The preflight result is one of the following run-level statuses:

| Status | Condition | Consequence |
|---|---|---|
| PREFLIGHT_BLOCKED_B1_IDENTITY_SOURCE_MISSING | Authoritative B1 row-level key source is absent or provenance is unresolved | Stop before selector preflight; no bank construction |
| PREFLIGHT_BLOCKED_PROTECTED_FRAME_OR_CUSTODIAN_MISSING | Protected evaluation frame, accepted B1 amendment, or independent custodian is absent | Stop before protected comparison; no bank construction |
| PREFLIGHT_EXTERNAL_OVERLAP | Any of the 60 diagnostic canonical identities overlaps either external set | Abort the entire frozen selector configuration; no replacement or new seed |
| PREFLIGHT_ERROR | Identity derivation, set comparison, custody, authentication, or report validation fails | Abort; no comparison result may be treated as PASS |
| PREFLIGHT_PASS | Both comparisons complete under the frozen procedure and report no overlaps | The configuration may proceed only to a separately authorized bank-generation step |

A PASS is specific to the exact v0.4 hash, protocol hash, PRNG, seed, slot mapping, canonicalization rule, B1 source hash, protected-frame identifier, custodian procedure and selector output. Any change invalidates the PASS and requires a new preflight.

### 5.6 No preflight-based reselection

If PREFLIGHT_EXTERNAL_OVERLAP occurs, the selector configuration is rejected as a whole. The protocol may not silently change seed, draw order, selected indices, parameter values or slots. A revised selector configuration requires a new protocol version, independent review, explicit owner acceptance and a new preflight. The external overlap is never entered as a candidate-level rejection and never used to select replacements.

## 6. Revised freeze and authorization sequence

A future workflow must separate preflight authorization from bank-generation authorization:

1. Complete Claude and GLM independent review of the exact protocol amendment; GPT adjudicates; obtain explicit owner acceptance of the exact final protocol hash.
2. Resolve every freeze-blocking decision in §7, including the PRNG algorithm, implementation, seed bytes, runtime, unbiased integer-range mapping, and draw order.
3. Establish the authoritative B1 78-row identity source and verify provenance.
4. Complete the separate B1 amendment defining the protected evaluation target, canonical identity frame, and comparison requirements.
5. Appoint and qualify the independent custodian; close consent and trigger-(i) gates.
6. Obtain a distinct, explicit GO for the narrowly scoped external preflight. No bank-generation GO is implied.
7. Pin and verify v0.4, its owner-acceptance record, this protocol, selector implementation, PRNG, seed, interpreter/runtime, and independent comparison procedure.
8. Derive the selector output only within the authorized preflight scope and compare its 60 canonical identities against the B1 development and protected evaluation sets.
9. Require an authenticated PREFLIGHT_PASS. Any missing source, error, or overlap stops the workflow; no replacement or reselection is permitted.
10. Only after a PASS, obtain a separate explicit bank-generation GO.
11. Reconstruct the same selector output from the identical frozen configuration; assert all invariants in §3; compute exact W and N0 by the independently specified implementations; and write the bank package.
12. Run the independent validator against the exact frozen bytes and reconcile the rejection sidecar, row manifest, oracle attachment, and hashes.
13. Freeze the manifest, oracle, sidecar, validation report and hash inventory together.
14. Solver construction or any further experiment requires another separately authorized phase and is not permitted by this protocol.

A preflight PASS does not authorize bank generation. A bank-generation GO does not authorize solver construction. Neither is granted by owner acceptance of v0.4 or by this design-only amendment.

## 7. Remaining freeze-blocking decisions

| ID | Decision | Status |
|---|---|---|
| V01 | Confirm the finite eligible-set definitions and cardinalities in §2 | PROPOSED; independent review required |
| V02 | Select exact PRNG algorithm and implementation | OPEN |
| V03 | Fix seed bytes and seed derivation, with no post-preflight seed changes | OPEN |
| V04 | Fix interpreter/runtime build and dependency environment | OPEN |
| V05 | Specify exact unbiased randbelow mapping and PRNG word-discard accounting | OPEN |
| V06 | Confirm partial Fisher-Yates and the draw order in §2.5 | PROPOSED |
| V07 | Freeze selected-parameter and eligible-index manifest fields | PROPOSED |
| V08 | Freeze the global canonical-identity registry implementation and independent recheck | PROPOSED |
| V09 | Establish authoritative B1 78-row identity source and provenance | OPEN / HARD STOP |
| V10 | Define the protected evaluation frame and accept separate B1 amendment | OPEN / HARD STOP |
| V11 | Appoint independent custodian and complete consent/trigger-(i) requirements | OPEN / HARD STOP |
| V12 | Specify and authorize external preflight procedure | OPEN / HARD STOP |
| V13 | Obtain owner acceptance of the exact final protocol hash | NOT ISSUED |
| V14 | Obtain separate preflight GO and, only after PASS, bank-generation GO | NOT ISSUED |

The parameter-set counts and zero candidate-rejection result are fully specified at the mathematical level. The PRNG/runtime/seed details remain open. This document is therefore not build-ready or frozen.

## 8. Current disposition

**v0.4 taxonomy:** OWNER-ACCEPTED at blob 8873389a0b38a7c9a1307f1c4f9fe4f7dee13def.  
**v0.1 base protocol:** DRAFT at blob 96e454b4bb0b1582635d47e89358a7feee021512.  
**v0.2 amendment:** DRAFT FOR INDEPENDENT REVIEW; not frozen or owner-accepted.  
**Eligible-set selector:** Specified as a finite-set sampler; PRNG/runtime/seed remain open.  
**Simultaneous quota feasibility:** Every selector-permitted parameter combination satisfies the internal quota and canonical-identity proof.  
**Candidate rejection under a correct selector:** Exactly zero by construction; no candidate replacement is permitted.  
**External B1 identity preflight:** BLOCKED because the authoritative 78-row identity source is OPEN / NOT ESTABLISHED.  
**Protected evaluation preflight:** BLOCKED because the protected frame, separate B1 amendment and custodian remain OPEN.  
**Preflight PASS:** NOT AVAILABLE.  
**Generator, selector execution, candidate enumeration, bank generation and solver work:** NOT AUTHORIZED.  
**Gate 0:** OPEN.  
**Project pause:** REMAINS IN FORCE.

No selector was executed. No candidate values were selected or materialized. No candidate list, bank, manifest, oracle attachment, rejection sidecar, solver body or experimental outcome was created by this amendment.
