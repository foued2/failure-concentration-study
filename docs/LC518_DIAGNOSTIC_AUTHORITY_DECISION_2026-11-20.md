# LC518 diagnostic-specification authority decision

**Decision ID:** LC518-DIAG-AUTH-2026-11-20  
**Version:** 1.1  
**Decision date:** 2026-11-20  
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

If each of the other 70 H1–H5/H7–H8 records also has a unique canonical identity, the complete 80-row H1–H8 bank would have 78 unique canonical identities. This is the count pattern identified in the cross-review. The design text alone does not prove that the other 70 records contain no additional within-stratum or cross-stratum canonical collisions; the frozen H80 manifest is required to establish the exact unique-identity count and multiplicities.

This arithmetic supports, but does not establish, the following D0.3 hypothesis: the B1 v1.7 78-record development bank might contain exactly the 78 unique canonical identities obtained by collapsing the two H6 ordering pairs in the historical 80-row H80 bank.

The accepted B1 v1.7 plan and its acceptance record do not cite BANK_DESIGN v1.0/H80, provide the 78 identities, or state that the rows were obtained by canonical de-duplication. Therefore equality, partial overlap, and disjointness of the two identity sets are all **OPEN**. Do not state that B1 is H80 deduplicated; equally, do not claim that the identity sets differ merely because the documents assign them different roles.

Even if the identity sets prove equal, the design objects remain different in role and provenance: H80 is the earlier package's 80-raw-record held-out target; B1 v1.7's 78 rows are publicly exposed development rows used in its accepted analysis plan. Identity-set equality would establish lineage or overlap, not make the targets analytically interchangeable or sealed.

The decisive comparison, if separately authorized after the current pause is lifted, is an identity-only comparison of all 80 H80 records and all 78 B1 rows using normalized keys `(amount, tuple(sorted(coins)))`. It must report the distinct-key count for each bank, duplicate multiplicities, intersection, H80-only keys, B1-only keys, and exact manifest hashes/provenance. Raw row count, a claimed total of 78, or equality of opaque IDs alone is insufficient. No such comparison is performed by this decision; the current pause and no-bank-access boundary remain in force.

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
| Historical H1–H8 held-out bank | 80 raw records in BANK_DESIGN v1.0; H6's two reordered pairs account for 10 rows but 8 canonical identities; total unique identities are 78 only if the other 70 rows are unique | Not adopted as B1 v1.7's target; its identity-level relation to B1's 78 rows is unresolved; not v0.21's proposed new protected set |

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

This decision does **not** choose among those future routes, create a bank, reconstruct a manifest, or change the current statistical formula.

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

**Review/provenance limitation:** This is GPT's documentary source adjudication under the instruction to start the authority decision. Claude's earlier supplied comments agreed that no current D1–D8 operational specification had been adopted, but those comments did not represent a separate direct inspection of every source listed here. This record is not represented as a formal joint GPT/Claude sign-off or as a new owner ratification of a bank specification.

## 9. Pause and authorization boundary

This is a documentation-only authority determination. It does not reopen the paused project and authorizes no bank access, bank generation, oracle access, solver construction or modification, compilation, execution, diagnostic probing, outcome collection, simulation, sampling, predictive fitting, or power analysis. No frozen specification, bank, manifest, or solver was modified by this decision.

**Final ruling:** accepted authority exists for the symbolic eight-stratum statistical structure and B1 analysis procedure. **No operational D1–D8 specification is presently adopted for v0.21.** The H80-to-B1-78 identity-set relationship is an explicit, untested D0.3 hypothesis, not an established lineage finding. Gate 0 remains open.
