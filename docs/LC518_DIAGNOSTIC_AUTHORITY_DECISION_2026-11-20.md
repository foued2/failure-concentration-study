# LC518 diagnostic-specification authority decision

**Decision ID:** LC518-DIAG-AUTH-2026-11-20  
**Version:** 1.5  
**Decision date:** 2026-11-20  
**Revision date:** 2026-11-21  
**Revision note:** v1.5 records the GPT adjudication of the first v0.21 specification challenges, the resulting v0.3 draft and its updated hash, the exact C_D feasibility envelope and k=0 convention from accepted Rev 1.4, D6 canonical-key sensitivity, and the H80 H2 oracle-answer-conditioned filter interpretation. H80-to-B1 identity remains open.  
**Status:** GPT SOURCE-ADJUDICATION RECORDED; NO CURRENT OPERATIONAL D1–D8 SPECIFICATION ADOPTED  
**Repository:** `foued2/failure-concentration-study`  
**Scope:** Documentary authority determination for the current v0.21 population-design route. Not a bank specification, protocol amendment, owner ratification of new strata, freeze, or execution authorization.

---

## 1. Decision

For the current v0.21 research route, the accepted source chain controls the **symbolic statistical structure**, but no source presently controls the **operational meanings and membership rules** of D1–D8.

The controlling symbolic layer is:

1. **B1/M1 Rev 1.4 Amendment E**, accepted for the symbolic feasibility specification by its separate GPT acceptance record. The Rev 1.4 acceptance is not a separate formal freeze.
2. **B1 analysis plan v1.7**, accepted and frozen as a symbolic analysis plan by its separate GPT acceptance record. It is not an execution GO.

The inherited Rev 1.1 §1.2 diagnostic structure, retained by Rev 1.4 §§1.1–1.4, states `S = 8` strata and `R_s = 8` records per stratum as **abstract structural constants** and expressly says no bank data are executed or reused by that specification. It defines the mathematical quantities `f_s(v)`, `M(v) = max_s f_s(v)`, and `C_D(v) = M(v)/k(v)`. It does not define the named input challenges D1–D8.

**Authority ruling:** the current design has an accepted eight-stratum/eight-record-per-stratum symbolic structure, but **no adopted operational D1–D8 specification or current v0.21-linked diagnostic manifest**. The old D1–D8 names and rules must therefore not be treated as binding for v0.21, and no current-design diagnostic outcomes may be counted or interpreted under an assumed v1.0/C9 mixture.

This is a positive determination of the present authority state: **NO OPERATIONAL D1–D8 SPECIFICATION IS ADOPTED.** It is not an adoption of BANK_DESIGN v1.0, C9 rev 2.6, or a newly invented replacement.

## 2. The controlling statistical layer and what it actually fixes

### 2.1 Rev 1.4 Amendment E

The accepted Rev 1.4 specification is the symbolic B1/M1 feasibility specification. Its inherited §§1.1–1.4 preserve `S = 8`, `R_s = 8` as abstract structural constants, the failure/unresolved count definitions, and the Berger–Parker maximum-share expression. The acceptance record states that Rev 1.4 is accepted for the symbolic specification, while distinguishing acceptance from a separate formal freeze.

The abstract structure implies 64 diagnostic record slots in the mathematical design. It does **not** establish 64 generated records, actual record identities, named input categories, item-level rule parameters, canonical IDs, or a frozen manifest.

### 2.2 B1 v1.7

B1 v1.7 is accepted and frozen as a symbolic analysis plan. Its primary outcome unit is version × canonical-record correctness on the fixed **78-record publicly exposed development bank**. That bank is development data, is not sealed confirmatory data, and supports no new-record generalization claim under v1.7.

The 78-record outcome bank is not the 64-slot diagnostic structure. The plan says diagnostic tables supply each version's identity, family, totals, and (C_D); it does not supply the missing operational D1–D8 construction rules or adopt BANK_DESIGN v1.0 by path/blob.

The v1.7 acceptance record supersedes the plan file's draft-time header status. It freezes the symbolic analysis plan only, not execution.

### 2.3 v0.21 population design

