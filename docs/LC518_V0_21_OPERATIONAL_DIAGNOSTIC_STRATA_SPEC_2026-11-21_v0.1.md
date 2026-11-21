# LC518 v0.21 operational diagnostic-strata specification

**Document ID:** LC518-V021-ODS-2026-11-21  
**Version:** 0.4  
**Date:** 2026-11-21  
**Status:** DRAFT FOR INDEPENDENT SCIENTIFIC REVIEW; v0.4 CLARIFIES STRATUM DESCRIPTION, FIXED-MIX LIMITATIONS, ORACLE CONDITIONS, AND THE GLOBAL ANSWER-BOUND REFERENCE; NOT ADOPTED OR FROZEN; NO BANK-GENERATION OR EXECUTION GO  
**Selected route:** New v0.21-linked operational specification, per owner instruction dated 2026-11-21.  
**Scope:** Define a new outcome-blind eight-stratum diagnostic taxonomy for the v0.21 population-design route.  
**Does not modify:** Accepted B1/M1 Rev 1.4 Amendment E, accepted B1 analysis plan v1.7, historical BANK_DESIGN v1.0, or C9 rev 2.6.

---

## 1. Purpose and governing decisions

This document is the new specification route selected by the owner. It does not selectively adopt historical BANK_DESIGN v1.0 §6 and does not ratify C9 rev 2.6. It defines a fresh operational proposal for the meaning and assignment of diagnostic strata D1–D8 under population-design v0.21.

The proposal preserves the accepted symbolic design structure:

- (S=8) diagnostic strata;
- (R_s=8) raw diagnostic records per stratum;
- 64 raw diagnostic records in total; and
- the existing record-weighted Berger–Parker maximum-share statistic.

The current v0.21 route still lacks an adopted operational D1–D8 specification. This draft does not become that authority until it passes independent scientific review, GPT adjudication, and explicit owner acceptance of an exact version/hash. It is not a frozen manifest, a generator implementation, or authorization to generate or run any bank.

### 1.1 Scientific object

A stratum is a predeclared category of LC518 input records. It is not a mutation mechanism, a program fault, or a causal explanation. The eight assigned categories describe input properties and challenge families. They must not be described as eight proven causes of solver failure.

The diagnostic bank is intended to measure a solver version's definite-failure distribution over these assigned input categories. The separate evaluation bank measures correctness on a declared evaluation distribution. This specification does not establish the diagnostic-to-evaluation transport relationship; that remains a separate Gate 0 evidence requirement.

### 1.2 Binding statistical interface

The accepted Rev 1.4/B1 framework remains unchanged. For solver version (v):

- (f_j(v)) is the number of definite failed diagnostic records assigned to stratum (j);
- (k_{mathrm{fail}}(v)=sum_{j=1}^{8}f_j(v));
- (k_{mathrm{unresolved}}(v)) is counted separately and does not enter the concentration numerator or denominator;
- (M(v)=max_j f_j(v)); and
- (C_D(v)=M(v)/k_{mathrm{fail}}(v)) when (k_{mathrm{fail}}(v)ge1).

When (k_{\mathrm{fail}}=0), the numerical index (C_D) is **undefined** under accepted Rev 1.4 §3.2. Report the status **NO OBSERVED FAILURES** and leave (C_D) undefined; do not substitute zero as a numeric index. Do not report unresolved records as definite failures. This specification does not introduce a new concentration index.

The primary concentration calculation remains record-weighted. Canonical-identity counts and D6 pair summaries are required exposure/dependence diagnostics, not replacements for the accepted (f_j) definition.

### 1.3 Finite-sample feasibility of the primary C_D statistic

Each diagnostic stratum contains eight raw records, so each definite-failure count satisfies (0\le f_j\le8), and the total definite-failure count satisfies (0\le k_{\mathrm{fail}}\le64). For a fixed total (k=k_{\mathrm{fail}}\ge1), the possible maximum failure count is exactly

[
\left\lceil\frac{k}{8}\right\rceil \le M \le \min(k,8),
]

and every integer (M) in this interval is attainable by some allocation of (k) failures across eight strata with capacity eight per stratum. Therefore the exact attainable concentration values are

