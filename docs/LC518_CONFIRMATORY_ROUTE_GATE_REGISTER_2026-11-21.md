# LC518 confirmatory-route gate register

**Record ID:** LC518-CONFIRMATORY-ROUTE-GATE-REGISTER-2026-11-21  
**Date:** 2026-11-21  
**Purpose:** Record the evidence and decisions still required before any confirmatory evaluation. This is a blocker register, not approval or execution authorization.

## 1. Governing facts

- The owner selected a confirmatory route **with consent**.
- The accepted B1 v1.7 acceptance record continues to report the joint-consent provenance gap as open.
- The v0.21 population-design document proposes a **new protected evaluation set**. It explicitly says the existing 78-record public development bank is not the new confirmatory target and requires a separate B1 amendment.
- Accepted B1 v1.7 and Rev 1.4 remain unchanged.
- Owner acceptance of operational taxonomy v0.4 does not clear any of the gates below.
- The current status grants no protected-set access and no execution GO.

## 2. Gate register

| Gate | Status | Evidence/decision required to close | Why it cannot be marked complete now |
|---|---|---|---|
| Joint-consent provenance | **OPEN** | Contemporaneous consent record identifying all relevant parties, scope, date, authority and explicit relation to the 2026-11-05 B1 decision. The record must be attributable and its bytes/path pinned. | The B1 acceptance record says the provenance gap remains open. The owner's present statement that a route was selected “with consent” is not a substitute for the missing contemporaneous record or proof of its scope. |
| Independent protected-set custodian | **OPEN** | Named independent custodian; documented appointment/acceptance; defined custody role, key/access controls, separation from construction/evaluation agents, access logging, release conditions and incident handling. | No independent custodian is identified or appointed in the controlling B1 acceptance and v0.21 records searched for this update. GPT cannot appoint a third party by assertion. |
| Trigger-(i) interpretation | **OPEN** | Exact written interpretation of trigger-(i), including the statistical condition, what evidence activates it, what conclusion it permits, who adjudicates it, and the required treatment if evidence is incomplete or unavailable. It must be reviewed and ratified in the governing decision record. | The v0.21 design record identifies statistical ratification as open. No ratification is evidenced by v0.4 taxonomy acceptance. |
| Separate B1 amendment | **NOT ACCEPTED / REQUIRED** | A versioned amendment for the new protected target, specifying target population and sampling frame; record/canonical identity; outcome rows and correctness predicate; scoring denominator; training/test rows and folds; B1 exact-cell support and rank rules; estimand and model; full-vector/comparator scope if any; fitting, aggregation and availability rules; synthetic controls; reporting and computational burden; custody and integrity checks. It must be independently reviewed and GPT-adjudicated, then explicitly accepted by the owner.

**Important distinction about existing B1 v1.7 rules:** for its current 78-record public development target, v1.7 already specifies the equal-parent \\(\\Delta LL\\) aggregation, version-by-canonical-record binary outcome rows, LOPO folds, scored-set rules, deterministic fitting/separation handling, and explicit test unavailability in §5.7 V5. N4-a replication unavailability and no-replacement are specified in §8(vii). These rules remain accepted and frozen for their existing target. The separate amendment for a new protected target must state exactly which rules carry forward and how the changed record set affects outcome rows, denominator, folds, support/rank checks, fitting workload, and availability. A new \`NOT_ESTIMABLE\` status or trigger must be reconciled explicitly with existing V5 unavailability and must not be introduced as an unexplained synonym. The amendment does not rewrite v1.7 in place. | B1 v1.7 is accepted/frozen for the existing 78-record public development set. It does not automatically govern a newly created protected set. No separate amendment for that target has been accepted. |
| Further execution GO | **NO GO** | A distinct, explicit owner authorization naming the exact accepted amendment, bank/specification hashes, environment, custodian, permitted operation, operators, evidence retention, and stop conditions. | No prior taxonomy acceptance or documentary review is an execution GO. The project pause remains in force. |

## 3. Repository search scope for this register

The following source records were read or inspected as part of the current Gate 0 review:

- B1 analysis plan v1.7, blob `8c666e501a31726c728447d155045c0b20adc178`, using symbolic rows (r=1,ldots,78).
- B1 v1.7 acceptance record, blob `ea51d72f4f85c5d832d72add561b4c93472c364a`.
- Population-and-experimental-design v0.21, blob `8af908f6b0ad4cd060194a0a63f4914939f07756`, whose §0 records joint consent, trigger-(i), and custodian gates as open and requires a separate B1 amendment for the proposed protected set.
- Accepted B1 publication tree at `ac06c6676982eed795db9cb04c6d91803b591ac7` (348 entries).
- Population v0.21 branch snapshot `7365ad5138595cd82736d325aea3fee28c85bcc0` (416 entries).
- Current Gate 0 branch snapshot `8ddb7fa5228dd7c0dedf7bcb467e7b005bf403c5` (345 entries).

The file-name searches in those trees did not locate a contemporaneous consent document, custodian appointment, or trigger-(i) ratification. The governing B1 and v0.21 source text explicitly reports those gaps. This bounded repository search is not proof that no off-repository or private record exists; an owner-supplied attributable record may change the relevant status after review.

No consent mailbox, private account, protected evaluation data, blind E3, private mutation annex, or owner-local archive was accessed for this register.

## 4. Required order

1. Obtain and verify the contemporaneous joint-consent record.
2. Appoint the independent custodian and document custody controls.
3. Resolve and ratify trigger-(i), including the evidence and incomplete-evidence semantics.
4. Draft and review the separate B1 amendment against the accepted v1.7 and Rev 1.4 authorities.
5. Obtain explicit owner acceptance of the exact B1 amendment hash.
6. Only then consider a separate execution GO for a precisely bounded operation.

A gate must not be inferred complete from a later gate or from a general owner statement. Failure to obtain required evidence results in an explicit blocked/unavailable status, not a silent substitute.

## 5. Overall disposition

**CONFIRMATORY ROUTE: SELECTED, NOT AUTHORIZED.** Consent provenance, independent custodian, trigger-(i) ratification and separate B1 amendment remain open. There is no execution GO. No protected evaluation record was accessed and no confirmatory evaluation was performed.