Population-design v0.21 is explicitly a design-only draft. It names B1 v1.7 and its acceptance record as the binding symbolic analysis-plan reference, and Rev 1.4 Amendment E as the controlling symbolic feasibility specification. It does not enumerate D1–D8 construction rules or incorporate BANK_DESIGN v1.0 by exact path and blob.

v0.21 also proposes a new protected evaluation set. Its text expressly says that this set cannot be silently substituted for the 78-record B1 development bank and requires a separately reviewed B1 amendment before that new target is used. v0.21 selects no parent implementations or mutation mechanisms and authorizes no bank access or execution.

## 3. Why BANK_DESIGN v1.0 is not current operational authority

BANK_DESIGN v1.0 is marked FROZEN by GLM on 2026-11-01 for the earlier **LC518 150-Body Construction Study**. It defines:

- 64 diagnostic records, eight per D1–D8 stratum;
- named historical input categories and construction rules for D1–D8;
- a separate 80-record H1–H8 held-out bank.

That freeze establishes the status of the earlier study-package design. It does not itself establish adoption by the later Rev 1.4/B1 v1.7/v0.21 source chain.

There is also a material target distinction: BANK_DESIGN v1.0 specifies an 80-record held-out bank, whereas accepted B1 v1.7 specifies the publicly exposed 78-record development bank as its outcome-record population. v0.21 proposes a further protected evaluation set and requires a separate B1 amendment. These must not be collapsed into one “held-out bank”.

The 64-record D bank in v1.0 happens to match the `8 × 8` abstract structure in Rev 1.4. Equal counts do not prove identity of record membership or semantic adoption. No exact path/hash cross-reference or owner-authorized selective adoption of BANK_DESIGN v1.0 §6 into v0.21 was found in the records reviewed.

**Disposition:** BANK_DESIGN v1.0 remains authoritative for its earlier frozen package and is a historical candidate source for possible selective adoption. It is not the current operational D1–D8 authority for v0.21.

### 3.1 D0.3 identity-reconciliation hypothesis: H80 may reduce to 78 canonical inputs

BANK_DESIGN v1.0 §2 defines canonical identity as `(amount, tuple(sorted(coins)))`; permutation copies of one mathematical instance share one canonical identity. Its §5 H6 row specifies 10 raw records as 2 canonical instances × 2 orderings plus 6 singleton records. H6 therefore contains 8 canonical identities.

The owner-authorized inspection of artifact 13210063805 now establishes the actual H80 count: the bank contains 80 raw rows and exactly 78 distinct canonical identities. The only duplicate groups are the two H6 reorder pairs, H057/H058 (H6-P01) and H059/H060 (H6-P02). No additional within-stratum or cross-stratum canonical collisions occur. All 80 stored canonical IDs recompute from `(amount, tuple(sorted(coins)))`, and all rows satisfy the distinct-denomination input rule. The two H6 pairs account for exactly two excess raw rows.

The verified H80 result strengthens the D0.3 hypothesis: its 78 canonical keys are exactly represented by its 78 oracle-output objects. However, this still does not establish that B1 v1.7's 78 development rows are those same identities. The B1 plan and acceptance record do not provide a B1 identity list or cite H80 by artifact ID/hash.

The accepted B1 v1.7 plan and its acceptance record do not cite BANK_DESIGN v1.0/H80, provide the 78 identities, or state that the rows were obtained by canonical de-duplication. Therefore equality, partial overlap, and disjointness of the two identity sets are all **OPEN**. Do not state that B1 is H80 deduplicated; equally, do not claim that the identity sets differ merely because the documents assign them different roles.

Even if the identity sets prove equal, the design objects remain different in role and provenance: H80 is the earlier package's 80-raw-record held-out target; B1 v1.7's 78 rows are publicly exposed development rows used in its accepted analysis plan. Identity-set equality would establish lineage or overlap, not make the targets analytically interchangeable or sealed.

The decisive comparison, if separately authorized after the current pause is lifted, is an identity-only comparison of all 80 H80 records and all 78 B1 rows using normalized keys `(amount, tuple(sorted(coins)))`. It must report the distinct-key count for each bank, duplicate multiplicities, intersection, H80-only keys, B1-only keys, and exact manifest hashes/provenance. Raw row count, a claimed total of 78, or equality of opaque IDs alone is insufficient. No such comparison is performed by this decision; the current pause and no-bank-access boundary remain in force.

