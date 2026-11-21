# LC518 v0.21 diagnostic-bank generation protocol

**Document ID:** LC518-V021-DIAG-GEN-PROTOCOL-2026-11-21  
**Version:** 0.1  
**Date:** 2026-11-21  
**Status:** DRAFT FOR INDEPENDENT REVIEW; DESIGN-ONLY; NOT FROZEN; NO GENERATION OR EXECUTION GO  
**Governing taxonomy:** v0.21 operational diagnostic-strata specification v0.4, exact blob `8873389a0b38a7c9a1307f1c4f9fe4f7dee13def`  
**Owner acceptance record:** `docs/LC518_V021_V04_OWNER_ACCEPTANCE_2026-11-21.md`, exact blob `472b7f1f94ee6fa1792f3f833a5418a77e93e9e9`  
**Design purpose:** Specify the controls and decisions required for a future deterministic construction of the 64-record D1–D8 diagnostic bank.  
**Current authorization:** Documentary design and independent critique only.

---

## 1. Purpose, authority and non-authorization

This is a new v0.21 generation-protocol draft. It is derived from the owner-accepted v0.4 taxonomy identified above. It does not amend the v0.4 predicates, the accepted B1 v1.7 analysis plan, or accepted Rev 1.4.

The protocol is deliberately separate from historical C9 revision 2.6. It does not adopt or reuse C9 seeds, PRNG settings, draw order, retry limits, rejection codes, generator assumptions, schemas, scripts, or execution settings. A future decision to use any matching technical choice would require a fresh derivation and explicit documentation against v0.4. Historical C9 materials are not authority for this protocol.

This draft is not a frozen generation protocol. It does not authorize:
- generator implementation or execution;
- candidate enumeration, sampling, or record generation;
- creation of the diagnostic bank, oracle attachment, manifest, or rejection sidecar;
- mutation allocation or solver construction, modification, compilation, or execution;
- diagnostic probing or outcome collection;
- access to protected evaluation records;
- model fitting, simulation, or power analysis.

The project pause remains in force. The constructions in §4 are mathematical quota-feasibility witnesses only. They are not an allocated bank, frozen slot contents, candidate manifest, or permission to materialize the inputs.

## 2. Normative inputs and fixed bank structure

### 2.1 Authority pins

A future run must pin and verify, by content hash, all of the following before any candidate construction:

| Object | Required pin |
|---|---|
| Operational taxonomy | v0.4 blob `8873389a0b38a7c9a1307f1c4f9fe4f7dee13def` |
| Owner acceptance | v0.4 acceptance-record blob `472b7f1f94ee6fa1792f3f833a5418a77e93e9e9` |
| Generation protocol | A later owner-accepted and frozen protocol hash; this draft is not that hash |
| Generator source and dependencies | Exact source commit, dependency lock, runtime/interpreter build and environment description |
| PRNG and selection configuration | Exact algorithm, implementation/version, seed material, stream/substream allocation and draw order, or an explicitly adjudicated alternative |
| Slot plan | Exact slot order, parameter-selection rule and D6 pair layout |
| Validation implementation | Exact primary and independent validator source hashes |

A mismatch between a run's pinned v0.4 blob and the accepted blob is a hard failure. The generator must not read an unpinned “latest” taxonomy file and continue.

### 2.2 Required quotas

The future diagnostic bank has exactly 64 raw records:

| Stratum | Raw records | Distinct canonical identities | Structural requirement |
|---|---:|---:|---|
| D1 | 8 | 8 | Each of the eight prescribed target positions appears exactly once |
| D2 | 8 | 8 | Eight distinct canonical inputs |
| D3 | 8 | 8 | Eight distinct canonical inputs |
| D4 | 8 | 8 | Eight distinct canonical inputs |
| D5 | 8 | 8 | Eight distinct canonical inputs |
| D6 | 8 | 4 | Four distinct inputs, each shown as one original and one non-identity permutation |
| D7 | 8 | 8 | Eight distinct canonical inputs |
| D8 | 8 | 8 | Eight distinct canonical inputs |
| **Total** | **64** | **60** | Four D6 duplicate groups only |