[
C_D\in\left\{\frac{m}{k}:m=\left\lceil\frac{k}{8}\right\rceil,\ldots,\min(k,8)\right\}.
]

| Definite failures (k) | Attainable integer maxima (M) | Attainable (C_D) values |
|---:|---|---|
| 1–8 | (1,\ldots,k) | ({m/k:m=1,\ldots,k}) |
| 9–16 | (2,\ldots,8) | ({m/k:m=2,\ldots,8}) |
| 17–24 | (3,\ldots,8) | ({m/k:m=3,\ldots,8}) |
| 25–32 | (4,\ldots,8) | ({m/k:m=4,\ldots,8}) |
| 33–40 | (5,\ldots,8) | ({m/k:m=5,\ldots,8}) |
| 41–48 | (6,\ldots,8) | ({m/k:m=6,\ldots,8}) |
| 49–56 | (7,8) | ({7/k,8/k}) |
| 57–64 | (8) only | ({8/k}) |

For (k=0), (C_D) is undefined; report **NO OBSERVED FAILURES** with no numeric index, as specified by Rev 1.4 §3.2. For (k\ge1), the attainable set above applies for every unresolved count (\ell\) satisfying (k+\ell\le64); the exact-maximum construction is proved in accepted Rev 1.4 §3.2.

Thus (M) has only nine possible integer values, 0 through 8, but (C_D)'s attainable values depend on the denominator (k). For (k\ge57), the maximum must equal eight and (C_D) is forced to (8/k). A repeated or nearly flat (C_D) across versions must not be interpreted without conditioning on (k_{\mathrm{fail}}) and these design-imposed limits. This is a deterministic feasibility fact, not a prediction about solver outcomes or a power calculation.



---

## 2. LC518 task contract and construction quantities

### 2.1 Valid input domain

Every diagnostic record must satisfy the LC518 contract:

- target amount is an integer in ([0,5000]);
- coin denominations are positive integers in ([1,5000]);
- denominations within an input are distinct;
- (1le nle300);
- the coin array may be in any order; and
- the exact LC518 answer fits a signed 32-bit integer.

Equivalently, the exact answer for every valid input is no greater than 2,147,483,647. This is a **global LC518 contract condition** applying to every diagnostic record, not a D8-specific selection criterion.

Malformed-input behaviour is outside the study contract. A repeated denomination is a contract violation, not a second representation of the same valid input. Do not normalize coin arrays with a set.

### 2.2 Exact task answer and bounded-combination comparison

Let (C=(c_1,ldots,c_n)) be the set of distinct denominations and (a) the target.

Define (W(a,C)) as the exact LC518 answer: the number of unordered combinations satisfying

[
sum_{i=1}^{n}x_i c_i=a,qquad x_iinmathbb Z_{ge0}.
]

Each denomination can be used an unlimited number of times. The order in which denominations are selected does not distinguish combinations.

For construction validation only, define (N_0(a,C)) as the number of unordered combinations satisfying the same equation with (x_iin{0,1}), so each denomination can be used at most once. (N_0) is not the LC518 answer and is not a solver outcome.

The D5 construction requires (W>N_0), which proves that at least one LC518 combination requires repeated use of a denomination. Do not substitute a minimum-coin objective or a greedy-output comparison for this condition.

### 2.3 Canonical identity

A canonical input identity is

[
K(a,C)=(a,operatorname{tuple}(operatorname{sort}(C))).
]

Input order is ignored; denomination multiplicity is preserved. Under the contract, multiplicity must always be one because each input has distinct denominations. The serialized `canonical_id` must be derived deterministically from the canonical JSON representation of the amount and sorted coin tuple and must be independently recomputed during validation.

---

## 3. Proposed D1–D8 assignments

Each stratum has exactly eight raw diagnostic records. The ranges and predicates below are binding within this draft. A record must satisfy exactly one stratum definition. The conditions are written to make the eight assignments mutually exclusive by construction constraints, not by outcome-dependent relabelling.

The full manifest must record the exact rule parameters and the validation quantities (W) and (N_0) where specified. All eight records in a stratum must meet that stratum's rule; no candidate may be kept merely to fill a slot.