### 3.1.1 Oracle-output cardinality and rejection-sidecar reconciliation

BANK_DESIGN v1.0 §7 says the oracle answer is computed once per canonical instance and attached to every raw record of that instance. The later C9 rev 2.6 proposal gives a more explicit file schema: one oracle-output object per distinct `canonical_id`, with both rows of an H6 reorder pair sharing one object. C9 rev 2.6 is unratified and is cited here only as a proposed serialization rule, not as current authority.

Under that one-object-per-canonical-identity schema, 80 raw H80 records and 78 oracle-output objects are mutually consistent **if and only if** H80 has 78 distinct canonical identities and every accepted bank record resolves to one of those output objects. The count of oracle-output objects should be compared with the number of distinct canonical identities, not automatically with the number of raw input rows. The actual artifact schema and generator provenance must be verified before applying this interpretation.

A rejection sidecar records rejected candidate attempts, not absent oracle outputs for accepted records. C9 rev 2.6's proposed schema gives each rejection event an attempt number, bank, planned candidate/instance ID, reason, and stratum. Rejected attempts are generation history; a candidate slot may be retried and later appear as an accepted record. Consequently, a sidecar containing two rejection events does not, by itself, explain why an already completed 80-row bank has 78 oracle-output objects. The sidecar must be reconciled against attempt numbers, accepted rows, and the generator's publication report. It must not be treated as subtracting two rows from the final bank merely because two rejection events exist.

A Claude review message supplied on 2026-11-21 reports an exposed held-out artifact with 80 input rows, 78 oracle outputs, and a file named `heldout_bank.rejections.jsonl`; it also states that the sidecar was not inspected. These three artifact-level statements remain **REPORTED-NOT-REPRODUCED** in this decision. Neither the artifact nor the sidecar was opened or hashed here.

#### Required D0.3 comparison protocol

If the project is separately reopened and this documentary comparison is authorized, perform these steps in order:

1. **Freeze provenance before inspecting identities.** Record exact artifact IDs/paths, byte sizes, and SHA-256 hashes for `heldout_bank.json`, `heldout_oracle_outputs.json`, `heldout_bank.rejections.jsonl`, the canonical-disjointness/publication report, the applicable B1 78-row source manifest and its oracle attachment, and the generator/specification revisions used to produce them. Commit or otherwise timestamp this inventory before computing any identity intersection. Missing artifacts must be reported as missing, not inferred.
2. **Validate the input domain.** Confirm each record has distinct coin denominations, as required by BANK_DESIGN v1.0 §1. If any record repeats a denomination, stop and report a contract/design violation; do not silently normalize it by dropping duplicates.
3. **Recompute identity without information loss.** Use `(amount, tuple(sorted(coins)))`. Sorting the tuple makes order irrelevant but preserves denomination multiplicity. Do not replace the tuple with a set or otherwise collapse repeated values.
4. **Reconcile accepted rows and oracle keys.** Report raw H80 row count, distinct canonical-key count, duplicate multiplicities, oracle-object count and exact oracle-key set. Every accepted raw row must resolve through its canonical identity to one oracle object; each distinct accepted identity must have exactly one object; there must be no missing or extra oracle keys. Confirm that each H6 reorder pair shares one key and one oracle answer. Compare B1's 78 source rows by the same normalized key, not by opaque IDs alone.
5. **Reconcile the rejection sidecar separately.** Validate its schema and each event's attempt, candidate/instance ID, reason, bank, and stratum against the pinned generator rules and publication report. Summarize events by reason and stratum; trace retry histories to their eventual accepted slots where applicable. Do not require a rejected planned ID to be absent from the final bank if a later attempt for that same slot was accepted. Conversely, do not count rejected attempts as accepted bank records or as missing oracle outputs.
6. **Publish the identity-set result.** Report `|H_raw|`, `|K_H|`, `|O_H|`, `|K_{B1}|`, `|K_H ∩ K_{B1}|`, H80-only keys, B1-only keys, all duplicate multiplicities, row-to-oracle resolution, sidecar reconciliation, and the frozen hashes. Preserve a machine-readable audit output and a reviewer-readable explanation.