The final canonical multiplicity profile must be exactly:
- 56 canonical identities with multiplicity one;
- four canonical identities with multiplicity two, each corresponding to one complete D6 pair;
- zero other repeated identities.

The bank is not valid merely because it contains 64 rows or eight rows bearing each label. All predicates, slot constraints, canonical multiplicities, exact-answer conditions and cross-bank checks must pass.

### 2.3 Slot-order convention proposed for review

The proposed slot sequence is stratum order D1 through D8, then within-stratum slot order 01 through 08. D6 is represented as four pair slots, each yielding two raw rows:

- D1-01 … D1-08
- D2-01 … D2-08
- D3-01 … D3-08
- D4-01 … D4-08
- D5-01 … D5-08
- D6-P01 … D6-P04, each with members A and B
- D7-01 … D7-08
- D8-01 … D8-08

For D6, the proposed presentation convention is a canonical ascending denomination order for member A and its exact reverse for member B. The reverse is non-identity because each D6 input has at least 11 distinct denominations. Both rows retain the same amount and canonical identity. This is a protocol proposal for review, not a change to v0.4.

## 3. Input contract and exact predicate validation

Every accepted candidate must satisfy the v0.4 LC518 input domain:
- integer target amount (0 \le a \le 5000);
- 1–300 distinct positive integer denominations, each in 1–5000;
- repeated denominations are invalid and must not be silently removed;
- exact LC518 answer (W(a,C)) must fit signed int32, at most 2,147,483,647.

The canonical identity is the pair consisting of the amount and the sorted denomination tuple. Input order is irrelevant to identity; multiplicity is preserved and separately rejected by the distinct-denomination contract.

For every candidate, the validator evaluates all eight v0.4 predicates. It must find exactly one match. Zero matches or multiple matches cause rejection. There is no priority assignment, relabelling, or post-outcome reassignment.

All exact-answer checks are performed before any solver outcome exists. Neither a candidate solver's result nor observed solver performance may influence candidate acceptance, rejection, slot assignment, ordering, or replacement.

## 4. Design-only simultaneous quota-feasibility proof

### 4.1 Purpose and limitation of this proof

Claude's review correctly distinguishes one non-emptiness witness per predicate from a simultaneous quota proof. This section addresses the latter by giving parameterized construction families. The families show that all eight quotas can be satisfied simultaneously, with four distinct D6 pairs and exactly 60 canonical identities, while respecting the stated domain bounds.

This is a mathematical existence argument only. No concrete 64-row manifest has been created, no candidate inputs have been emitted by a generator, no parameter values have been allocated to future slots, and no cross-bank disjointness claim is made. A later generator still needs an owner-accepted deterministic selection rule and must pass the full validators.

### 4.2 Parametric witness families

The following families are sufficient to establish the eight-per-stratum quota. They are intentionally described as families rather than as a frozen record list.

**D1.** Use the v0.4 witness denomination set (C=\{3,11\}). Its minimum denomination is 3, its gcd is 1, and (3c_{\min}+1=10\le1500). The required eight target positions are the eight distinct values
[
\{0,1,2,4,5,7,8,10\}.
]
None is a denomination. For target 0, (W=N_0=1); for the other seven targets, both counts are zero. Thus all eight positions meet D1 and have eight distinct canonical identities because their amounts differ.

**D2.** For any eight distinct integer amounts selected from ([2,1500]), use the singleton denomination set (C=\{a\}) for each amount. Each input has (n=1), and (W=N_0=1). Distinct amounts give distinct canonical identities.

**D3.** For each amount (a\) in the eight-value set ({2,3,4,5,6,7,8,9}), use (C=\{a,10,11\}). Exactly one denomination equals the target, the other two exceed it, and (gcd(a,10,11)=1) because (gcd(10,11)=1). Therefore (W=N_0=1). The eight distinct amounts give eight distinct canonical identities.

**D4.** Use (C=\{4,6\}), with any eight distinct odd target amounts from 5 through 1500. The denominations are even, their gcd is 2, and each selected target is odd and at least the minimum denomination. Every target is unreachable, so (W=N_0=0). Distinct targets give distinct canonical identities.