| Stratum | Proposed name | Required construction rule | Intended challenge |
|---|---|---|---|
| **D1** | Boundary, zero-target and below-minimum cases | (2le nle10); (c_{min}ge3); (3c_{min}+1le1500); (gcd(C)=1); target (a) is one of ({0,1,c_{min}-1,c_{min}+1,2c_{min}-1,2c_{min}+1,3c_{min}-1,3c_{min}+1}); (a ∉ C); (W=N_0). The eight target positions are represented once each. | Zero-target, below-minimum and near-multiple boundary handling without exact-denomination membership or repeated-use multiplicity. |
| **D2** | Single-denomination exact match | (n=1); (2le c_1=ale1500). Therefore (W=N_0=1). | Direct exact-match handling in the smallest denomination-set case. |
| **D3** | Exact match with distractors | (2le nle10); (2le ale1500); exactly one denomination equals (a); every other denomination is greater than (a); (gcd(C)=1). Therefore (W=N_0=1). | Exact-denomination recognition in the presence of irrelevant larger denominations. |
| **D4** | Parity-unreachable target | (2le nle10); every denomination is even; (gcd(C)=2); target (a) is odd, (3le ale1500), and (c_{min}le a). Therefore (W=N_0=0). | Modular/parity unreachability when the odd target is at or above the smallest available denomination, rather than merely below every available denomination. |
| **D5** | Repeated-use combination multiplicity | (2le nle10); (10le ale1500); (a ∉ C); (gcd(C)=1); (Wge2) and (W>N_0). The exact values (W) and (N_0) are stored as pre-outcome construction checks. | LC518-specific combination-count multiplicity where at least one valid combination requires repeated use of a denomination. No greedy or minimum-coin criterion is used. |
| **D6** | Reordering pairs | Four distinct canonical instances, each emitted as two records: one original ordering and one non-identity permutation. Thus 4 canonical identities and 8 raw records. Each instance has (11le nle30), (100le ale1500), (gcd(C)=1), (a ∉ C), and (W=N_0ge1). | Order-invariance challenge, with repeated-use multiplicity excluded by the construction rule. |
| **D7** | Wide-denomination-set cases | (50le nle300); (50le ale500); (gcd(C)=1); (a ∉ C); and (1le W=N_0le10). | Large denomination-array traversal while keeping the number of valid combinations bounded and requiring no repeated-denomination use. |
| **D8** | Large-target cases | (3le nle30); (2000le ale5000); (a ∉ C); (gcd(C)=1); (Wge1); (Wle2{,}147{,}483{,}647) (redundant restatement of the global §2.1 validity condition, not a D8-specific filter). Store (W) and (N_0) for descriptive validation. | Large-target computation on valid reachable inputs. This is not a high-answer-count stress stratum; combination multiplicity is reported rather than silently assumed homogeneous. |

### 3.1 Exclusivity and assignment validation

The eight rules are pairwise disjoint by the following explicit separators; no priority rule is needed:

| Comparison | Separating conditions |
|---|---|
| D2 vs D1/D3/D4/D5/D6/D7/D8 | D2 requires (n=1); every other stratum requires (n\ge2). |
| D1 vs D3 | D1 requires (a\notin C); D3 requires exactly one (a\in C). |
| D1 vs D4 | D1 requires (gcd(C)=1); D4 requires (gcd(C)=2). |
| D1 vs D5 | D1 requires (W=N_0); D5 requires (W>N_0). |
| D1 vs D6/D7 | D1 has (2\le n\le10); D6 has (11\le n\le30); D7 has (n\ge50). |
| D1 vs D8 | D1's largest permitted target (3c_{\min}+1) is at most 1,500; D8 requires (a\ge2,000). |
| D3 vs D4 | D3 requires (gcd(C)=1); D4 requires (gcd(C)=2). |
| D3 vs D5/D6/D7/D8 | D3 requires (a\in C); each of D5–D8 requires (a\notin C). |
| D4 vs D5/D6/D7/D8 | D4 requires (gcd(C)=2); D5–D8 require (gcd(C)=1). |
| D5 vs D6 | D5 requires (2\le n\le10); D6 requires (11\le n\le30). |
| D5 vs D7 | D5 requires (n\le10); D7 requires (n\ge50). |
| D5 vs D8 | D5 requires (a\le1,500); D8 requires (a\ge2,000). |
| D6 vs D7 | D6 requires (n\le30); D7 requires (n\ge50). |
| D6 vs D8 | D6 requires (a\le1,500); D8 requires (a\ge2,000). |
| D7 vs D8 | D7 requires (n\ge50) and (a\le500); D8 requires (n\le30) and (a\ge2,000). |