Interpretation is predetermined:

- If H80 has 80 raw rows, 78 distinct canonical keys, 78 matching oracle keys, and the B1 set equals those 78 keys, the H80-to-B1 identity hypothesis is supported. This is not evidence that the two banks had interchangeable roles.
- If H80 has 80 raw rows and 80 distinct keys but only 78 oracle keys, two accepted identities lack oracle objects; this is an artifact/acceptance defect or an unresolved schema mismatch. Two sidecar rejection events do not repair it.
- If H80 has 78 distinct keys and 78 oracle keys but B1's keys differ, the 80/78 arithmetic is not evidence that B1 is H80 deduplicated.
- If the intersection is partial, report the exact overlap and set differences; do not describe the banks as either identical or disjoint.
- Rejection-sidecar events are a separate generation-history result. They explain the 80/78 oracle cardinality only if the pinned artifact schema and row-level reconciliation demonstrate a direct effect; their count alone is insufficient.

### 3.1.2 Authorized H80 artifact result

The owner authorized inspection of GitHub Actions artifact `13210063805` (`lc518-bank-run-41591572358-1`, workflow run `41591572358`). Its archive SHA-256 was recorded from GitHub metadata before download and independently matched the downloaded 75,523-byte ZIP. All 15 archive-member byte sizes and SHA-256 hashes were recorded before parsing the bank, oracle, and H80 sidecar contents.

The detailed audit is recorded in `docs/LC518_D0_3_RECONCILIATION_RESULT_2026-11-21.md`. The controlling H80 findings are:

- `heldout_bank.json`: 80 raw rows, 80 unique input IDs, 78 unique canonical IDs; all 80 denomination lists are distinct; all stored canonical IDs recompute correctly.
- The only duplicate groups are H057/H058 (H6-P01; original/permutation) and H059/H060 (H6-P02; original/permutation). Each pair shares one canonical ID and differs only in coin ordering.
- `heldout_oracle_outputs.json`: 78 objects, 78 unique canonical keys. Its key set equals the H80 canonical-key set exactly. Every raw H80 record resolves to exactly one oracle object with matching amount and sorted denominations; no keys are missing or extra.
- `heldout_bank.rejections.jsonl`: 26 events, all `bank=heldout`, `stratum=H2`, `reason=H2_ORACLE_BELOW_TWO`, across candidate slots H018–H024. Every affected candidate slot later appears as an accepted H2 row. These events are retry history and do not explain the 80-to-78 oracle count.
- `canonical_disjointness_report.json`: status PASS; 80 held-out raw rows, 78 held-out unique canonical identities, and zero cross-bank collisions in each reported D/H stratum. Its hash and all six referenced artifact hashes match the archived bytes.
- `run_manifest.json`: reports item-8 PASS, overall generation-run status ACCEPTED, process exit 0, and 57 test-suite passes. Its aggregate rejection count is 63 across both banks. Only the H80 sidecar was parsed for this D0.3 scope; the diagnostic sidecar was not inspected.

The run's `ACCEPTED` status records the generator/launcher acceptance checks for this artifact. It does not owner-ratify C9 rev 2.6, make C9 current v0.21 authority, or change the status of any accepted B1/Rev 1.4 source.

**Result:** the historical H80 bank is an internally consistent 80-raw-row / 78-canonical-key input bank with exactly 78 corresponding oracle objects. The 80-to-78 difference is explained by H6 permutation identity collapse, not by rejected H80 attempts.

### 3.1.3 B1 identity source remains unestablished

The accepted B1 v1.7 analysis plan defines its outcome rows as canonical records (r=1,ldots,78), and its acceptance record confirms the fixed 78-record publicly exposed development set. Neither document supplies the 78 keys or cites artifact 13210063805, `heldout_bank.json`, or `heldout_oracle_outputs.json` by immutable identity.

A repository-tree check of B1 acceptance commit `ac06c6676982eed795db9cb04c6d91803b591ac7` (348 entries) found the B1 plan and acceptance records but no B1 78-row bank manifest or canonical-record/oracle attachment. The symbolic index (r=1,ldots,78) is not an identity list.