**D5.** Use (C=\{1,3\}), with any eight distinct amounts from 10 through 1500. For each such amount,
[
W(a,\{1,3\})=\left\lfloor a/3\right\rfloor+1,
]
because each nonnegative number of 3-denominations from zero through (lfloor a/3\rfloor) determines exactly one number of 1-denominations. Hence (W\ge4). Since the sum of the two denominations when each can be used at most once is only 4, (N_0=0) for every target in this range. Thus (W>N_0), the target is not a denomination, and the gcd is 1. Distinct amounts give eight distinct identities.

**D6.** Set the target to (a=100). For a parameter (x) with (2\le x\le49) and (gcd(x,100)=1), define
[
C_x=\{x,100-x\}\cup\{101,102,\ldots,109\}.
]
There are 11 distinct denominations, the target is not a denomination, and the gcd is 1. The nine filler denominations exceed the target and cannot contribute. For the two remaining denominations (x) and (100-x), the equation
[
u x+v(100-x)=100,quad u,v\in\mathbb Z_{\ge0}
]
has only the solution ((u,v)=(1,1)): because (gcd(x,100-x)=1), every integer solution differs from ((1,1)) by a multiple of ((100-x,-x)), and every nonzero such multiple makes at least one coefficient negative. Consequently (W=N_0=1).

There are (arphi(100)=40) integers in ([1,99]) coprime to 100. Excluding 1 and 99 leaves 38 interior values, paired symmetrically around 50, hence 19 eligible values in ([2,49]). Four distinct values can therefore be selected to define four distinct canonical identities. Each identity yields two rows, one in ascending order and one in reverse order. This proves the availability of four complete D6 pairs without making a pair manifest.

**D7.** For each target (a\) in ({100,101,102,103,104,105,106,107}), select a parameter (x) satisfying
[
2\le x\le\left\lfloor(a-1)/2\right\rfloor,qquad \gcd(x,a)=1,
]
and let (y=a-x). Define
[
C_{a,x}=\{x,y\}\cup\{a+1,a+2,\ldots,a+48\}.
]
This gives exactly 50 distinct denominations. The 48 filler denominations exceed the target and cannot contribute. Also, (x,y>1), (x+y=a), and (gcd(x,y)=gcd(x,a)=1). The same integer-solution argument used for D6 shows that (ux+vy=a) has only ((u,v)=(1,1)) in nonnegative integers. Thus (W=N_0=1). All filler values are at most 155, so the input-domain bounds are respected.

For each (a\in[100,107]), there are eligible (x) values in the stated interval. Specifically, the number is ((\varphi(a)-2)/2); for these eight amounts the minimum (arphi(a)) is 32, leaving at least 15 eligible values. Therefore each of the eight amounts admits at least one valid D7 construction. Since the amounts differ, the resulting eight canonical identities are distinct. This directly addresses the D7 scale concern: the 48 filler denominations are a simple contiguous range above the target, not the result of a combinatorial search.

**D8.** For each amount (a\) in ({2000,2001,\ldots,2007}), use
[
C_a=\{1,a-1,5000\}.
]
There are three distinct denominations, none equals the target, and the gcd is 1. The 5000 denomination exceeds each selected target. For the other two denominations, the equation (u+v(a-1)=a) has exactly two nonnegative solutions: ((a,0)) and ((1,1)). Therefore (W=2). Only ((1,1)) uses each denomination at most once, so (N_0=1). D8 requires reachability, and this family satisfies it. The eight distinct amounts give eight distinct canonical identities.

### 4.3 Simultaneous identity and collision proof

The family constructions establish within-stratum uniqueness by distinct amounts, except D6, where uniqueness follows from four distinct (x) values with (2\le x\le49) and a common target of 100.

Cross-stratum collisions are excluded as follows:

- D2 has one denomination; no other stratum does.
- D3 and D8 each have three denominations, but their amount ranges are disjoint: D3 uses 2–9 and D8 uses 2000–2007.
- D6 has 11 denominations; D7 has 50.
- The only remaining strata with two denominations are D1, D4 and D5. Their denomination sets are respectively (\{3,11\}), (\{4,6\}), and (\{1,3\}), so their canonical denomination tuples cannot coincide.
- Every other cross-stratum pair differs by denomination count or, for the identified two-denomination cases, by the denomination tuple.

Thus the constructed families can furnish 8 + 8 + 8 + 8 + 8 + 4 + 8 + 8 = 60 distinct canonical identities. Expanding the four D6 identities to original/permutation presentations yields 64 raw rows. The only repeated canonical identities are those four declared D6 pairs. This is a constructive simultaneous-quota existence proof, not a statement that any future random draw or seeded generator will succeed.

### 4.4 What this proof does not establish

It does not establish:
- which parameter values will be used in the final bank;
- that a future PRNG selection rule will choose valid, mutually distinct candidates;
- diagnostic-to-development or diagnostic-to-evaluation disjointness;
- a representative natural-input distribution;
- baseline difficulty equivalence across strata;
- equal computational cost across strata; or
- any solver failure, predictive effect, or scientific result.

The eventual protocol must either adopt a deterministic selection rule that uses these families or independently prove equivalent simultaneous feasibility for its own construction method. It must not claim that the existence proof validates a different generator's unconstrained random proposal process.

## 5. Exact computation of W and N0

### 5.1 Primary exact algorithm

For each valid input, sort the distinct denominations in ascending order. Compute with arbitrary-precision integers; do not use floating point, saturation arithmetic, or signed-32-bit intermediate counters.

For (W), initialize an array (dp_W[0..a]) to zero and set (dp_W[0]=1). For each denomination (c), in ascending order, update targets in ascending order:
[
dp_W[t]\leftarrow dp_W[t]+dp_W[t-c],quad t=c,c+1,\ldots,a.
]
The final value (dp_W[a]) is the exact number of unordered combinations with unlimited use of each denomination.

For (N_0), initialize (dp_0[0..a]) to zero and set (dp_0[0]=1). For each denomination (c), in ascending order, update targets in descending order:
[
dp_0[t]\leftarrow dp_0[t]+dp_0[t-c],quad t=a,a-1,\ldots,c.
]
The final value (dp_0[a]) is the exact number of unordered combinations in which each denomination is used at most once.

The direction of iteration is normative: ascending for (W), descending for (N_0). Reversing either direction changes the counting problem and is a validation failure.

### 5.2 Independent implementation check

A second implementation must be written and versioned independently from the primary implementation. It must not import the primary DP functions or share their mutable DP arrays.

The proposed independent implementation uses a two-dimensional denomination-prefix table. Let (W_i[t]) and (N_i[t]) be counts using the first (i) sorted denominations. Initialize (W_0[0]=N_0[0]=1), with all positive-target entries zero. For denomination (c_i), compute:
[
W_i[t]=W_{i-1}[t]+W_i[t-c_i]quad(t\ge c_i),
]
with (W_i[t]=W_{i-1}[t]) for (t<c_i); and
[
N_i[t]=N_{i-1}[t]+N_{i-1}[t-c_i]quad(t\ge c_i),
]
with (N_i[t]=N_{i-1}[t]) for (t<c_i).
The final entries (W_n[a]) and (N_n[a]) must exactly match the primary implementation.

The two implementations use the same mathematical counting definitions but different state representations and separately written code. Their source files, runtimes, dependency environments, and hashes must be recorded separately. A single code path called twice is not an independent check.

### 5.3 Arithmetic and acceptance guards

Both implementations must use arbitrary-precision integer arithmetic for every intermediate entry. A final answer that exceeds 2,147,483,647 fails the global LC518 input contract; it must not be clipped, wrapped, rounded, or stored as a valid oracle output.

For every canonical identity:
1. Both implementations must independently compute (W).
2. Both must independently compute (N_0).
3. The two (W) values must agree exactly.
4. The two (N_0) values must agree exactly.
5. (0\le N_0\le W\le2,147,483,647) must hold.
6. The exact D1–D8 predicate must pass using the agreed values.
7. The stored oracle output must equal the agreed (W).