The D4 condition (a\notin C) is implicit because every denomination is even and the target is odd. These separators cover all pairs of distinct strata.

The validator must evaluate every candidate against all eight rules and confirm exactly one eligible assignment. If zero or more than one rule matches, reject the candidate and record the cause. Do not resolve an overlap by arbitrary priority assignment or after observing solver outcomes. No record reassignment stage exists; therefore there is no reassignment count to report. No diagnostic records have been generated under this draft.

At whole-bank validation, the 64 raw records must yield exactly **60 distinct canonical identities**. The only permitted within-bank duplicate groups are the four D6 pair identities, each occurring exactly twice within its own declared pair. No canonical identity may appear in two different D6 pairs, in two different strata, or in any non-D6 record alongside another row. Any such collision fails the complete bank validation and must not be silently repaired by dropping or relabelling a row.

### 3.2 Pre-outcome construct hypotheses and reporting

The strata are defined by observable input properties and intended computational/semantic challenges. The following are **a priori susceptibility hypotheses**, not claims that a solver population must have different failure rates across all eight strata, not causal conclusions, and not predictions of an effect size or ranking.

| Stratum | Input property | Pre-outcome susceptibility hypothesis | Required descriptive report |
|---|---|---|---|
| D1 | Eight target positions around zero and successive multiples of the minimum denomination, including two guaranteed below-minimum targets | May expose zero-target, below-minimum, off-by-one, and small-boundary logic errors | Report each target position separately, including (W) and (N_0). Identify a=1 and a=c_min−1 as guaranteed unreachable (W=N_0=0), and a=0 as W=N_0=1; do not hide position heterogeneity inside (f_1). |
| D2 | One denomination equal to the target | May expose the single-denomination/base-case path and exact-match handling | Report the exact-match outcome count; (W=N_0=1) is fixed by construction. |
| D3 | One exact-match denomination plus larger distractors | May expose loops or membership logic that mishandle denominations larger than the target | Report (n), the exact-match denomination, and distractor range. |
| D4 | All denominations even, gcd 2, odd target at or above the minimum denomination | May expose modular/parity unreachability handling when the target is not merely below all available denominations | Report target and (c_{\min}), and verify (W=0). |
| D5 | (W>N_0) and (W\ge2) | May expose a 0/1-use recurrence or other implementation that fails to count unlimited repeated use correctly | Report both exact counts (W) and (N_0) for every record. |
| D6 | Same canonical input under two non-identical orders | May expose dependence on input ordering when the contract requires order invariance | Report pairwise PASS/FAIL/UNRESOLVED patterns and the pair-mean sensitivity in §4. |
| D7 | 50–300 distinct denominations with a bounded small positive answer | May expose scaling or traversal issues in the denomination dimension without high answer-count complexity | Report (n), target, (W=N_0), and the bounded-answer band. |
| D8 | Large target, 3–30 denominations, reachable answer, without a high-answer-count selection rule | May expose target-dimension memory/time or array-boundary issues at large permitted target amounts; does not deliberately select high answer-count cases | Report (n), target, (W), and (N_0). The signed-32-bit answer bound is global under §2.1, not a D8-specific stress criterion. |

The primary hypothesis is that these predefined input challenges may elicit different failure profiles from some implementation classes. There is **no prespecified universal direction or rank order** of stratum failure rates across the solver population. A common failure rate across strata is possible and would not retroactively make input assignment invalid; it would, however, limit the empirical concentration observed beyond the finite-sample constraints in §1.3.