Accordingly, the H80 canonical set (K_H) and B1 development set (K_{B1}) cannot yet be compared directly. Do not substitute H80's oracle keys for (K_{B1}) solely because both have cardinality 78. Equality, partial overlap, and disjointness remain **OPEN** until the independently attributable B1 78-row source is identified with provenance and immutable hash.

If the owner identifies `heldout_oracle_outputs.json` from artifact 13210063805 as the intended B1 source, that linkage must be supported by contemporaneous or authoritative B1 provenance; it cannot be inferred after the fact from matching counts.

#### Coin-denomination identity rule

BANK_DESIGN v1.0 §1 states that denominations are distinct. Thus an input such as `[1,1,2]` is outside the stated valid input domain and must fail validation rather than enter the bank comparison. The identity tuple `(amount, tuple(sorted(coins)))` would in any case preserve multiplicity: `[1,1,2]` and `[1,2]` produce different sorted tuples. Do not use set-based normalization. If an actual artifact contains repeated denominations, stop the identity audit and report the violation; do not decide post hoc whether repeated denominations should be treated as equivalent.

#### Consequences if identity equality is confirmed

If B1's 78 identities equal the 78 unique canonical identities in H80, then B1's development rows are not a distinct mathematical-input set from the historical H80 package. The historical H80 target cannot be described as an independent or unseen input set relative to B1. Any cross-study claim that uses H80 as a separate held-out validation of B1 on new canonical inputs must be withdrawn or narrowed.

This finding alone would **not** invalidate the accepted B1 v1.7 symbolic analysis plan or change its stated status: B1 v1.7 explicitly treats its 78 rows as publicly exposed development data and supports no new-record generalization claim. Its prespecified finite-development-bank analysis remains distinguishable from a claim of independent validation on new inputs. What would be invalid is any stronger description of B1's 78 rows as independent of H80, or any use of H80 as an independent target relative to that same B1 development set.

The separate phrase in B1 v1.7 that the frozen blind E3 is untouched must be assessed against E3's own exact identity manifest and custody history. H80/B1 identity equality does not by itself prove overlap with E3 or prove that E3 was accessed. Do not relabel E3 as H80, or claim E3 contamination, without its own identity and custody evidence. If E3 overlaps B1 or H80, that requires a separate consequence assessment.

If the comparison instead finds partial overlap, only the non-overlapping identities can be described as distinct; the full H80 and B1 sets cannot be called independent. If it finds disjoint sets, that rejects this specific lineage hypothesis but does not by itself establish E3 blindness or any broader confirmatory validity.


## 4. Why C9 revision 2.6 is not current authority

C9 rev 2.6 pins detailed proposed generator rules, including refinements to D4 and D5. Its own status says the revision has not received separate follow-up review, is not owner-ratified or frozen, and does not modify historical BANK_DESIGN v1.0. It states that the historical design-of-record sources remain authoritative until separate owner ratification.

C9 may be used as review material. Its changed details, including the proposed D4 subtype allocation and D5 construction rules, cannot be treated as binding for v0.21.

**Disposition:** C9 rev 2.6 is not current authority and does not supersede BANK_DESIGN v1.0 or amend the accepted Rev 1.4/B1 v1.7 statistical framework.

## 5. Keep the four data/design objects separate

| Object | Source-supported status | What it is not |
|---|---|---|
| Eight diagnostic strata × eight records | Accepted symbolic structure inherited through Rev 1.4; 64 abstract diagnostic slots | Not proof of a generated or current D1–D8 manifest |
| Historical D1–D8 diagnostic bank | Defined in BANK_DESIGN v1.0 for the earlier 150-body package; 64 records | Not automatically adopted by v0.21 |
| B1 v1.7 development/outcome records | Fixed 78-record publicly exposed development bank | Not the diagnostic bank and not sealed confirmatory data |
| Historical H1–H8 held-out bank | Artifact 13210063805 verifies 80 raw records and 78 unique canonical identities; the only duplicates are the two H6 reorder pairs; 78 exact oracle objects resolve all raw rows | Not adopted as B1 v1.7's target; identity-level relation to B1's 78 rows remains unresolved because no independent B1 identity source is specified |