Any disagreement or inability to compute is a hard failure. Do not choose one implementation's value, rerun selectively until values agree, or repair an answer by inspecting solver outcomes.

### 5.4 Complexity and the D7 scale issue

The primary one-dimensional algorithms take (O(n a)) DP updates and (O(a)) integer cells per count. Under the v0.4 bounds:
- D7 has (n\le300) and (a\le500), so at most 150,000 denomination-target update positions per DP;
- D8 has (n\le30) and (a\le5000), also at most 150,000 update positions per DP.

The D7 construction family in §4 uses two denominations that sum to the target and 48 denominations strictly greater than the target. Those 48 values are selected by a simple bounded rule, not searched as subsets. Exact DP still validates the entire denomination array. The construction does not enumerate combinations or search an exponential subset space.

The operation counts above are design bounds, not measured runtimes. Runtime and memory requirements must be verified in the pinned environment before any future execution GO. No benchmark or computational run is authorized by this draft.

## 6. Candidate proposal, rejection accounting and fail-closed behavior

### 6.1 Attempt unit and slot accounting

A candidate attempt is one proposal evaluated for one singleton slot. For D6, one attempt is a complete proposed canonical input plus both required orderings; the pair is accepted or rejected as a unit. A half-pair must never occupy a slot.

The attempt counter increments before validation for every proposal, including invalid-domain proposals, exact-answer failures, duplicates, and candidates that fail an external disjointness check. A rejected attempt remains in the sidecar. It is not an accepted bank row and cannot be erased from the run history.

A future deterministic selection mechanism must define the proposal stream before execution. Slot order and draw order must be fixed. No proposal stream may depend on solver outcomes.

### 6.2 Rejection reason codes

The following proposed reason codes are protocol-local and are not inherited from C9:

| Code | Meaning |
|---|---|
| `TYPE_OR_RANGE_INVALID` | Amount or denomination violates the LC518 type/range domain |
| `DUPLICATE_DENOMINATION` | A denomination is repeated within an input |
| `COIN_COUNT_INVALID` | Number of denominations is outside 1–300 |
| `W_ABOVE_INT32` | Exact (W) exceeds the global signed-int32 bound |
| `EXACT_COUNT_COMPUTATION_FAILED` | Either independent exact computation fails |
| `W_IMPLEMENTATIONS_DISAGREE` | Independent (W) values differ |
| `N0_IMPLEMENTATIONS_DISAGREE` | Independent (N_0) values differ |
| `STRATUM_MATCH_COUNT_ZERO` | Candidate matches none of D1–D8 |
| `STRATUM_MATCH_COUNT_MULTIPLE` | Candidate matches more than one of D1–D8 |
| `SLOT_PREDICATE_FAIL` | Candidate does not satisfy its predeclared slot rule |
| `D1_POSITION_DUPLICATE_OR_MISSING` | D1 position quota is not met exactly once |
| `D6_PAIR_INCOMPLETE` | Both D6 presentations are not available and valid |
| `D6_PERMUTATION_NOT_NONIDENTITY` | D6 member B is not a non-identity permutation |
| `CANONICAL_COLLISION` | Canonical multiplicity violates the 56-singleton/four-pair structure |
| `ORACLE_MAPPING_MISMATCH` | Oracle key or value does not match independently recomputed identity and (W) |
| `B1_DEVELOPMENT_OVERLAP` | Candidate canonical key appears in the authoritative B1 development identity set |
| `PROTECTED_EVALUATION_OVERLAP` | Independent custodian reports an overlap with the protected evaluation set |
| `HASH_OR_SERIALIZATION_MISMATCH` | A required byte-level hash or canonical serialization check fails |

A candidate may carry multiple reason codes. The sidecar records all applicable codes in a predeclared validation-stage order; it must not suppress secondary failures merely because an earlier check also failed. Run-level failures, including quota exhaustion and validator failure, are separate terminal statuses rather than candidate reason codes.

### 6.3 Proposed retry policy and unresolved numeric setting

This draft proposes **zero retries after a rejected proposal**. The initial proposal counts as attempt 1. If it fails any mandatory check, the run aborts; the slot is not refilled, no alternative stratum is used, no seed is changed, and no new attempt is silently started.