The proposed 64 raw records constitute an **engineered, oracle-checked finite challenge suite**, not a probability sample of naturally occurring LC518 inputs. They are selected to satisfy predeclared input-property and exact-answer predicates. Equal allocation of eight records per stratum is a design allocation, not evidence that the eight categories have equal prevalence in naturally occurring LC518 inputs. (C_D) therefore describes concentration over this fixed, equally allocated suite. It is not a natural-population prevalence-weighted failure share.

The strata are not calibrated or equated for baseline difficulty. Equal record allocation does not imply equal difficulty, comparable failure opportunity, or equivalent computational burden. The observed (f_j) values and (C_D) summarize definite failures over this exact challenge mix and therefore combine implementation behaviour with the difficulty and composition of the assigned records. This specification defines no baseline-difficulty measure or adjustment. Accordingly, (C_D) does not support an interpretation as difficulty-adjusted, mix-independent, or intrinsic implementation failure concentration, and this suite alone does not support extrapolation to differently weighted input distributions. A larger stratum failure count cannot, from this design alone, be attributed uniquely to greater implementation susceptibility rather than greater baseline challenge difficulty.

### 3.3 Non-emptiness witnesses (illustrative only)

The following small examples demonstrate that the defining predicates are mathematically nonempty. They are not frozen bank records, are not assigned input IDs, and must not be copied into a future manifest without the ordinary collision and freeze checks.

- D1: (C={3,11}), (c_{min}=3), with the eight targets (0,1,2,4,5,7,8,10); all targets differ from the denominations and (W=N_0).
- D2: (C={5}), (a=5); (W=N_0=1).
- D3: (C={5,11,13}), (a=5); the two distractors exceed the target and (W=N_0=1).
- D4: (C={4,6}), (a=5); (gcd(C)=2), (W=N_0=0), and (c_{min}le a).
- D5: (C={1,3}), (a=6); (W=3), (N_0=0).
- D6: (C={21,79,101,103,107,109,113,127,131,137,139}), (a=100); (W=N_0=1); an original and any non-identity permutation form one pair.
- D7: (a=100), with denominations 37 and 63 plus 48 distinct denominations greater than 100; (W=N_0=1).
- D8: (C={997,1003,1500}), (a=2000); (W=N_0=1).

These witnesses establish only that the predicates can be satisfied. They do not establish that a deterministic seeded generator can fill all 64 slots under all collision, disjointness, and overflow guards. That requires a separate design-only feasibility review before any generator is implemented or run.

---

## 4. D6 dependence and the unchanged concentration measure

D6 contains eight raw records but only four distinct canonical inputs. Each pair consists of the same mathematical input presented in two different coin orders. The manifest must carry:

- a unique `pair_id` for each of the four pairs;
- the shared `canonical_id`;
- `ordering = original` for one record and `ordering = permutation` for the other; and
- evidence that the permutation is non-identity while preserving the sorted denomination tuple and amount.

The primary concentration measure remains record-weighted under the accepted B1 formula. Its estimand is the share of definite **record-level failures** across the 64 diagnostic presentations. D6 deliberately allocates eight record presentations to four canonical inputs so that both orders are tested. Those two presentations count as two record exposures in the accepted primary formula; they are not eight independent canonical inputs. This choice preserves the accepted record-level (f_j) estimand and the explicit purpose of testing order invariance. It does not give equal weight to unique mathematical inputs.

A pair contributes to (f_6) as follows:

| Original | Permutation | Contribution to (f_6) |
|---|---|---:|
| PASS | PASS | 0 |
| PASS | FAIL | 1 |
| FAIL | PASS | 1 |
| FAIL | FAIL | 2 |

A definite FAIL remains a definite failure even if both orderings return the same wrong integer. If a member is UNRESOLVED, its definite FAIL partner, if any, still contributes to (f_6); unresolved records are counted separately in (k_{mathrm{unresolved}}).

D6's pair-level discordance summary must be reported separately from (C_D). (C_D) is a share of failed records, not a share of independent canonical inputs and not itself an order-sensitivity statistic. A pair-weighted (f_6) or pair-weighted concentration measure would change the accepted measurement and requires a separate B1 amendment. This draft does not make that change.