## 6. Consequences for the research claim

Until an operational diagnostic specification and manifest are adopted:

1. The eight-component vector `F = (f_1, ..., f_8)` is only symbolically defined by eight abstract strata. The current input meaning of each component is not fixed.
2. A calculation of `C_D` is mathematically definable once the eight record groups and outcomes exist, but its current-design construct interpretation is not established without the operational stratum definitions.
3. Historical descriptions of D1–D8 may be made only with an explicit reference to BANK_DESIGN v1.0 and its earlier-package status.
4. The D4 composite, D5 objective-validity, and D6 record-versus-pair weighting questions must be adjudicated against the specification eventually adopted. The prior review conclusions remain design requirements; they do not convert C9 into authority.
5. No diagnostic outcome should be used to resolve source authority or retrospectively choose stratum membership.

## 7. What would create operational authority

A future operational specification must be selected through an explicit, versioned source decision. The owner may consider, without any default presumption:

- selectively adopting BANK_DESIGN v1.0 §6 as the diagnostic specification while explicitly stating that its separate 80-record H1–H8 bank is not thereby substituted for the B1/v0.21 evaluation target;
- separately reviewing and ratifying a clearly enumerated subset of C9 rev 2.6, with every adopted and rejected change identified; or
- issuing a new v0.21-linked diagnostic specification.

Whichever route is chosen must identify the exact specification path, revision and immutable blob; the current diagnostic manifest hash; each record's ID, assigned stratum, rule ID, canonical identity and rule parameters; the D4 subtype allocation if applicable; the D6 pair identities and ordering; and the relation to the applicable B1 analysis plan and evaluation target. Any change to the B1 statistical structure or outcome target requires a separately reviewed B1 amendment.

Owner route decision (2026-11-21): **a new v0.21-linked operational diagnostic-stratum specification is selected** rather than adopting BANK_DESIGN v1.0 §6 or ratifying a C9 subset. Draft `docs/LC518_V0_21_OPERATIONAL_DIAGNOSTIC_STRATA_SPEC_2026-11-21_v0.1.md` is on branch `gpt/lc518-v021-operational-strata-spec-2026-11-21`, current revision v0.3, blob SHA-1 `299464b2057d352416ddd6db1ee489ac09617394`. It preserves the accepted symbolic eight-stratum/eight-record interface and proposes new input-property rules, but remains **DRAFT FOR INDEPENDENT REVIEW; NOT ADOPTED; NOT FROZEN; NO BANK-GENERATION OR EXECUTION GO**. GPT has adjudicated the summary-based first comments; Claude has not yet conducted a direct file-level review of v0.3 and GLM's review remains pending. The draft requires direct independent challenge, GPT adjudication, and explicit owner acceptance of an exact reviewed hash. It must not amend Rev 1.4 or B1 v1.7 in place.

This decision does **not** create a new diagnostic bank or manifest, reconstruct an allocation, or change the current statistical formula.

## 8. Source register and provenance