This no-retry policy is chosen to prevent unbounded rejection search, hidden selection pressure, and unreported replacement. It is a proposal for review, not yet owner-accepted. A reviewer may argue for a bounded retry design, but any alternative must state:
- a finite per-slot and per-pair attempt cap;
- whether the cap counts proposals or complete D6 pairs;
- deterministic draw and retry order;
- exactly what is written for every rejected attempt;
- the terminal status on exhaustion; and
- an explicit prohibition on increasing the cap, changing the seed, moving the candidate to another stratum, or replacing a row after exhaustion.

Under the proposed zero-retry rule, a failed proposal yields terminal status `RUN_ABORTED_CANDIDATE_REJECTED`. If a future owner-accepted protocol instead chooses a positive finite cap, reaching it with an unfilled slot yields `RUN_ABORTED_QUOTA_EXHAUSTED`. In either case, an aborted run is not a bank and cannot be presented as a partially valid 64-row suite.

**Open decision:** the actual proposal-selection mechanism, PRNG, seed material, and whether the v0.4 §5.4 PRNG requirement is satisfied by a seeded parameter selector or requires another explicitly adjudicated deterministic method remain unresolved. This draft does not select a PRNG, seed, retry count above zero, or generator implementation. Those choices must be reviewed and frozen before any implementation or execution.

### 6.4 Rejection sidecar structure

The future rejection sidecar is deterministic UTF-8 JSON Lines. Each event must include:
- monotonically increasing `event_index`;
- `slot_id` and, for D6, `pair_id`;
- `attempt_index`;
- candidate amount and the exact proposed coin array in as-proposed order;
- `canonical_id`, if the candidate is valid enough to canonicalize;
- all applicable `reason_codes`, in fixed validation-stage order;
- the validator version/hash; and
- a terminal run status when the event aborts the run.

No wall-clock timestamp is required; omitting it avoids injecting non-deterministic metadata into the construction record. The complete sidecar must reconcile exactly with the attempt counters, accepted slot records, and final run status.

## 7. Canonical serialization, manifest and oracle outputs

### 7.1 Canonical input identity bytes

The proposed canonical identity byte representation is UTF-8 without BOM, with no whitespace, using exactly this key order and value form:

`{"amount":<base-10-integer>,"coins":[<ascending-base-10-integers>]}`

The amount is a base-10 integer with no leading plus sign or leading zeroes except the value zero. The coin array contains the sorted distinct denominations, comma-separated, with no spaces. The canonical ID is the lowercase hexadecimal SHA-256 digest of those bytes, prefixed by `sha256:`.

This is a protocol-level serialization proposal. It must be independently implemented and tested in both validators before freeze. It does not alter the mathematical canonical identity defined by v0.4.

### 7.2 Manifest structure

The future manifest must include, at minimum:
- protocol ID/version and all pinned source hashes;
- generation run ID and deterministic run configuration;
- ordered slot list and exact quota counts;
- each raw `input_id`, stratum, slot ID and rule ID;
- amount and coins in presentation order;
- canonical ID;
- D6 pair ID and `ordering` for D6 rows only;
- exact (W) and (N_0) validation references;
- oracle-object key;
- record hash;
- counts of accepted proposals, rejected proposals and terminal status.

The manifest must preserve the distinction between raw record rows and canonical identities. The D6 members share one canonical ID and one oracle object but have distinct raw `input_id` and record hashes.

### 7.3 Oracle and validation attachments

The oracle attachment contains exactly one object for each of the 60 canonical identities. Each object includes canonical ID, amount, sorted denominations and exact (W). D6 pair members point to the same object. There must be no extra oracle keys and no missing key.

The separate construction-validation attachment records both exact (W) and (N_0) for all 60 identities, both independent implementation results, the D1 target-position result, the D6 pair check, the unique stratum match count, and the associated predicate checks. (N_0) must be labelled as a construction-validation quantity, not the LC518 oracle answer.

### 7.4 Hashing and byte-level reproducibility