### 4.1 Canonical-identity-weighted descriptive sensitivity

Because D6 gives each of four mathematical inputs two raw presentations while every other diagnostic identity has one, the report must also provide a clearly secondary **canonical-identity-weighted descriptive sensitivity**. This is not the accepted primary (C_D), does not replace record weighting, and must not receive confirmatory inferential status under B1 v1.7 without a separate B1 amendment.

For canonical identity (q), let (R_q) be its raw records whose result is resolved as PASS or FAIL. If (|R_q|\ge1), define

[
u_q=\frac{\#\{r\in R_q:r\text{ is FAIL}\}}{|R_q|}.
]

Thus a D6 pair contributes 0 for PASS/PASS, (1/2) for PASS/FAIL or FAIL/PASS, and 1 for FAIL/FAIL. An unresolved member is not counted as a failure; the average is over resolved members only, and the unresolved-record count is reported separately. A canonical identity with no resolved member is omitted from the sensitivity denominator and reported as wholly unresolved.

For stratum (j), let (K_j) be its distinct canonical identities and define

[
F_j^{(K)}=\sum_{q\in K_j:|R_q|\ge1}u_q,\qquad
K_{\mathrm{fail}}=\sum_{j=1}^{8}F_j^{(K)}.
]

When (K_{\mathrm{fail}}>0), report

[
C_D^{(K)}=\frac{\max_jF_j^{(K)}}{K_{\mathrm{fail}}}.
]

When (K_{\mathrm{fail}}=0), the sensitivity ratio is undefined; report **NO OBSERVED FAILURES AMONG RESOLVED CANONICAL IDENTITIES** with no numeric sensitivity value. Always report the number of distinct identities with at least one resolved member, the number wholly unresolved, and the number of unresolved raw records. This sensitivity gives each distinct mathematical input one unit of total weight while averaging over the two D6 orders; it is descriptive only.



---

## 5. Manifest, oracle and freeze requirements

### 5.1 Diagnostic manifest fields

Each raw record must include at least:

- `input_id` (unique within the 64-row diagnostic bank);
- `stratum` (`D1`–`D8`);
- `rule_id` and all rule parameters needed to reproduce membership;
- `amount`;
- `coins` in as-given order;
- `canonical_id`;
- `pair_id` and `ordering` for D6 only;
- `oracle_output_file_sha256`; and
- `record_sha256`.

Construction-check fields (W) and (N_0), where required, must be stored in an auditable construction-validation attachment. They are not solver outputs and must not be inferred from candidate solver behaviour.

### 5.2 Oracle attachment

There must be exactly one oracle-output object per distinct canonical identity, not one object per raw row. Each object contains the canonical ID, amount, sorted denominations, and exact LC518 answer (W). The two records of a D6 pair resolve to the same object.

Under this draft's 64-record structure, the whole-bank validator requires exactly 60 distinct canonical identities: four D6 pair keys with multiplicity two, and 56 other keys with multiplicity one. The diagnostic oracle attachment must therefore contain exactly 60 distinct-key objects. This is a design expectation to be checked against the future frozen manifest, not an observed artifact. Any other duplicate pattern is a validation failure.

### 5.3 Rejection sidecar

Every rejected whole-record or pair candidate attempt must be logged with attempt number, bank, candidate/slot ID, stratum, and one declared reason code. A rejected attempt is not an accepted record and must not be confused with a missing oracle object. Retry history must reconcile to the final accepted slot IDs and the generator's publication report.

### 5.4 Hash and freeze sequence

Before any solver body is constructed or modified:

1. Freeze the exact specification revision, generation protocol, deterministic PRNG/interpreter details, seeds, slot order, draw order, rejection reasons, and retry limits.
2. Generate the diagnostic bank only after a separate execution GO.
3. Hash the complete raw bank, oracle attachment, rejection sidecar, and validation report.
4. Independently recompute every canonical identity, record hash, oracle key mapping, stratum assignment, D6 pair identity/order, and within-bank collision summary.
5. Verify diagnostic-to-evaluation canonical disjointness through the independent custodian required by the evaluation plan, without exposing protected evaluation inputs to the construction agent.
6. Freeze the manifest hashes and validation outputs before solver construction, source mutation, or any solver outcome is observed.

Any change after outcome collection requires a new version, fresh hash, and separate review. No post-outcome stratum reassignment or record replacement is permitted.

---

## 6. Relationship to B1 and the evaluation target

B1 v1.7 remains the accepted symbolic analysis plan for its fixed, publicly exposed 78-record development bank. It is not a sealed confirmatory bank and supports no new-record generalization claim. Its separate identity source has not yet been identified in the D0.3 audit; the H80 oracle keys must not be assumed to be B1's keys based on matching cardinality alone.

Population-design v0.21 proposes a new protected evaluation set. Using that protected set in the confirmatory target requires a separate B1 amendment covering the new record population, outcome rows, scoring denominator, fold/test definitions, support and rank checks, computational burden, custody, and controls. This document does not silently substitute the new protected set into B1 v1.7.

Before a future diagnostic manifest can be frozen, its canonical identities must be checked against every relevant exposed development input set and the separately defined evaluation set. The H80-to-B1 source gap and the selected confirmatory route's consent/custody requirements remain blockers to that later freeze.

### 6.1 Oracle-answer-conditioned construction is not population-neutral

The historical H80 audit identified 26 rejected H2 candidate attempts with reason code `H2_ORACLE_BELOW_TWO`; all 12 accepted H2 rows have oracle answer (W\ge2). The earlier BANK_DESIGN v1.0 describes H2 as a small-amount, multiple-combination challenge. The generator run operationalised that intended challenge by rejecting H2 candidates whose exact LC518 oracle answer was below two.

This is a filter on the **true task answer (W)**, not on a candidate solver's correctness outcome. It is therefore not post-hoc selection on solver PASS/FAIL. It nevertheless conditions the accepted H2 input distribution on (W\ge2). The H80 bank's published target is its fixed finite 80-record list with its declared record weights; no inference to all small-amount LC518 inputs is justified. The 26 retries are part of the provenance and selection history of that finite bank, not evidence of missing oracle objects.

The H80 (W\ge2) filter is **not automatically imported** into the new v0.21 diagnostic taxonomy. D1–D8 use only their own explicit, pre-outcome construction predicates. The proposed v0.21 rules include the following exact-answer conditions:

| Stratum | Exact-answer condition | How the condition enters the rule |
|---|---|---|
| D1 | (W=N_0) | Explicit construction predicate. |
| D2 | (W=N_0=1) | Implied by the single-denomination exact-match construction. |
| D3 | (W=N_0=1) | Implied by the exact-match denomination and all-larger-distractors construction. |
| D4 | (W=N_0=0) | Implied by all-even denominations and an odd target. |
| D5 | (W\ge2) and (W>N_0) | Explicit construction predicates. |
| D6 | (W=N_0\ge1) | Explicit construction predicate. |
| D7 | (1\le W=N_0\le10) | Explicit construction predicate. |
| D8 | (W\ge1) | Explicit reachability predicate. The upper bound (W\le2^{31}-1) repeated in the D8 rule is redundant because it already applies globally under §2.1; it is not a D8-specific filter. |

These conditions are part of the definitions of the proposed diagnostic categories. Some are explicit candidate-selection predicates; others are exact-answer consequences of the structural input rules. In either case, the resulting 64 records are an engineered, oracle-checked finite challenge suite. They are not a probability sample of LC518 inputs and do not define a representative or prevalence-weighted population of those inputs. The resulting interpretation is conditional on this exact declared challenge mix.

Any future protected evaluation bank must separately state its target population and sampling frame. If inclusion or rejection depends on (W), (N_0), or another oracle-derived input property, that condition must be justified and frozen in the separate evaluation design/B1 amendment before candidate selection. The resulting estimand is conditional on that declared sampling frame. Do not transfer the H80 H2 filter by default, describe an oracle-conditioned bank as representative of all LC518 inputs, or reject candidates based on solver outcomes.

### 6.2 Consent and custody status

The owner selected a confirmatory route **with consent**. The accepted B1 v1.7 acceptance record still states that the joint-consent provenance gap remains open. No contemporaneous consent evidence is created by this draft or by the owner's current instruction. Before confirmatory evaluation, the actual consent record, parties, scope, date, and relation to the 2026-11-05 B1 decision must be verified. An independent protected-set custodian must also be identified and appointed, and the trigger-(i) interpretation must be ratified before the separate B1 amendment is accepted.

---

## 7. Claims and interpretations prohibited by this specification

Do not:

- call D1–D8 eight causal mechanisms or eight proven failure causes;
- claim the categories are independent merely because their assigned labels are exclusive;
- describe (C_D) as a rate per independent canonical challenge;
- claim (C_D) measures order sensitivity;
- claim a greedy minimum-coin output is an LC518 combinations-count answer;
- use (G
e M) or any greedy criterion as the D5 validity condition;
- count unresolved records as definite failures;
- treat the 78-record B1 development bank as sealed or as evidence of new-record generalization;
- claim a diagnostic-to-evaluation transport relationship without the separate crosswalk and evidence;
- infer mutation/operator effects from stratum labels; or
- use historical H80 identities as current v0.21 diagnostic records or evaluation records without a separately reviewed decision.

---

## 8. Required independent review and closure gates

Before this specification can be accepted as the operational v0.21 D1–D8 authority, independent reviewers must challenge:

1. **D1 boundaries:** whether the eight target positions define a meaningful boundary construct and whether (W=N_0) is an appropriate homogeneity condition.
2. **D2/D3 distinction:** whether single-denomination and exact-match-with-distractors cases represent two scientifically useful challenge families rather than redundant categories.
3. **D4 parity:** whether a single homogeneous (gcd(C)=2), odd-target construction is the right scope and whether the (c_{min}le a) guard isolates the intended modular property.
4. **D5 task validity:** verify the (W) and (N_0) definitions and the exact implication of (W>N_0); no greedy/minimum-coin substitution.
5. **D6 dependence:** validate pair accounting, record-weighted (f_6), and the separate pair-level summary.
6. **D7/D8 support:** challenge whether the bounded-combination and large-target conditions are feasible and represent the intended computational stresses without post-outcome selection.
7. **Mutual exclusivity:** verify that every candidate has exactly one assigned stratum and that all eight definitions are deterministic and outcome-blind.
8. **Coverage and transport:** identify which evaluation properties are measured, which are omitted, and what evidence could support the diagnostic-to-evaluation crosswalk.
9. **Reproducibility:** specify deterministic construction, hash/freeze, rejection-sidecar and oracle-validation rules before a generator can be run.
10. **Finite-sample concentration feasibility:** verify the attainable (C_D) set for each (k_{\mathrm{fail}}) and assess the reporting implications of its discreteness.
11. **Canonical-identity weighting:** review the proposed descriptive sensitivity (C_D^{(K)}), its handling of unresolved pair members, and its separation from the accepted primary statistic.

**Acceptance gates:** independent scientific review; GPT adjudication; explicit owner acceptance of the exact document hash; a separate deterministic generation protocol; design-only feasibility review; identified B1 78-row source; resolved consent/custody/trigger-(i) gates; separate B1 amendment for the new protected target; and a further execution GO. Until those gates are complete, this draft is not current operational authority.

---

## 9. Authorization boundary

This draft authorizes documentary critique and revision only. It authorizes no bank generation, generator implementation or execution, mutation allocation, solver construction or modification, compilation, diagnostic probing, solver outcome collection, protected-set access, model fitting, simulation, sampling, or power analysis.

The owner's separate D0.3 GO authorized inspection of artifact 13210063805 for H80/oracle/sidecar identity reconciliation. That bounded audit is recorded separately. The artifact is to be preserved. The confirmatory route is selected with consent, but its historical consent, independent-custodian, trigger-(i), B1 amendment, and execution gates remain open.

**Current disposition:** New v0.21 operational diagnostic-strata route selected; this is draft v0.4 for independent review, not an accepted/frozen operational specification. The accepted symbolic eight-stratum structure is preserved. B1 v1.7 and Rev 1.4 remain unchanged. No experiment work is authorized.