| Source | Branch/ref | Blob SHA-1 | Authority finding |
|---|---|---|---|
| Rev 1.1 symbolic specification (inherited §§1.1–1.4) | `dbdc82984a9259aa6d731bc6a64224373d74673b` | `516f856c16aa8da02f43dc1e1a90f347ad872838` | Specifies (S=8), (R_s=8) as abstract constants; no named D1–D8 input categories |
| Rev 1.4 Amendment E | `b8b8af042c16eeb9e02077c781ab05c582eeb65d` | `3728146356a74363a94fe75a87fd06c483954ee2` | Accepted symbolic B1/M1 feasibility specification; acceptance is distinct from formal freeze |
| Rev 1.4 acceptance record | `ca15a29bd25c4c9c2293394f67cb19e1a18f34bd` | `074b40980eb96d164cd8411c8995bb1db4af0d46` | Authoritative acceptance event for Rev 1.4 Amendment E |
| B1 analysis plan v1.7 | `c3abe107acd2a3f8be58bf933eafcd734823a129` | `8c666e501a31726c728447d155045c0b20adc178` | Accepted/frozen symbolic analysis plan; 78-record development outcome population |
| B1 v1.7 acceptance record | `ac06c6676982eed795db9cb04c6d91803b591ac7` | `ea51d72f4f85c5d832d72add561b4c93472c364a` | Authoritative acceptance/freeze event; not execution GO |
| Population design v0.21 | `gpt/lc518-m1si-audit-2026-11-17` | `8af908f6b0ad4cd060194a0a63f4914939f07756` | Current population-design draft; does not adopt named D1–D8 rules |
| BANK_DESIGN v1.0 | `gpt/lc518-claim-b1-primary-2026-11-05` | `d91b8dcee05808926262c3636a891b776c03ab44` | Frozen historical 64/80 bank design for earlier 150-body package; not adopted by v0.21 |
| C9 generation spec review rev 2.6 | `gpt/lc518-claim-b1-primary-2026-11-05` | `bd9f13fee63ee2716345447461bf3b8bcd904eaa` | Detailed but unratified/unfrozen replacement proposal |
| Analysis spec review draft | `gpt/lc518-claim-b1-primary-2026-11-05` | `c47760b1ca9121291f600db87b1e90665d57b8f6` | Review-only analysis draft; no authority to adopt D1–D8 |
| New v0.21 operational diagnostic-strata spec v0.3 | `gpt/lc518-v021-operational-strata-spec-2026-11-21` | `299464b2057d352416ddd6db1ee489ac09617394` | Owner-selected new route; GPT review amendments; still draft only, not adopted or frozen |
| First-review adjudication record | `gpt/lc518-v021-operational-strata-spec-2026-11-21` | `c03cf8b8d27730ef4186a36c836d6c3f3cda98cc` | GPT adjudication of provisional Claude summary-based comments; not independent Claude file review |

**Review/provenance limitation:** This is GPT's documentary source adjudication under the instruction to start the authority decision. Claude's earlier supplied comments agreed that no current D1–D8 operational specification had been adopted, but those comments did not represent a separate direct inspection of every source listed here. This record is not represented as a formal joint GPT/Claude sign-off or as a new owner ratification of a bank specification.

## 9. Pause and authorization boundary

This is a documentation-only authority determination with a later bounded owner GO. On 2026-11-21, the owner authorized the D0.3 identity/provenance comparison for artifact 13210063805, specifically its H80 bank, H80 oracle attachment, H80 rejection sidecar, publication report, and run-manifest fields. That bounded inspection was completed and is recorded in `docs/LC518_D0_3_RECONCILIATION_RESULT_2026-11-21.md`. The artifact is to be preserved and was not deleted or modified. The owner also selected drafting of a new v0.21-linked operational diagnostic-stratum specification.

This bounded GO does not authorize solver construction or modification, compilation, execution, diagnostic outcome collection, access to blind E3 or other protected evaluation records, model fitting, simulation, sampling, power analysis, or confirmatory evaluation. The confirmatory route was selected with consent, but the B1 acceptance record's joint-consent provenance gap remains open; independent custody, trigger-(i) ratification, and a separately reviewed B1 amendment are also still required. No frozen Rev 1.4/B1 specification, bank, manifest, or solver was modified by the H80 audit.

**Final ruling:** accepted authority exists for the symbolic eight-stratum statistical structure and B1 analysis procedure. **No operational D1–D8 specification is presently adopted for v0.21.** H80-to-oracle reconciliation is complete: 80 raw rows, 78 unique canonical identities, and 78 matching oracle objects. The H80 sidecar contains 26 H2 retries; these use the oracle-answer rule `H2_ORACLE_BELOW_TWO`, so accepted H2 records are conditioned on (W\ge2), but the retries do not explain the 80-to-78 oracle cardinality. This is task-answer selection, not solver-outcome selection, and the H80 target remains the fixed finite 80-record list. H80-to-B1 identity equality remains OPEN because the independently attributable B1 78-row source is not established. Repeated denominations are invalid under the stated input domain. The owner-selected new v0.21 taxonomy is draft v0.3, not adopted or frozen. Confirmatory evaluation remains blocked on consent/custody/amendment gates. Gate 0 remains open.