The frozen package must include SHA-256 digests for:
- raw manifest bytes;
- oracle attachment bytes;
- rejection sidecar bytes;
- construction-validation report bytes;
- primary validator source and environment;
- independent validator source and environment;
- generator source and environment; and
- a package inventory listing all filenames, sizes and digests.

The exact serialization rules, line endings, key ordering, newline termination and archive packaging must be specified before the hashes are calculated. The hash inventory must not hash a file containing its own final digest unless a separate non-recursive rule is defined.

The independent reviewer must recompute file hashes from the delivered bytes and verify every row-level record hash and canonical ID. A filename or a GitHub artifact digest alone is not a substitute for member-level validation.

## 8. Independent validation and role separation

At least two validation paths are required:
1. The generator-side validator checks domain, exact (W), exact (N_0), all eight predicates, slot quotas, canonical identities, D6 pairing, and serialization.
2. An independently written validator recomputes the same properties from the frozen bytes without importing generator code or trusting the generator's reported values.

The independent validator must:
- recalculate every canonical ID from amount and sorted denominations;
- recalculate (W) and (N_0) using its own implementation;
- confirm exactly one D1–D8 match for every canonical identity;
- confirm eight raw rows per stratum;
- confirm D1 positions appear once each;
- confirm four complete D6 pairs with different orderings and identical canonical keys;
- confirm 60 canonical identities, comprising 56 singletons and four multiplicity-two D6 keys;
- confirm exactly 60 oracle objects with exact key equality;
- compare every oracle (W) value to both independent computations;
- verify the rejection ledger and attempt counters; and
- recompute all file/member hashes.

A self-review by the generator author is not independent validation. Reviewer identity and role must be recorded. This document does not appoint the independent reviewer or custodian.

## 9. B1 development identity and protected-evaluation hard stop

### 9.1 B1 78-row source

The D0.3 repository search did not establish the canonical identity source for the 78 rows used by accepted B1 v1.7. The fact that H80 has 78 unique canonical identities is not evidence that H80 and B1 contain the same records. No intersection, equality, overlap, or disjointness may be inferred from the matching cardinality.

The missing B1 identity source is a **hard stop** for final cross-bank disjointness clearance and final diagnostic manifest freeze. Before that gate can close, an authoritative row-level B1 identity source must be located or established, its provenance and relation to accepted B1 v1.7 must be verified, and the 78 keys must be independently recomputed or checked against the accepted record definition.

H80 must not be substituted for this missing source. The search status remains OPEN / NOT ESTABLISHED; this protocol draft does not resolve it.

### 9.2 Protected evaluation set

Any future diagnostic-to-protected-evaluation disjointness test must be performed through the separately appointed independent custodian. The construction agent must not obtain protected evaluation records merely to perform a collision check. The custodian must compare canonical identities under a predeclared procedure and return a signed/hash-bound PASS or FAIL report with the exact compared-set identifiers and counts, without disclosing protected inputs to the construction agent.

A missing custodian, absent evaluation-set identity specification, missing comparison report, or any overlap is a hard stop. The construction agent must not independently access, copy, inspect, hash, or reconstruct protected records.

### 9.3 Freeze condition

Even if a future execution GO separately permits candidate construction, final manifest freeze remains blocked until:
1. the authoritative 78-row B1 development key source is established;
2. the B1 development overlap check passes;
3. the protected evaluation frame and canonical identity definition are fixed in the accepted separate B1 amendment;
4. the independent custodian completes and reports the protected-set disjointness check;
5. all internal bank and oracle checks pass; and
6. all other consent, custody, trigger-(i), review and acceptance conditions are closed.

No condition in this section is waived by the quota-feasibility proof.

## 10. Freeze sequence for a later authorized run

A future authorized run must follow this order:

1. Confirm that this protocol has completed Claude and GLM independent review, GPT adjudication, and explicit owner acceptance of the exact final protocol hash.
2. Confirm that all numeric and operational decisions in §11 are resolved and frozen.
3. Confirm separate execution GO and all consent, custodian, trigger-(i), and B1 amendment prerequisites.
4. Verify pinned v0.4 taxonomy and acceptance hashes byte-for-byte.
5. Verify generator, validators, interpreter/runtime and dependencies against their frozen hashes.
6. Freeze slot order, D6 pair order, parameter-selection rule, PRNG/seed material, draw order and retry policy.
7. Construct the proposed diagnostic package only within the authorized environment.
8. Run all generator-side checks and stop on any failure.
9. Run the independent validator against the exact generated bytes.
10. Obtain the independent custodian's disjointness result for the authoritative B1 development keys and protected evaluation set.
11. Freeze the manifest, oracle, rejection sidecar, validation report and hash inventory together.
12. Only after a successful freeze may a separately authorized next phase consider solver construction. This protocol does not grant that authorization.

Any change to a candidate, rule, slot, seed, draw order, retry policy, validator, or package after freeze invalidates the affected hashes and requires a new reviewed version and appropriate authorization. No post-outcome repair or replacement is permitted.

## 11. Unresolved decisions that block protocol freeze

The following items are deliberately not guessed or silently inherited. Each requires an explicit written resolution before this protocol can be frozen:

| ID | Decision required | Current status |
|---|---|---|
| P01 | Select deterministic parameter-selection mechanism for each D1–D8 family | OPEN |
| P02 | Decide whether to use a seeded PRNG selector or another method, and reconcile it explicitly with v0.4 §5.4 | OPEN |
| P03 | If a PRNG is used, name exact algorithm, implementation/version, seed material, stream allocation and draw order | OPEN |
| P04 | Pin generator interpreter/runtime build, dependencies and execution environment | OPEN |
| P05 | Confirm proposed slot order and D6 ascending/reverse presentation convention | PROPOSED, NOT ACCEPTED |
| P06 | Confirm proposed zero-retry rule, or adopt explicit finite per-slot and per-pair caps with a fail-closed exhaustion rule | PROPOSED, NOT ACCEPTED |
| P07 | Freeze exact rejection-stage ordering and sidecar schema | PROPOSED, NOT ACCEPTED |
| P08 | Freeze exact record serialization and record-hash rules beyond canonical identity bytes | OPEN |
| P09 | Freeze package/archive format, file inventory and newline/encoding rules | OPEN |
| P10 | Name the independent validator and establish reviewer separation | OPEN |
| P11 | Establish authoritative B1 78-row identity source and verify its provenance | OPEN / HARD STOP |
| P12 | Define protected evaluation frame and appoint independent custodian | OPEN / HARD STOP |
| P13 | Complete separate B1 amendment and all consent/trigger-(i) prerequisites | OPEN / HARD STOP |
| P14 | Obtain explicit owner acceptance of the final protocol hash and a separate execution GO | NOT ISSUED |

The protocol is not complete while any required decision is open. The design-only quota proof in §4 closes only the narrow question of whether the v0.4 predicates admit a simultaneous 8-per-stratum, 60-identity construction. It does not close the decisions above.

## 12. Current disposition

**v0.4 taxonomy:** OWNER-ACCEPTED at blob `8873389a0b38a7c9a1307f1c4f9fe4f7dee13def`.  
**This protocol:** DRAFT v0.1 for independent review only.  
**Simultaneous quota feasibility:** Constructively demonstrated at the level of parameterized families; no manifest or bank created.  
**D7 scale:** Addressed by a bounded 48-filler construction and (O(n a)) exact DP validation; no search or benchmark run.  
**Exact (W/N_0) protocol:** Proposed two independent arbitrary-precision implementations; implementation/runtime pins remain open.  
**Retry policy:** Zero retries proposed; not owner-accepted.  
**PRNG, seed, runtime and draw order:** OPEN.  
**B1 78-row identity source:** OPEN / NOT ESTABLISHED; hard stop for final cross-bank clearance and manifest freeze.  
**Protected-set custody and disjointness:** OPEN.  
**Generator, bank generation and solver work:** NOT AUTHORIZED.  
**Gate 0:** OPEN.  
**Project pause:** REMAINS IN FORCE.

No bank, generator, candidate list, manifest, oracle output, rejection sidecar, solver body, or experimental outcome was created by this document.
